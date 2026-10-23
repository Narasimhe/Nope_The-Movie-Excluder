import json
import logging
import os
import re
import sqlite3
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.8-flash")
DEFAULT_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview")

SKILLS_REGISTRY = {
    "related": {
        "command": "/related",
        "name": "Related Movies Reality Check",
        "description": "Evaluates related movies on screen with craft takes and YES/NOPE verdicts.",
        "requires_dossier": False,
        "directive": (
            "ACTIVE SKILL: /related (Related Movies Reality Check)\n"
            "Evaluate the related movies on screen strictly by script craft, pacing, tension, and audience respect.\n"
            "Format each evaluated film as:\n"
            "**[Movie Title] ([Year])**\n"
            "[1-2 sentence sharp cinephile take on script, tension, atmosphere, or acting]\n"
            "Verdict: **YES** or **NOPE**\n\n"
            "Leave an empty line between each movie entry so it is effortless to scan.\n"
            "Deliver an honest, decisive YES or NOPE for each title, directly calibrated to the user's taste and quality standards."
        ),
        "default_query": "Are any of the related movies on screen worth my attention?",
    },
    "batch": {
        "command": "/batch",
        "name": "Batch Move / Queue",
        "description": "Applies library status changes to multiple movies simultaneously.",
        "requires_dossier": False,
        "directive": (
            "ACTIVE SKILL: /batch (Batch Move / Queue)\n"
            "Execute a batch status change on multiple movies (e.g. all YES movies to New Discovery).\n"
            "Return action type 'batch_set_movie_status' with status and the list of target movies."
        ),
        "default_query": "Add the approved YES movies to my New Discovery shelf.",
    },
    "research": {
        "command": "/research",
        "name": "Cinema Research Files",
        "description": "Manages focused 1-5 research markdown files in data/research/*.md.",
        "requires_dossier": True,
        "directive": (
            "ACTIVE SKILL: /research (Cinema Research Files)\n"
            "You manage 1–5 focused research markdown files stored directly in data/research/*.md.\n"
            "Active files on disk:\n{{RESEARCH_FILES_INDEX}}\n\n"
            "1. SAVE CHAT TO FILE: When asked to save/freeze chat (e.g. 'save this chat to [xyz] file'), format findings into markdown and return action 'save_research_file' with filename and content.\n"
            "2. ADD TO FILE: When asked to add or append an insight, word, director, or film to a research file (e.g. 'add this to high frequency words file'), match target file from active list and return action 'append_research_file' with filename and entry.\n"
            "3. RESEARCH INDEX: When asked 'what research files do I have?' or 'show research index', present the active files from {{RESEARCH_FILES_INDEX}} with filenames and details.\n"
            "4. DELETE FILE: When asked to delete a research file, return action 'delete_research_file' with filename."
        ),
        "default_query": "What research files do I have on disk?",
    },
}


class GreyService:
    def __init__(self, db_path: str = "data/movie_excluder.db"):
        self.db_path = db_path
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.research_dir = Path(__file__).resolve().parent.parent.parent / "data" / "research"
        self.research_dir.mkdir(parents=True, exist_ok=True)
        self.reactions_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "gifs_n_media"
        self.reactions_dir.mkdir(parents=True, exist_ok=True)
        self.reactions_file = Path(__file__).resolve().parent / "reactions.json"

    def get_reactions_index(self) -> str:
        if not self.reactions_dir.exists():
            return "No reaction media available."
        valid_exts = {".gif", ".webp", ".png", ".jpg", ".jpeg"}
        files = [f.name for f in self.reactions_dir.iterdir() if f.is_file() and f.suffix.lower() in valid_exts]
        if not files:
            return "No reaction media available."

        metadata: dict[str, str] = {}
        meta_file = self.reactions_file
        if meta_file.exists():
            try:
                metadata = json.loads(meta_file.read_text(encoding="utf-8"))
            except Exception:
                metadata = {}

        items = []
        for f in sorted(files):
            if f in metadata and metadata[f]:
                items.append(f"- `{f}`: {metadata[f]}")
            else:
                inferred = re.sub(r"[_\-]+", " ", Path(f).stem).strip()
                items.append(f"- `{f}`: {inferred}")

        return "\n".join(items)

    def get_research_files_index(self) -> str:
        if not self.research_dir.exists():
            return "No research files on disk yet."
        files = sorted(self.research_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)[:5]
        if not files:
            return "No research files on disk yet."
        items = []
        for f in files:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore").strip()
                size = f.stat().st_size
                if not content:
                    items.append(f"### File: `{f.name}` (Empty, 0 bytes)\n*(File currently contains no text)*")
                else:
                    snippet = content[:3000] + ("\n... [remaining text truncated]" if len(content) > 3000 else "")
                    items.append(f"### File: `{f.name}` ({size} bytes)\n```markdown\n{snippet}\n```")
            except Exception as e:
                items.append(f"### File: `{f.name}` ({f.stat().st_size} bytes)")
        return "\n\n".join(items)

    def resolve_research_file(self, query: str) -> Path | None:
        if not self.research_dir.exists():
            return None
        clean_q = re.sub(r"[^a-zA-Z0-9]", "", (query or "").lower())
        if not clean_q:
            return None
        files = list(self.research_dir.glob("*.md"))
        for f in files:
            if re.sub(r"[^a-zA-Z0-9]", "", f.stem.lower()) == clean_q:
                return f
        for f in files:
            f_clean = re.sub(r"[^a-zA-Z0-9]", "", f.stem.lower())
            if clean_q in f_clean or f_clean in clean_q:
                return f
        return None

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_taste_dossier(self) -> dict[str, Any]:
        """Extract user high-rated movies, watchlist items, and discarded patterns."""
        favorites = []
        watchlist = []
        discarded_count = 0

        try:
            with self._get_connection() as conn:
                # Top rated / high verdicts
                rows = conn.execute(
                    """
                    SELECT m.title, m.release_date, m.vote_average, u.verdict, u.notes
                    FROM movies m
                    JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                    WHERE u.verdict >= 8 OR u.is_favorite = 1
                    ORDER BY u.verdict DESC, m.vote_average DESC
                    LIMIT 15
                    """
                ).fetchall()
                for r in rows:
                    favorites.append({
                        "title": r["title"],
                        "year": (r["release_date"] or "")[:4],
                        "verdict": r["verdict"],
                        "notes": r["notes"],
                    })

                # Watchlist samples
                rows = conn.execute(
                    """
                    SELECT m.tmdb_id, m.title, m.release_date, m.vote_average
                    FROM movies m
                    JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                    WHERE u.status = 'watch_later'
                    ORDER BY m.vote_average DESC
                    LIMIT 20
                    """
                ).fetchall()
                for r in rows:
                    watchlist.append({
                        "tmdb_id": r["tmdb_id"],
                        "title": r["title"],
                        "year": (r["release_date"] or "")[:4],
                        "rating": r["vote_average"],
                    })

                # Discard count & notable samples
                row = conn.execute(
                    "SELECT COUNT(*) as cnt FROM user_movie_data WHERE status = 'excluded'"
                ).fetchone()
                if row:
                    discarded_count = row["cnt"]

                discarded_samples = []
                rows = conn.execute(
                    """
                    SELECT m.title, m.release_date, u.notes
                    FROM movies m
                    JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                    WHERE u.status = 'excluded'
                    ORDER BY (u.notes IS NOT NULL AND u.notes != '') DESC, u.updated_at DESC
                    LIMIT 8
                    """
                ).fetchall()
                for r in rows:
                    discarded_samples.append({
                        "title": r["title"],
                        "year": (r["release_date"] or "")[:4],
                        "notes": r["notes"] if r["notes"] else None,
                    })
                journal_digest = []
                j_rows = conn.execute(
                    """
                    SELECT entry_id, title
                    FROM general_entries
                    WHERE is_deleted = 0 AND is_archived = 0 AND status = 'published'
                    ORDER BY updated_at DESC
                    LIMIT 8
                    """
                ).fetchall()
                for jr in j_rows:
                    e_id = jr["entry_id"]
                    t_rows = conn.execute(
                        """
                        SELECT t.name FROM general_entry_tags t
                        JOIN general_entry_tag_links l ON t.tag_id = l.tag_id
                        WHERE l.entry_id = ?
                        """,
                        (e_id,),
                    ).fetchall()
                    journal_digest.append({
                        "title": jr["title"],
                        "tags": [tr["name"] for tr in t_rows],
                    })

                journal_notes_list = []
                jn_rows = conn.execute(
                    """
                    SELECT entry_id, title, status
                    FROM general_entries
                    WHERE is_deleted = 0 AND is_archived = 0 AND status = 'published'
                    ORDER BY updated_at DESC
                    LIMIT 50
                    """
                ).fetchall()
                for jnr in jn_rows:
                    journal_notes_list.append({
                        "entry_id": jnr["entry_id"],
                        "title": jnr["title"],
                        "status": jnr["status"],
                    })

                watched_titles = []
                w_rows = conn.execute(
                    """
                    SELECT m.title, u.verdict
                    FROM movies m
                    JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                    WHERE u.status = 'watched'
                    ORDER BY u.updated_at DESC
                    """
                ).fetchall()
                for r in w_rows:
                    v_str = f" ({r['verdict']}/10)" if r['verdict'] is not None else ""
                    watched_titles.append(f"{r['title']}{v_str}")

                rewatch_list = []
                rw_rows = conn.execute(
                    """
                    SELECT m.title, u.verdict
                    FROM movies m
                    JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                    WHERE u.status = 'rewatch'
                    ORDER BY u.updated_at DESC
                    """
                ).fetchall()
                for r in rw_rows:
                    v_str = f" ({r['verdict']}/10)" if r['verdict'] is not None else ""
                    rewatch_list.append(f"{r['title']}{v_str}")

                excluded_titles = []
                e_rows = conn.execute(
                    """
                    SELECT m.title
                    FROM movies m
                    JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                    WHERE u.status = 'excluded'
                    ORDER BY u.updated_at DESC
                    """
                ).fetchall()
                for r in e_rows:
                    excluded_titles.append(r["title"])
        except Exception as e:
            logger.warning(f"Error fetching taste dossier: {e}")

        return {
            "high_rated": favorites,
            "watchlist": watchlist,
            "discarded_count": discarded_count,
            "discarded_samples": discarded_samples,
            "journal_digest": journal_digest if 'journal_digest' in locals() else [],
            "journal_notes_list": journal_notes_list if 'journal_notes_list' in locals() else [],
            "all_watched_titles": watched_titles if 'watched_titles' in locals() else [],
            "rewatch_list": rewatch_list if 'rewatch_list' in locals() else [],
            "all_excluded_titles": excluded_titles if 'excluded_titles' in locals() else [],
        }

    def _deduplicate_and_format_note_body(
        self,
        existing_body: str,
        new_body: str,
        mode: str,
        user_message: str,
        inspected_movie_id: int | None = None,
        inspected_movie_title: str | None = None,
    ) -> str:
        lower_msg = (user_message or "").lower()
        wants_raw = any(
            w in lower_msg
            for w in [
                "as it is",
                "raw",
                "verbatim",
                "plain text",
                "no toggle",
                "without toggle",
                "dont format",
                "don't format",
            ]
        )
        wants_toggle = (
            any(
                w in lower_msg
                for w in ["toggle", "collapse", "collpase", "collapsible", "expandable", "spoiler"]
            )
            and not wants_raw
        )

        # 1. Identify target movie title candidates
        candidate_titles: list[str] = []
        if inspected_movie_title and len(inspected_movie_title.strip()) >= 2:
            candidate_titles.append(inspected_movie_title.strip())

        if not candidate_titles and inspected_movie_id:
            try:
                with self._get_connection() as conn:
                    row = conn.execute("SELECT title FROM movies WHERE tmdb_id = ?", (inspected_movie_id,)).fetchone()
                    if row and row["title"]:
                        candidate_titles.append(row["title"].strip())
            except Exception:
                pass

        raw_new_lines = [l.strip() for l in (new_body or "").splitlines() if l.strip()]
        first_line_clean = ""
        if raw_new_lines:
            first_line = raw_new_lines[0]
            first_line_clean = re.sub(r"^(?:<details\b[^>]*>|<summary\b[^>]*>|[•\-*]|\d+\.|\>\>|\-\>|[▸▶])\s*", "", first_line)
            first_line_clean = re.sub(r"</summary>.*$", "", first_line_clean).strip()
            m = re.match(r"^([^(\n:\-\[<]+)", first_line_clean)
            if m:
                extracted = m.group(1).strip()
                if len(extracted) >= 2 and extracted.lower() not in ["the", "a", "an", "movie", "film", "note", "critique", "review", "here", "ok"]:
                    if extracted not in candidate_titles:
                        candidate_titles.append(extracted)

        # Expand candidate_titles with normalized forms (without 'The', 'A', 'An', and trailing years/plurals)
        expanded_candidates: list[str] = []
        for cand in candidate_titles:
            if cand not in expanded_candidates:
                expanded_candidates.append(cand)
            norm = re.sub(r"^(?:the|a|an)\s+", "", cand, flags=re.IGNORECASE).strip()
            if norm and norm not in expanded_candidates:
                expanded_candidates.append(norm)
            stem = norm.rstrip("s").strip()
            if stem and len(stem) >= 3 and stem not in expanded_candidates:
                expanded_candidates.append(stem)
        candidate_titles = expanded_candidates

        # 2. Check if existing_body contains any candidate title
        existing_text = (existing_body or "").strip()
        matched_cand = None
        for cand in candidate_titles:
            pattern = rf"\b{re.escape(cand)}\b"
            if re.search(pattern, existing_text, re.IGNORECASE):
                matched_cand = cand
                break

        # If user message explicitly mentions a known title in existing_text, prefer that
        if existing_text:
            for line in existing_text.splitlines():
                stripped = line.strip()
                clean_l = re.sub(r"^(?:[•\-*]|\d+\.|\>\>|\-\>|[▸▶]|#+)\s*", "", stripped)
                m = re.match(r"^([^(\n:\-\[<]+)", clean_l)
                if m:
                    t = m.group(1).strip()
                    if len(t) >= 3 and re.search(rf"\b{re.escape(t)}\b", user_message, re.IGNORECASE):
                        matched_cand = t
                        if t not in candidate_titles:
                            candidate_titles.insert(0, t)
                        break

        # Extract critique block for matched candidate in existing_body if new_body is sparse
        existing_critique = []
        if matched_cand and existing_text:
            lines = existing_text.splitlines()
            cand_pat = rf"\b{re.escape(matched_cand)}\b"
            recording = False
            for line in lines:
                stripped = line.strip()
                if re.search(cand_pat, stripped, re.IGNORECASE):
                    recording = True
                    continue
                if recording:
                    if stripped.startswith("•") or stripped.startswith("-") or stripped.startswith("*") or stripped.startswith("#") or stripped.startswith(">>") or stripped.startswith("<details"):
                        recording = False
                    elif stripped:
                        existing_critique.append(stripped)

        # Convert any raw HTML <details><summary> tags in existing_text or new_body to clean human-readable >> syntax
        if "<details" in existing_text.lower():
            existing_text = re.sub(
                r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*(.*?)\s*</details>",
                r">> \1\n\2\n",
                existing_text,
                flags=re.DOTALL | re.IGNORECASE,
            ).strip()

        formatted_entry = (new_body or "").strip()
        if "<details" in formatted_entry.lower():
            formatted_entry = re.sub(
                r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*(.*?)\s*</details>",
                r">> \1\n\2\n",
                formatted_entry,
                flags=re.DOTALL | re.IGNORECASE,
            ).strip()

        # 3. Format entry / toggle using clean Notion-style >> syntax
        already_has_toggle = (
            formatted_entry.startswith(">>")
            or "\n>>" in f"\n{formatted_entry}"
            or formatted_entry.startswith("->")
            or "\n->" in f"\n{formatted_entry}"
        )

        if wants_toggle and not already_has_toggle:
            summary_title = first_line_clean or matched_cand or (candidate_titles[0] if candidate_titles else "Notes")
            if raw_new_lines and (raw_new_lines[0].startswith("•") or raw_new_lines[0].startswith("-") or raw_new_lines[0].startswith("*")):
                summary_title = re.sub(r"^[•\-*]\s*", "", raw_new_lines[0]).strip()
                body_content = "\n\n".join(raw_new_lines[1:]).strip()
            elif raw_new_lines and any(cand.lower() in raw_new_lines[0].lower() for cand in candidate_titles):
                summary_title = raw_new_lines[0].strip()
                body_content = "\n\n".join(raw_new_lines[1:]).strip()
            else:
                body_content = formatted_entry

            if not body_content and existing_critique:
                body_content = "\n\n".join(existing_critique)

            if not body_content:
                body_content = formatted_entry or "Personal critique"

            formatted_entry = f">> {summary_title}\n{body_content}\n"

        if wants_raw:
            if formatted_entry.startswith(">>") or formatted_entry.startswith("->"):
                fe_lines = formatted_entry.splitlines()
                if len(fe_lines) > 1:
                    formatted_entry = "\n".join(fe_lines[1:]).strip()
                else:
                    formatted_entry = re.sub(r"^(?:>>|->)\s*", "", formatted_entry).strip()

        if not existing_text:
            return formatted_entry

        if not formatted_entry:
            return existing_text

        if not matched_cand:
            if mode == "append":
                return f"{existing_text}\n\n{formatted_entry}" if formatted_entry else existing_text
            return formatted_entry if formatted_entry else existing_text

        # 4. In-place upsert and deduplication
        lines = existing_text.splitlines()
        cand_pattern = rf"\b{re.escape(matched_cand)}\b"

        target_entry_idx = None
        for idx, line in enumerate(lines):
            stripped = line.strip()
            is_entry_start = (
                stripped.startswith("•")
                or stripped.startswith("-")
                or stripped.startswith("*")
                or stripped.startswith(">>")
                or stripped.startswith("->")
                or stripped.startswith("▶")
                or stripped.startswith("▸")
                or stripped.startswith("#")
                or bool(re.match(r"^\d+\.\s+", stripped))
            )
            if is_entry_start and re.search(cand_pattern, stripped, re.IGNORECASE):
                target_entry_idx = idx
                if wants_toggle and formatted_entry.startswith(">> ") and (stripped.startswith("•") or stripped.startswith("-") or stripped.startswith("*")):
                    rich_summary = re.sub(r"^[•\-*]\s*", "", stripped).strip()
                    lines_f = formatted_entry.splitlines()
                    body_rest = "\n".join(lines_f[1:])
                    formatted_entry = f">> {rich_summary}\n{body_rest}\n"
                break

        if target_entry_idx is not None:
            new_lines = []
            replaced = False
            skip_following_critique = False

            for idx, line in enumerate(lines):
                stripped = line.strip()

                if idx == target_entry_idx:
                    new_lines.append(formatted_entry.rstrip())
                    new_lines.append("")
                    new_lines.append("")
                    replaced = True
                    skip_following_critique = True
                    continue

                if re.search(cand_pattern, stripped, re.IGNORECASE) and replaced:
                    skip_following_critique = True
                    continue

                if skip_following_critique:
                    is_next_item = (
                        stripped.startswith("•")
                        or stripped.startswith("-")
                        or stripped.startswith("*")
                        or stripped.startswith(">>")
                        or stripped.startswith("->")
                        or stripped.startswith("▶")
                        or stripped.startswith("▸")
                        or stripped.startswith("#")
                        or stripped.startswith("<details")
                        or bool(re.match(r"^\d+\.\s+", stripped))
                    )
                    if is_next_item:
                        skip_following_critique = False
                        new_lines.append(line)
                    elif not stripped:
                        continue
                    else:
                        continue
                else:
                    new_lines.append(line)

            cleaned_result = "\n".join(new_lines)
            cleaned_result = re.sub(r"\n{3,}", "\n\n", cleaned_result).strip()
            return cleaned_result

        if mode == "append":
            return f"{existing_text}\n\n{formatted_entry}" if formatted_entry else existing_text
        return formatted_entry if formatted_entry else existing_text

    def chat(
        self,
        message: str,
        current_view: str = "library",
        inspected_movie_id: int | None = None,
        inspected_note: dict[str, Any] | None = None,
        related_movies: list[dict[str, Any]] | None = None,
        active_filters: dict[str, Any] | None = None,
        active_person: dict[str, Any] | None = None,
        visible_movies: list[dict[str, Any]] | None = None,
        notes_shelf_filter: str | None = None,
        live_movie_notes: str | None = None,
        history: list[dict[str, str]] | None = None,
        model_mode: str = "auto",
        active_skill_key: str | None = None,
    ) -> dict[str, Any]:
        if not self.api_key:
            return {
                "text": "Gemini API key is not configured in .env. Please set GEMINI_API_KEY to start chatting with Grey.",
                "action": None,
                "pills": [],
                "model_used": "Offline",
            }

        # Semantic query routing
        lower_msg = message.lower()
        research_triggers = [
            "rotten tomatoes", "imdb", "imbd", "metacritic", "rt score", "tomatometer", "rating", "ratings",
            "critical reception", "box office", "review", "reviews", "analysis", "critique",
            "thematic", "cinematography", "director", "essay", "compare", "breakdown",
            "trivia", "behind the scenes", "awards", "oscar", "deep dive"
        ]
        is_research = any(t in lower_msg for t in research_triggers)

        if model_mode == "pro":
            target_model = DEFAULT_PRO_MODEL
            model_label = "Gemini Pro"
        elif model_mode == "flash":
            target_model = DEFAULT_FLASH_MODEL
            model_label = "Gemini 3.8 Flash"
        else:
            # Auto routing
            if is_research:
                target_model = DEFAULT_PRO_MODEL
                model_label = "Gemini Pro (Research)"
            else:
                target_model = DEFAULT_FLASH_MODEL
                model_label = "Gemini 3.8 Flash"

        # Slash Command & Skill Routing
        active_skill_key = active_skill_key or None
        user_query = message.strip()

        # 1. Direct slash command match
        if user_query.startswith("/"):
            cmd_token = user_query.split()[0].lower()
            for k, s in SKILLS_REGISTRY.items():
                if cmd_token in (s["command"], f"/{k}"):
                    active_skill_key = k
                    user_query = user_query[len(cmd_token):].strip()
                    break

        # 2. Natural language skill match fallback
        if not active_skill_key:
            lq = user_query.lower()
            if any(p in lq for p in ["related movie", "related titles", "worth my attention", "worth my time", "any of these good", "which related"]):
                active_skill_key = "related"
            elif any(p in lq for p in ["add the yes movies", "add all yes", "batch add", "batch move"]):
                active_skill_key = "batch"
            elif any(p in lq for p in ["save this chat", "save this conversation", "save as research", "save research", "add to my research", "add this to research", "append to research", "research session", "research index", "show research index", "what research do i have"]):
                active_skill_key = "research"

        active_skill = SKILLS_REGISTRY.get(active_skill_key) if active_skill_key else None
        if active_skill and not user_query:
            user_query = active_skill.get("default_query", user_query)

        # Targeted dossier loading: skip heavy queries when the active skill doesn't need them
        if active_skill and not active_skill.get("requires_dossier", True):
            dossier = {
                "high_rated": [],
                "watchlist": [],
                "discarded_count": 0,
                "discarded_samples": [],
                "journal_digest": [],
                "journal_notes_list": [],
                "all_watched_titles": [],
                "rewatch_list": [],
                "all_excluded_titles": [],
            }
        else:
            dossier = self.get_taste_dossier()

        # Inspected movie info or detected mentioned movie in message
        inspected_info = "None"
        inspected_title = None
        try:
            with self._get_connection() as conn:
                if inspected_movie_id:
                    row = conn.execute(
                        """
                        SELECT m.title, m.release_date, m.overview, m.vote_average, u.status, u.verdict, u.notes
                        FROM movies m
                        LEFT JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                        WHERE m.tmdb_id = ?
                        """,
                        (inspected_movie_id,),
                    ).fetchone()
                    if row:
                        inspected_title = row['title']
                        year_str = f" ({(row['release_date'] or '')[:4]})" if row['release_date'] else ""
                        effective_notes = (live_movie_notes.strip() if live_movie_notes and live_movie_notes.strip() else None) or row['notes']
                        inspected_info = f"{row['title']}{year_str} (TMDB ID: {inspected_movie_id}), TMDB Rating {row['vote_average']} | Status: {row['status'] or 'unseen'} | User Verdict: {row['verdict'] or 'None'} | User Notes: {effective_notes or 'None'} | Overview: {row['overview'][:200]}..."
                else:
                    # Search if user mentioned a specific movie title in their message
                    rows = conn.execute(
                        """
                        SELECT m.tmdb_id, m.title, m.release_date, m.overview, m.vote_average, u.status, u.verdict, u.notes
                        FROM movies m
                        LEFT JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                        WHERE u.status IS NOT NULL
                        ORDER BY (u.notes IS NOT NULL AND trim(u.notes) != '') DESC, u.updated_at DESC
                        LIMIT 200
                        """
                    ).fetchall()
                    msg_words = [w for w in re.findall(r"\b[a-zA-Z0-9]{4,}\b", lower_msg) if w not in ("find", "movie", "notes", "note", "from", "library", "then", "this", "that", "with", "have")]
                    for r in rows:
                        t = (r["title"] or "").lower().strip()
                        t_norm = re.sub(r"^(?:the|a|an)\s+", "", t).strip()
                        t_stem = t_norm.rstrip("s")
                        matched = False
                        if len(t) >= 3 and t in lower_msg:
                            matched = True
                        elif len(t_norm) >= 3 and t_norm in lower_msg:
                            matched = True
                        elif len(t_stem) >= 4 and t_stem in lower_msg:
                            matched = True
                        elif any(w == t or w == t_norm or w == t_stem or (len(w) >= 4 and w in t_norm) for w in msg_words):
                            matched = True

                        if matched:
                            inspected_movie_id = r['tmdb_id']
                            inspected_title = r['title']
                            year_str = f" ({(r['release_date'] or '')[:4]})" if r['release_date'] else ""
                            inspected_info = f"{r['title']}{year_str} (TMDB ID: {inspected_movie_id}), TMDB Rating {r['vote_average']} | Status: {r['status']} | User Verdict: {r['verdict'] or 'None'} | User Notes: {r['notes'] or 'None'} | Overview: {r['overview'][:200]}..."
                            break

                # Frugal on-demand journal excerpt: fetch full text only if asked or relevant
                relevant_journal_excerpt = "None"
                wants_journal = any(w in lower_msg for w in ["my blog", "my essay", "my note", "my journal", "my writing", "what did i write", "based on my"])
                j_entries = conn.execute(
                    """
                    SELECT title, body FROM general_entries
                    WHERE is_deleted = 0 AND is_archived = 0 AND status = 'published'
                    ORDER BY updated_at DESC
                    LIMIT 15
                    """
                ).fetchall()
                for er in j_entries:
                    et = er["title"].lower()
                    if (wants_journal and (et in lower_msg or any(word in lower_msg for word in et.split() if len(word) > 4))) or (inspected_title and inspected_title.lower() in et):
                        body_preview = (er["body"] or "")[:700]
                        relevant_journal_excerpt = f"Title: {er['title']}\nExcerpt: {body_preview}"
                        break
        except Exception:
            pass

        inspected_note_info = "None"
        inspected_note_title = None
        inspected_note_id = None
        if inspected_note and isinstance(inspected_note, dict):
            inspected_note_id = inspected_note.get("id")
            inspected_note_title = inspected_note.get("title", "Current Note")
            nbody = inspected_note.get("body", "")
            nstatus = inspected_note.get("status", "note")
            ntags = inspected_note.get("tags", [])
            tag_str = f" | Tags: {', '.join(ntags)}" if ntags else ""
            id_str = f" (ID: {inspected_note_id})" if inspected_note_id else ""
            inspected_note_info = f"Title: {inspected_note_title}{id_str} (Status: {nstatus}{tag_str})\nContent:\n{nbody[:25000]}"
        elif not inspected_note_id:
            try:
                with self._get_connection() as conn:
                    matched_rows = conn.execute(
                        "SELECT entry_id, title, body, status FROM general_entries WHERE is_deleted = 0 AND is_archived = 0 ORDER BY updated_at DESC LIMIT 50"
                    ).fetchall()
                    for mr in matched_rows:
                        m_title = (mr["title"] or "").lower()
                        if len(m_title) > 2 and (m_title in lower_msg or any(word in lower_msg for word in m_title.split() if len(word) > 4)):
                            inspected_note_id = mr["entry_id"]
                            inspected_note_title = mr["title"]
                            nbody = mr["body"] or ""
                            nstatus = mr["status"] or "published"
                            inspected_note_info = f"Title: {inspected_note_title} (ID: {inspected_note_id}) (Status: {nstatus})\nContent:\n{nbody[:25000]}"
                            break
            except Exception:
                pass

        # Format related movies list for inspected movie
        related_movies_str = "None"
        if related_movies and isinstance(related_movies, list):
            items = []
            for rm in related_movies[:12]:
                t = rm.get("title") or rm.get("original_title") or "Unknown"
                yr = f" ({rm['year']})" if rm.get("year") else ""
                rt = f", TMDB {rm['rating']}" if rm.get("rating") else ""
                st = rm.get("status") or "unseen"
                vd = f", User Verdict {rm['verdict']}/10" if rm.get("verdict") else ""
                mid = rm.get("id") or rm.get("tmdb_id") or ""
                id_str = f" [ID: {mid}]" if mid else ""
                items.append(f"- {t}{yr}{id_str}: Status: {st}{rt}{vd}")
            if items:
                related_movies_str = "\n".join(items)
        elif inspected_movie_id:
            try:
                from app.movie_service import MovieService
                movie_svc = MovieService()
                rel_data = movie_svc.get_related_movies(inspected_movie_id, limit=12, include_previously_watched=True)
                results = rel_data.get("results") or []
                items = []
                for rm in results[:12]:
                    t = rm.get("title") or rm.get("original_title") or "Unknown"
                    yr = f" ({(rm.get('release_date') or '')[:4]})" if rm.get("release_date") else ""
                    rt = f", TMDB {rm.get('vote_average')}" if rm.get("vote_average") else ""
                    st = (rm.get("user_data") or {}).get("status") or "unseen"
                    vd = f", User Verdict {rm.get('user_data', {}).get('verdict')}/10" if (rm.get("user_data") or {}).get("verdict") else ""
                    mid = rm.get("tmdb_id") or ""
                    id_str = f" [ID: {mid}]" if mid else ""
                    items.append(f"- {t}{yr}{id_str}: Status: {st}{rt}{vd}")
                if items:
                    related_movies_str = "\n".join(items)
            except Exception:
                pass

        active_person_info = "None"
        if active_person and isinstance(active_person, dict):
            p_name = active_person.get("name") or "Unknown"
            p_dept = active_person.get("known_for_department") or active_person.get("department") or ""
            p_id = active_person.get("id") or active_person.get("tmdb_person_id") or ""
            active_person_info = f"{p_name} ({p_dept}) [TMDB Person ID: {p_id}]"

        visible_movies_str = "None"
        if visible_movies and isinstance(visible_movies, list) and len(visible_movies) > 0:
            v_items = []
            for vm in visible_movies[:20]:
                t = vm.get("title") or vm.get("original_title") or "Unknown"
                yr = f" ({vm['year']})" if vm.get("year") else ""
                rt = f", TMDB {vm['rating']}" if vm.get("rating") else ""
                st = vm.get("status") or "unseen"
                vd = f", Verdict {vm['verdict']}/10" if vm.get("verdict") else ""
                vmid = vm.get("id") or vm.get("tmdb_id") or ""
                id_str = f" [ID: {vmid}]" if vmid else ""
                v_items.append(f"- {t}{yr}{id_str}: Status: {st}{rt}{vd}")
            if v_items:
                visible_movies_str = "\n".join(v_items)

        # Modular Prompt Architecture: Load grey_core.md and dynamically route to the active skill
        prompts_dir = os.path.join(os.path.dirname(__file__), "prompts")
        core_prompt_path = os.path.join(prompts_dir, "grey_core.md")
        system_template = ""
        if os.path.exists(core_prompt_path):
            try:
                with open(core_prompt_path, "r", encoding="utf-8") as f:
                    system_template = f.read()
            except Exception as e:
                logger.warning(f"Could not read core prompt file {core_prompt_path}: {e}")

        # Fallback to monolithic prompt if core is missing
        if not system_template:
            monolith_path = os.path.join(prompts_dir, "grey_system_prompt.md")
            if os.path.exists(monolith_path):
                try:
                    with open(monolith_path, "r", encoding="utf-8") as f:
                        system_template = f.read()
                except Exception as e:
                    logger.warning(f"Could not read fallback prompt {monolith_path}: {e}")

        if not system_template:
            system_template = """You are Grey, the native cinema curator and personal film archivist for the NOPE (Movie Excluder) library.
ACTIVE MOVIE SCREEN FOCUS: {{INSPECTED_INFO}}
Related movies on screen:
{{RELATED_MOVIES_LIST}}
ACTIVE NOTE SCREEN FOCUS: {{INSPECTED_NOTE_INFO}}
User high-rated: {{FAVORITES_JSON}}
Watchlist: {{WATCHLIST_JSON}}
Discarded: {{DISCARDED_COUNT}}
Screen context: {{CURRENT_VIEW}}
Active person on screen: {{ACTIVE_PERSON_INFO}}
Visible movies on screen:
{{VISIBLE_MOVIES_LIST}}
Active filters: {{ACTIVE_FILTERS_JSON}}
"""

        # Dynamic Skill Module Routing
        active_rf_stems = [f.stem.lower() for f in self.research_dir.glob("*.md")] if self.research_dir.exists() else []
        last_turn_text = (history[-1].get("text") or "").lower() if history else ""
        is_research_followup = any(w in lower_msg for w in ["try again", "what about", "tell me more", "show it", "what is in", "what's in", "read", "check again"]) and any(stem in last_turn_text for stem in active_rf_stems)

        skill_filename = "library_ops.md"
        if active_skill_key == "related":
            skill_filename = "related_curator.md"
        elif active_skill_key == "watchlist":
            skill_filename = "watchlist_builder.md"
        elif active_skill_key == "batch":
            skill_filename = "library_ops.md"
        elif active_skill_key == "research":
            skill_filename = "research_partner.md"
        elif any(w in lower_msg for w in [
            "research file", "research files", "save this chat", "save as research",
            "save to research", "create research", "new research", "research session",
            "research index", "add to my research", "append to research", "what research do i have"
        ]) or any(stem in lower_msg for stem in active_rf_stems if len(stem) >= 4) or is_research_followup:
            skill_filename = "research_partner.md"
        elif (
            current_view in ("movie-notes", "notes")
            or inspected_note_id
            or any(w in lower_msg for w in ["note", "draft", "journal", "post", "essay", "blog", "write-up", "entry"])
        ):
            skill_filename = "notes_editor.md"
        elif (
            current_view == "filmography"
            or (active_person and isinstance(active_person, dict) and active_person.get("name"))
        ):
            skill_filename = "filmography_explorer.md"
        elif any(w in lower_msg for w in ["related", "similar to this", "worth my attention", "recommend from these"]):
            skill_filename = "related_curator.md"
        else:
            skill_filename = "library_ops.md"

        skill_directive_text = active_skill["directive"] if active_skill else ""
        skill_file_path = os.path.join(prompts_dir, "skills", skill_filename)
        if os.path.exists(skill_file_path):
            try:
                with open(skill_file_path, "r", encoding="utf-8") as sf:
                    file_skill_text = sf.read().strip()
                    if skill_directive_text:
                        skill_directive_text = f"{skill_directive_text}\n\n{file_skill_text}"
                    else:
                        skill_directive_text = file_skill_text
            except Exception as e:
                logger.warning(f"Could not read skill file {skill_file_path}: {e}")

        if not skill_directive_text:
            skill_directive_text = "None"

        research_files_index_str = self.get_research_files_index()
        reactions_index_str = self.get_reactions_index()

        system_instruction = (
            system_template
            .replace("{{ACTIVE_SKILL_DIRECTIVE}}", skill_directive_text)
            .replace("{{INSPECTED_INFO}}", inspected_info)
            .replace("{{INSPECTED_TITLE}}", inspected_title or "None")
            .replace("{{INSPECTED_MOVIE_TMDB_ID}}", str(inspected_movie_id or "None"))
            .replace("{{RELATED_MOVIES_LIST}}", related_movies_str)
            .replace("{{INSPECTED_NOTE_INFO}}", inspected_note_info)
            .replace("{{INSPECTED_NOTE_TITLE}}", inspected_note_title or "None")
            .replace("{{INSPECTED_NOTE_ID}}", str(inspected_note_id or "None"))
            .replace("{{ACTIVE_PERSON_INFO}}", active_person_info)
            .replace("{{VISIBLE_MOVIES_LIST}}", visible_movies_str)
            .replace("{{RESEARCH_FILES_INDEX}}", research_files_index_str)
            .replace("{{AVAILABLE_REACTIONS}}", reactions_index_str)
            .replace("{{FAVORITES_JSON}}", json.dumps(dossier["high_rated"][:8]))
            .replace("{{WATCHLIST_JSON}}", json.dumps(dossier["watchlist"][:16]))
            .replace("{{DISCARDED_COUNT}}", str(dossier["discarded_count"]))
            .replace("{{DISCARDED_SAMPLES_JSON}}", json.dumps(dossier["discarded_samples"][:6]))
            .replace("{{JOURNAL_DIGEST}}", json.dumps(dossier.get("journal_digest", [])))
            .replace("{{JOURNAL_NOTES_LIST}}", json.dumps(dossier.get("journal_notes_list", [])))
            .replace("{{RELEVANT_JOURNAL_EXCERPT}}", relevant_journal_excerpt)
            .replace("{{ALL_WATCHED_TITLES}}", ", ".join(dossier.get("all_watched_titles", [])) or "None")
            .replace("{{REWATCH_LIST}}", ", ".join(dossier.get("rewatch_list", [])) or "None")
            .replace("{{ALL_EXCLUDED_TITLES}}", ", ".join(dossier.get("all_excluded_titles", [])) or "None")
            .replace("{{CURRENT_VIEW}}", current_view)
            .replace("{{ACTIVE_FILTERS_JSON}}", json.dumps(active_filters or {}))
        )

        contents = []
        if history:
            for item in history[-16:]:
                role = "user" if item.get("role") == "user" else "model"
                contents.append({"role": role, "parts": [{"text": item.get("text", "")}]})

        screen_contexts = []
        if active_person_info != "None":
            screen_contexts.append(f"Filmography on screen: {active_person_info}")
        if visible_movies and isinstance(visible_movies, list) and len(visible_movies) > 0:
            titles_sample = [vm.get("title") or vm.get("original_title") for vm in visible_movies[:8] if (vm.get("title") or vm.get("original_title"))]
            if titles_sample:
                screen_contexts.append(f"Grid shows {len(visible_movies)} titles including: {', '.join(titles_sample)}")
        if notes_shelf_filter:
            screen_contexts.append(f"Movie Notes paired shelf filter: {notes_shelf_filter}")
        if inspected_title:
            id_info = f" (TMDB ID: {inspected_movie_id})" if inspected_movie_id else ""
            screen_contexts.append(f"Currently viewing movie on screen: {inspected_title}{id_info}")
            if live_movie_notes and live_movie_notes.strip():
                screen_contexts.append(f"Active movie Personal Memory on screen: {live_movie_notes.strip()[:300]}")
        if inspected_note_title:
            screen_contexts.append(f"Currently viewing note on screen: {inspected_note_title}")

        prefix = f"[{' | '.join(screen_contexts)}]\n" if screen_contexts else ""
        user_content = f"{prefix}{user_query}"
        contents.append({"role": "user", "parts": [{"text": user_content}]})

        payload = {
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "contents": contents,
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.35,
            },
        }

        def call_gemini(model_name: str):
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            return requests.post(endpoint, json=payload, headers={"Content-Type": "application/json"}, timeout=60)

        if "pro" in target_model.lower():
            candidate_models = list(dict.fromkeys([
                target_model,
                "gemini-3.1-pro-preview",
                "gemini-pro-latest",
                "gemini-3.5-flash",
                "gemini-3.8-flash",
                "gemini-3.7-flash",
                "gemini-3.5-flash-lite",
                "gemini-flash-lite-latest",
            ]))
        else:
            candidate_models = list(dict.fromkeys([
                target_model,
                "gemini-3.5-flash",
                "gemini-3.8-flash",
                "gemini-3.7-flash",
                "gemini-3.5-flash-lite",
                "gemini-3.1-flash-lite",
                "gemini-flash-latest",
                "gemini-flash-lite-latest",
            ]))

        try:
            resp = None
            for model_candidate in candidate_models:
                try:
                    resp = call_gemini(model_candidate)
                    if resp.status_code == 200:
                        model_label = f"Gemini {model_candidate.replace('gemini-', '').capitalize()}"
                        break
                    logger.info(f"Model {model_candidate} returned {resp.status_code}, trying next in cascade...")
                except requests.exceptions.Timeout:
                    logger.warning(f"Model {model_candidate} timed out, trying next in cascade...")
                    continue
                except requests.exceptions.RequestException as req_err:
                    logger.warning(f"Model {model_candidate} request error: {req_err}, trying next in cascade...")
                    continue

            if not resp or resp.status_code != 200:
                logger.error(f"All Gemini models exhausted. Last error: {resp.status_code if resp else 'None'}")
                return {
                    "text": "I ran into a temporary connection issue reaching the Gemini engine. Please try your request again in a moment.",
                    "action": None,
                    "pills": [],
                    "model_used": "Offline",
                }

            candidates = resp.json().get("candidates", [])
            raw_text = ""
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                for part in parts:
                    if isinstance(part, dict) and "text" in part and part["text"]:
                        raw_text = part["text"]
                        break

            clean_str = raw_text.strip()
            if clean_str.startswith("```"):
                lines = clean_str.splitlines()
                if len(lines) >= 2 and lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                clean_str = "\n".join(lines).strip()

            data = None
            if clean_str:
                try:
                    data = json.loads(clean_str)
                except Exception:
                    start_idx = clean_str.find("{")
                    end_idx = clean_str.rfind("}")
                    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                        try:
                            data = json.loads(clean_str[start_idx:end_idx + 1])
                        except Exception:
                            data = None

            if not isinstance(data, dict):
                data = {
                    "text": clean_str or "I've reviewed your request and library.",
                    "action": None,
                    "pills": [],
                }

            action = data.get("action")
            pills = data.get("pills", [])

            # Status normalization map for movie library shelves
            status_map = {
                "new_discovery": "new_discovery",
                "discovery": "new_discovery",
                "new discovery": "new_discovery",
                "watch_later": "watch_later",
                "watchlist": "watch_later",
                "watch later": "watch_later",
                "watched": "watched",
                "seen": "watched",
                "rewatch": "rewatch",
                "excluded": "excluded",
                "nope": "excluded",
                "noped": "excluded",
                "reject": "excluded",
            }

            # If the model returned an 'actions' list with multiple movie status changes, synthesize batch_set_movie_status
            if isinstance(data.get("actions"), list) and data["actions"]:
                status_actions = [a for a in data["actions"] if isinstance(a, dict) and a.get("type") == "set_movie_status"]
                if len(status_actions) > 1 and not (action and action.get("type") == "batch_set_movie_status"):
                    first_status = status_actions[0].get("params", {}).get("status")
                    action = {
                        "type": "batch_set_movie_status",
                        "params": {
                            "status": first_status,
                            "movies": [a.get("params", {}) for a in status_actions],
                        }
                    }
                elif len(status_actions) == 1 and not action:
                    action = status_actions[0]

            is_post_mention = any(w in lower_msg for w in ["post", "note", "journal", "entry", "draft", "blog", "write-up"])

            if action and action.get("type") == "create_draft":
                try:
                    from app.general_entry_repository import GeneralEntryRepository
                    repo = GeneralEntryRepository()
                    params = action.get("params") or {}
                    draft_title = params.get("title", "Untitled Draft").strip() or "Untitled Draft"
                    draft_body = params.get("body", "")
                    raw_tags = params.get("tags", [])
                    if isinstance(raw_tags, str):
                        draft_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
                    elif isinstance(raw_tags, list):
                        draft_tags = [str(t).strip() for t in raw_tags if str(t).strip()]
                    else:
                        draft_tags = []

                    created = repo.create_entry(
                        entry_type="note",
                        title=draft_title,
                        body=draft_body,
                        tags=draft_tags,
                        status="draft",
                    )
                    draft_id = created["entry_id"]
                    if not isinstance(action.get("params"), dict):
                        action["params"] = {}
                    action["params"]["entry_id"] = draft_id

                    open_pill_found = False
                    for p in pills:
                        if p.get("action") == "open_entry":
                            p["payload"] = {"entry_id": draft_id}
                            open_pill_found = True
                            break
                    if not open_pill_found:
                        pills.insert(0, {
                            "label": f"📖 Open Draft: {draft_title[:24]}",
                            "action": "open_entry",
                            "payload": {"entry_id": draft_id},
                        })
                except Exception as draft_err:
                    logger.error(f"Failed to auto-create draft entry: {draft_err}")

            elif action and action.get("type") == "batch_set_movie_status":
                try:
                    from app.movie_service import MovieService
                    from app.user_movie_repository import UserMovieRepository
                    movie_svc = MovieService()
                    user_repo = UserMovieRepository()
                    params = action.get("params") or {}
                    raw_st = params.get("status")
                    target_status = status_map.get(str(raw_st).lower().strip(), raw_st) if raw_st else None

                    raw_movies = params.get("movies") or params.get("tmdb_ids") or []
                    if not isinstance(raw_movies, list):
                        raw_movies = [raw_movies]

                    # Map of titles to IDs from related_movies if available
                    related_title_map = {}
                    if related_movies and isinstance(related_movies, list):
                        for rm in related_movies:
                            rtitle = (rm.get("title") or rm.get("original_title") or "").strip().lower()
                            rid = rm.get("id") or rm.get("tmdb_id")
                            if rtitle and rid:
                                related_title_map[rtitle] = int(rid)

                    updated_movies = []
                    preserved_movies = []
                    for item in raw_movies:
                        m_id = None
                        m_title = ""
                        m_verdict = None
                        m_notes = None

                        if isinstance(item, (int, str)) and str(item).isdigit():
                            m_id = int(item)
                        elif isinstance(item, dict):
                            raw_id = item.get("tmdb_id") or item.get("id")
                            if raw_id and str(raw_id).isdigit():
                                m_id = int(raw_id)
                            m_title = item.get("title") or item.get("name") or ""
                            m_verdict = item.get("verdict")
                            m_notes = item.get("notes")
                        elif isinstance(item, str):
                            m_title = item

                        # Resolve missing TMDB ID from related_movies or database
                        if not m_id and m_title:
                            clean_t = m_title.strip().lower()
                            clean_t_noyear = re.sub(r"\s*\(\d{4}\)$", "", clean_t).strip()
                            if clean_t in related_title_map:
                                m_id = related_title_map[clean_t]
                            elif clean_t_noyear in related_title_map:
                                m_id = related_title_map[clean_t_noyear]
                            else:
                                for rt, rid in related_title_map.items():
                                    if clean_t_noyear in rt or rt in clean_t_noyear:
                                        m_id = rid
                                        break

                            if not m_id:
                                with self._get_connection() as conn:
                                    row = conn.execute(
                                        "SELECT tmdb_id, title FROM movies WHERE lower(title) = lower(?) OR lower(title) = lower(?) LIMIT 1",
                                        (clean_t, clean_t_noyear)
                                    ).fetchone()
                                    if row:
                                        m_id = row["tmdb_id"]
                                        m_title = row["title"]

                        if m_id and target_status:
                            user_data = user_repo.get_user_movie_data(m_id)
                            current_status = user_data.get("status") if user_data else None

                            # Intelligent Protection: Only move to new_discovery if currently untracked!
                            # Never silently override or un-banish movies that are already watched, excluded (NOPE),
                            # rewatch, or watch_later without explicit instruction.
                            if target_status == "new_discovery" and current_status is not None:
                                preserved_movies.append({
                                    "tmdb_id": m_id,
                                    "title": m_title or f"Movie #{m_id}",
                                    "status": current_status,
                                })
                                continue

                            movie_svc.set_movie_status(m_id, target_status)
                            if m_verdict is not None:
                                try:
                                    v_int = int(m_verdict)
                                    if 1 <= v_int <= 10:
                                        movie_svc.set_movie_verdict(m_id, v_int)
                                except Exception:
                                    pass
                            if m_notes and isinstance(m_notes, str):
                                movie_svc.set_movie_notes(m_id, m_notes)
                            updated_movies.append({"tmdb_id": m_id, "title": m_title})

                    if not isinstance(action.get("params"), dict):
                        action["params"] = {}
                    action["params"]["movies"] = updated_movies
                    action["params"]["status"] = target_status

                    if preserved_movies:
                        preserved_notes = []
                        for pm in preserved_movies:
                            readable_status = pm["status"].replace("_", " ").upper()
                            preserved_notes.append(f"**{pm['title']}** (kept as {readable_status})")
                        preserved_msg = f"Preserved prior judgments: {', '.join(preserved_notes)}."
                        if data.get("text"):
                            data["text"] = f"{data['text']}\n\n{preserved_msg}"
                        else:
                            data["text"] = preserved_msg
                except Exception as batch_err:
                    logger.error(f"Failed to batch set movie status via Grey: {batch_err}")

            elif action and action.get("type") == "set_movie_status":
                is_post_mention = any(w in lower_msg for w in ["post", "note", "journal", "entry", "draft", "blog", "write-up"])
                if is_post_mention:
                    # User intended a note/post operation, not a library shelf status change!
                    logger.info("Intercepted set_movie_status with post/note mention; converting to update_entry.")
                    t_id = action.get("params", {}).get("tmdb_id") or inspected_movie_id
                    t_title = action.get("params", {}).get("title") or inspected_title or "Movie"
                    m_year = ""
                    m_overview = ""
                    cast_names = "Unknown"
                    if t_id:
                        with self._get_connection() as conn:
                            m_row = conn.execute("SELECT title, release_date, overview FROM movies WHERE tmdb_id = ?", (t_id,)).fetchone()
                            if m_row:
                                t_title = m_row["title"]
                                m_year = f" ({(m_row['release_date'] or '')[:4]})" if m_row["release_date"] else ""
                                m_overview = (m_row["overview"] or "").strip()
                            c_rows = conn.execute("SELECT name FROM movie_credits WHERE tmdb_id = ? AND credit_type = 'actor' ORDER BY position ASC LIMIT 3", (t_id,)).fetchall()
                            if c_rows:
                                cast_names = ", ".join(c["name"] for c in c_rows)

                    target_body_format = "toggle"
                    existing_body_sample = ""
                    if inspected_note_id:
                        with self._get_connection() as conn:
                            erow = conn.execute("SELECT body FROM general_entries WHERE entry_id = ?", (inspected_note_id,)).fetchone()
                            if erow and erow["body"]:
                                existing_body_sample = erow["body"].strip()
                    elif inspected_note and isinstance(inspected_note, dict):
                        existing_body_sample = (inspected_note.get("body") or "").strip()

                    bullet_char = "•"
                    has_imdb = "imdb" in existing_body_sample.lower()
                    if existing_body_sample:
                        lines = [l.strip() for l in existing_body_sample.splitlines() if l.strip()]
                        bullet_lines = [l for l in lines if l.startswith("•") or l.startswith("- ") or l.startswith("* ")]
                        if bullet_lines and ">>" not in existing_body_sample:
                            target_body_format = "bullet"
                            if bullet_lines[0].startswith("- "):
                                bullet_char = "-"
                            elif bullet_lines[0].startswith("* "):
                                bullet_char = "*"

                    if target_body_format == "bullet":
                        cast_part = f" ({cast_names})" if cast_names and cast_names != "Unknown" else ""
                        link_part = " - [IMDb](https://www.imdb.com/)" if has_imdb else ""
                        appended_body = f"{bullet_char} {t_title}{m_year}{cast_part}{link_part}"
                    else:
                        appended_body = (
                            f">> {t_title}{m_year}\n"
                            f"- **Cast:** {cast_names}\n"
                            f"- **Synopsis:** {m_overview[:180]}...\n"
                            f"- **Why YES:** Added to watchlist post."
                        )

                    action = {
                        "type": "update_entry",
                        "params": {
                            "title": None,
                            "body": appended_body,
                            "mode": "append",
                        }
                    }
                else:
                    try:
                        from app.movie_service import MovieService
                        movie_svc = MovieService()
                        params = action.get("params") or {}
                        param_tmdb_id = params.get("tmdb_id")
                        param_title = (params.get("title") or "").strip()
                        target_tmdb_id = None

                        if param_tmdb_id and str(param_tmdb_id).isdigit():
                            target_tmdb_id = int(param_tmdb_id)
                            # Only override with inspected_movie_id if user didn't explicitly target another film
                            if inspected_movie_id and not param_title and target_tmdb_id != inspected_movie_id:
                                target_tmdb_id = inspected_movie_id
                        elif inspected_movie_id and not param_title:
                            target_tmdb_id = inspected_movie_id
                        elif param_title:
                            clean_t = param_title.strip().lower()
                            clean_t_noyear = re.sub(r"\s*\(\d{4}\)$", "", clean_t).strip()
                            with self._get_connection() as conn:
                                row = conn.execute(
                                    "SELECT tmdb_id, title FROM movies WHERE lower(title) = lower(?) OR lower(title) = lower(?) LIMIT 1",
                                    (clean_t, clean_t_noyear)
                                ).fetchone()
                                if row:
                                    target_tmdb_id = row["tmdb_id"]
                        elif inspected_movie_id:
                            target_tmdb_id = inspected_movie_id

                        target_status = params.get("status")
                        target_verdict = params.get("verdict")
                        target_notes = params.get("notes")

                        if target_status:
                            raw_st = str(target_status).lower().strip()
                            target_status = status_map.get(raw_st, raw_st)

                        if target_tmdb_id and str(target_tmdb_id).isdigit():
                            target_tmdb_id = int(target_tmdb_id)
                            if target_status:
                                movie_svc.set_movie_status(target_tmdb_id, target_status)
                            if target_verdict is not None:
                                try:
                                    v_int = int(target_verdict)
                                    if 1 <= v_int <= 10:
                                        movie_svc.set_movie_verdict(target_tmdb_id, v_int)
                                except Exception:
                                    pass
                            if target_notes and isinstance(target_notes, str):
                                movie_svc.set_movie_notes(target_tmdb_id, target_notes)

                            if not isinstance(action.get("params"), dict):
                                action["params"] = {}
                            action["params"]["tmdb_id"] = target_tmdb_id
                            action["params"]["status"] = target_status
                    except Exception as status_err:
                        logger.error(f"Failed to set movie status via Grey: {status_err}")
                        data["text"] = f"I couldn't update the status for this movie due to an error: {status_err}"
                        action = None

            if action and action.get("type") == "update_entry":
                try:
                    from app.general_entry_repository import GeneralEntryRepository
                    repo = GeneralEntryRepository()
                    params = action.get("params") or {}
                    target_id = params.get("entry_id") or inspected_note_id
                    target_title = params.get("title") or inspected_note_title
                    mode = params.get("mode", "append")
                    new_body = params.get("body", "")

                    existing = None
                    if target_id and str(target_id).isdigit():
                        try:
                            existing = repo.get_entry(int(target_id))
                        except Exception:
                            existing = None

                    if not existing and target_title:
                        with self._get_connection() as conn:
                            row = conn.execute(
                                "SELECT entry_id FROM general_entries WHERE is_deleted = 0 AND lower(title) = lower(?) ORDER BY updated_at DESC LIMIT 1",
                                (str(target_title).strip(),)
                            ).fetchone()
                            if not row:
                                row = conn.execute(
                                    "SELECT entry_id FROM general_entries WHERE is_deleted = 0 AND lower(title) LIKE lower(?) ORDER BY updated_at DESC LIMIT 1",
                                    (f"%{str(target_title).strip()}%",)
                                ).fetchone()
                            if row:
                                existing = repo.get_entry(row["entry_id"])

                    # If not explicitly named, scan if the user query mentioned any existing note title
                    # Sort by length descending so specific titles like "Watchlist 1" match before "Watchlist"
                    if not existing:
                        with self._get_connection() as conn:
                            all_titles = conn.execute("SELECT entry_id, title FROM general_entries WHERE is_deleted = 0").fetchall()
                            sorted_titles = sorted(all_titles, key=lambda x: len(x["title"] or ""), reverse=True)
                            for at in sorted_titles:
                                if at["title"] and at["title"].strip().lower() in lower_msg:
                                    existing = repo.get_entry(at["entry_id"])
                                    break

                    # Regex extraction fallback for patterns like "add this to my [X] post"
                    if not existing:
                        cand_match = re.search(r"(?:add|save|append|put)\s+(?:this\s+)?(?:to\s+|into\s+)?(?:my\s+)?['\"]?([^'\"\n]+?)['\"]?\s+(?:post|note|journal|entry|blog|draft|list)", message, re.IGNORECASE)
                        if cand_match:
                            cand_title = cand_match.group(1).strip()
                            with self._get_connection() as conn:
                                row = conn.execute(
                                    "SELECT entry_id FROM general_entries WHERE is_deleted = 0 AND lower(title) = lower(?) ORDER BY updated_at DESC LIMIT 1",
                                    (cand_title,)
                                ).fetchone()
                                if not row:
                                    row = conn.execute(
                                        "SELECT entry_id FROM general_entries WHERE is_deleted = 0 AND lower(title) LIKE lower(?) ORDER BY updated_at DESC LIMIT 1",
                                        (f"%{cand_title}%",)
                                    ).fetchone()
                                if row:
                                    existing = repo.get_entry(row["entry_id"])

                    # The user must either have the note open on screen, OR explicitly request note modification in chat message
                    explicit_note_request = (
                        any(w in lower_msg for w in ["note", "draft", "journal", "essay", "blog", "write-up", "entry", "list", "post"])
                        or (bool(target_title) and str(target_title).strip().lower() in lower_msg)
                        or (bool(existing) and existing["title"].strip().lower() in lower_msg)
                    )

                    if not inspected_note_id and not explicit_note_request:
                        logger.warning("Rejected unprompted update_entry action: user did not request note modification.")
                        action = None
                    elif not existing:
                        action = None
                        data["text"] = f"I couldn't locate the note '{target_title or 'requested'}' in your notebook to update."
                    elif existing:
                        final_body = self._deduplicate_and_format_note_body(
                            existing_body=existing.get("body") or "",
                            new_body=new_body,
                            mode=mode,
                            user_message=message,
                            inspected_movie_id=inspected_movie_id,
                            inspected_movie_title=inspected_title,
                        )

                        raw_tags = params.get("tags")
                        if raw_tags is None:
                            tags_to_save = [t["name"] for t in existing.get("tags", [])]
                        elif isinstance(raw_tags, str):
                            tags_to_save = [t.strip() for t in raw_tags.split(",") if t.strip()]
                        elif isinstance(raw_tags, list):
                            tags_to_save = [str(t).strip() for t in raw_tags if str(t).strip()]
                        else:
                            tags_to_save = []

                        updated = repo.update_entry(
                            entry_id=existing["entry_id"],
                            entry_type=existing["entry_type"],
                            title=params.get("title") or existing["title"],
                            body=final_body,
                            url=existing.get("url"),
                            tags=tags_to_save,
                            status=existing["status"],
                        )
                        if updated:
                            if not isinstance(action.get("params"), dict):
                                action["params"] = {}
                            action["params"]["entry_id"] = updated["entry_id"]
                            action["params"]["title"] = updated["title"]
                            if is_post_mention and (not data.get("text") or "movie" in data.get("text", "").lower() or "status" in data.get("text", "").lower()):
                                data["text"] = f"Added to your '{updated['title']}' post."

                            open_pill_found = False
                            for p in pills:
                                if p.get("action") in ("open_entry", "open_note") or "open" in (p.get("label") or "").lower():
                                    p["action"] = "open_entry"
                                    p["payload"] = {"entry_id": updated["entry_id"], "title": updated["title"]}
                                    p["label"] = f"📖 Open {updated['title'][:24]}"
                                    open_pill_found = True
                                    break
                            if not open_pill_found:
                                pills.insert(0, {
                                    "label": f"📖 Open {updated['title'][:24]}",
                                    "action": "open_entry",
                                    "payload": {"entry_id": updated["entry_id"], "title": updated["title"]},
                                })
                except Exception as update_err:
                    logger.error(f"Failed to update entry: {update_err}")

            if action and action.get("type") == "save_research_file":
                try:
                    params = action.get("params") or {}
                    raw_fname = (params.get("filename") or params.get("title") or "research").strip()
                    if not raw_fname.endswith(".md"):
                        raw_fname += ".md"
                    clean_fname = re.sub(r"[^\w\.\-]", "_", raw_fname).lower()
                    if not clean_fname.endswith(".md"):
                        clean_fname += ".md"
                    file_path = self.research_dir / clean_fname
                    content = (params.get("content") or "").strip()
                    if not content and data.get("text"):
                        content = f"# {params.get('title') or clean_fname[:-3].replace('_', ' ').title()}\n\n{data['text']}"
                    file_path.write_text(content + "\n", encoding="utf-8")
                    if not isinstance(action.get("params"), dict):
                        action["params"] = {}
                    action["params"]["filename"] = clean_fname
                    action["params"]["filepath"] = str(file_path)
                except Exception as r_save_err:
                    logger.error(f"Failed to save research file: {r_save_err}")

            elif action and action.get("type") == "append_research_file":
                try:
                    params = action.get("params") or {}
                    target_query = params.get("filename") or params.get("title") or ""
                    entry_text = (params.get("entry") or params.get("text") or "").strip()
                    matched_file = self.resolve_research_file(target_query)
                    if not matched_file:
                        raw_fname = (target_query or "research.md").strip()
                        clean_fname = re.sub(r"[^\w\.\-]", "_", raw_fname).lower()
                        if not clean_fname.endswith(".md"):
                            clean_fname += ".md"
                        matched_file = self.research_dir / clean_fname
                        matched_file.write_text(f"# {target_query.replace('_', ' ').title()}\n\n", encoding="utf-8")

                    with open(matched_file, "a", encoding="utf-8") as af:
                        af.write(f"\n{entry_text}\n")

                    if not isinstance(action.get("params"), dict):
                        action["params"] = {}
                    action["params"]["filename"] = matched_file.name
                    action["params"]["filepath"] = str(matched_file)
                except Exception as r_app_err:
                    logger.error(f"Failed to append to research file: {r_app_err}")

            elif action and action.get("type") == "delete_research_file":
                try:
                    params = action.get("params") or {}
                    target_query = params.get("filename") or params.get("title") or ""
                    matched_file = self.resolve_research_file(target_query)
                    if matched_file and matched_file.exists():
                        matched_file.unlink()
                        if not isinstance(action.get("params"), dict):
                            action["params"] = {}
                        action["params"]["filename"] = matched_file.name
                except Exception as r_del_err:
                    logger.error(f"Failed to delete research file: {r_del_err}")

            reaction = data.get("reaction")
            valid_reaction = None
            if reaction and isinstance(reaction, str):
                reaction_filename = Path(reaction).name
                reaction_path = self.reactions_dir / reaction_filename
                if reaction_path.exists() and reaction_path.is_file():
                    valid_reaction = reaction_filename

            # Filter out unsolicited shelf categorization pills (e.g. "+ Add to Watchlist", "✨ New Discovery")
            sanitized_pills = []
            for p in (pills or []):
                if not isinstance(p, dict):
                    continue
                lbl = (p.get("label") or "").lower()
                act = p.get("action")
                payload_st = str((p.get("payload") or {}).get("status", "")).lower()
                is_status_pill = (
                    act == "set_movie_status"
                    or payload_st in ("watch_later", "new_discovery", "watched", "rewatch", "excluded")
                    or any(s in lbl for s in ["watchlist", "new discovery", "add to shelf", "mark as"])
                )
                if not is_status_pill:
                    sanitized_pills.append(p)
            pills = sanitized_pills

            return {
                "text": data.get("text", "Here are the matching titles from your library."),
                "action": action,
                "reaction": valid_reaction,
                "pills": pills,
                "model_used": model_label,
                "active_skill": active_skill_key,
                "active_skill_name": active_skill["name"] if active_skill else None,
            }
        except Exception as e:
            logger.error(f"Error calling Grey Gemini API: {e}")
            err_str = str(e)
            if "timed out" in err_str.lower() or "timeout" in err_str.lower():
                user_msg = "The request took longer than expected to complete. Please try your request again."
            else:
                user_msg = f"Grey encountered a temporary error: {e}"
            return {
                "text": user_msg,
                "action": None,
                "pills": [],
                "model_used": "Error",
            }
