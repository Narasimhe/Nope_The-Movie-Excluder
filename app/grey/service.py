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

from app.config import (
    DEFAULT_FLASH_MODEL,
    DEFAULT_PRO_MODEL,
    GEMINI_API_BASE_URL,
    GEMINI_FLASH_CANDIDATE_MODELS,
    GEMINI_PRO_CANDIDATE_MODELS,
)
from app.general_entry_repository import GeneralEntryRepository
from app.grey.note_formatter import deduplicate_and_format_note_body
from app.movie_service import MovieService
from app.user_movie_repository import UserMovieRepository

logger = logging.getLogger(__name__)

# Lightweight metadata registry only — 100% of prompt instructions live in app/grey/prompts/skills/*.md
SKILLS_REGISTRY: dict[str, dict[str, Any]] = {
    "related": {
        "command": "/related",
        "name": "Related Movies Reality Check",
        "description": "Evaluates related movies on screen with craft takes and YES/NOPE verdicts.",
        "requires_dossier": False,
        "skill_file": "related_curator.md",
        "default_query": "Are any of the related movies on screen worth my attention?",
    },
    "batch": {
        "command": "/batch",
        "name": "Batch Move / Queue",
        "description": "Applies library status changes to multiple movies simultaneously.",
        "requires_dossier": False,
        "skill_file": "library_ops.md",
        "default_query": "Add the approved YES movies to my New Discovery shelf.",
    },
    "research": {
        "command": "/research",
        "name": "Cinema Research Files",
        "description": "Manages focused 1-5 research markdown files in data/research/*.md.",
        "requires_dossier": True,
        "skill_file": "research_partner.md",
        "default_query": "What research files do I have on disk?",
    },
}

STATUS_NORMALIZATION_MAP: dict[str, str] = {
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

NOTE_WRITE_VERBS = (
    "add",
    "append",
    "put",
    "insert",
    "update",
    "edit",
    "modify",
    "rewrite",
    "replace",
    "format",
    "toggle",
    "collapse",
    "collapsible",
    "draft",
    "create",
    "save",
    "summarize",
    "table",
)


class GreyService:
    """AI Cinema Companion orchestrator with Two-Tier Progressive Context & RAM caching."""

    _file_cache: dict[str, tuple[float, str]] = {}

    def __init__(self, db_path: str = "data/movie_excluder.db"):
        self.db_path = db_path
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.prompts_dir = Path(__file__).resolve().parent / "prompts"
        self.research_dir = Path(__file__).resolve().parent.parent.parent / "data" / "research"
        self.research_dir.mkdir(parents=True, exist_ok=True)
        self.reactions_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "gifs_n_media"
        self.reactions_dir.mkdir(parents=True, exist_ok=True)
        self.reactions_file = Path(__file__).resolve().parent / "reactions.json"

        self.http_session = requests.Session()
        self._reactions_cache: tuple[float, float, str] | None = None
        self._dossier_cache: tuple[str, dict[str, Any]] | None = None

        # Preload static prompt templates into memory at initialization
        self._preload_prompts()

    def _read_cached_file(self, path: Path) -> str:
        """Read a prompt/config file with mtime-aware in-memory caching (0ms disk read when unchanged)."""
        if not path.exists():
            return ""
        try:
            mtime = path.stat().st_mtime
            key = str(path.resolve())
            cached = self._file_cache.get(key)
            if cached and cached[0] == mtime:
                return cached[1]
            content = path.read_text(encoding="utf-8")
            self._file_cache[key] = (mtime, content)
            return content
        except Exception as exc:
            logger.warning("Could not read cached file %s: %s", path, exc)
            return ""

    def _preload_prompts(self) -> None:
        """Warm the in-memory prompt cache on startup."""
        core_path = self.prompts_dir / "grey_core.md"
        self._read_cached_file(core_path)
        skills_dir = self.prompts_dir / "skills"
        if skills_dir.exists():
            for skill_file in skills_dir.glob("*.md"):
                self._read_cached_file(skill_file)

    def get_reactions_index(self) -> str:
        """Return formatted reaction GIF/sticker index, cached in memory by directory/file mtime."""
        if not self.reactions_dir.exists():
            return "No reaction media available."
        try:
            dir_mtime = self.reactions_dir.stat().st_mtime
            meta_mtime = self.reactions_file.stat().st_mtime if self.reactions_file.exists() else 0.0
            if (
                self._reactions_cache
                and self._reactions_cache[0] == dir_mtime
                and self._reactions_cache[1] == meta_mtime
            ):
                return self._reactions_cache[2]
        except Exception:
            dir_mtime, meta_mtime = 0.0, 0.0

        valid_exts = {".gif", ".webp", ".png", ".jpg", ".jpeg"}
        files = [
            f.name
            for f in self.reactions_dir.iterdir()
            if f.is_file() and f.suffix.lower() in valid_exts
        ]
        if not files:
            return "No reaction media available."

        metadata: dict[str, str] = {}
        raw_meta = self._read_cached_file(self.reactions_file)
        if raw_meta:
            try:
                metadata = json.loads(raw_meta)
            except Exception:
                metadata = {}

        items = []
        for f in sorted(files):
            if f in metadata and metadata[f]:
                items.append(f"- `{f}`: {metadata[f]}")
            else:
                inferred = re.sub(r"[_\-]+", " ", Path(f).stem).strip()
                items.append(f"- `{f}`: {inferred}")

        result = "\n".join(items)
        self._reactions_cache = (dir_mtime, meta_mtime, result)
        return result

    def get_research_files_summary(self) -> str:
        """Tier 1 lightweight 1-line filenames index for normal turns (prevents 15,000-char bloat)."""
        if not self.research_dir.exists():
            return "No research files on disk yet."
        files = sorted(
            self.research_dir.glob("*.md"),
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )[:5]
        if not files:
            return "No research files on disk yet."
        names = [f"`{f.name}` ({f.stat().st_size} bytes)" for f in files]
        return "Active files on disk: " + ", ".join(names) + " (use tool_call `read_research_file` to read contents)."

    def get_research_files_index(self) -> str:
        """Tier 2 full research markdown contents (loaded when /research or research files are active)."""
        if not self.research_dir.exists():
            return "No research files on disk yet."
        files = sorted(
            self.research_dir.glob("*.md"),
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )[:5]
        if not files:
            return "No research files on disk yet."
        items = []
        for f in files:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore").strip()
                size = f.stat().st_size
                if not content:
                    items.append(
                        f"### File: `{f.name}` (Empty, 0 bytes)\n*(File currently contains no text)*"
                    )
                else:
                    snippet = content[:3000] + (
                        "\n... [remaining text truncated]" if len(content) > 3000 else ""
                    )
                    items.append(f"### File: `{f.name}` ({size} bytes)\n```markdown\n{snippet}\n```")
            except Exception:
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

    def invalidate_dossier_cache(self) -> None:
        """Clear cached dossier after any status or note mutation."""
        self._dossier_cache = None

    def get_taste_dossier(self) -> dict[str, Any]:
        """Extract user taste dossier using 2 consolidated SQLite queries + RAM cache (down from 17 queries)."""
        favorites: list[dict[str, Any]] = []
        watchlist: list[dict[str, Any]] = []
        discarded_count = 0
        discarded_samples: list[dict[str, Any]] = []
        journal_digest: list[dict[str, Any]] = []
        journal_notes_list: list[dict[str, Any]] = []
        watched_titles: list[str] = []
        rewatch_list: list[str] = []
        excluded_titles: list[str] = []
        new_discovery_list: list[str] = []

        try:
            with self._get_connection() as conn:
                # Fast cache signature check across user_movie_data and general_entries
                sig_row = conn.execute(
                    """
                    SELECT
                        (SELECT COUNT(*) || ':' || COALESCE(MAX(updated_at), '') FROM user_movie_data) as u_sig,
                        (SELECT COUNT(*) || ':' || COALESCE(MAX(updated_at), '') FROM general_entries WHERE is_deleted = 0) as j_sig
                    """
                ).fetchone()
                cache_key = f"{self.db_path}|{sig_row['u_sig'] if sig_row else ''}|{sig_row['j_sig'] if sig_row else ''}"
                if self._dossier_cache and self._dossier_cache[0] == cache_key:
                    return self._dossier_cache[1]

                # Query 1: Single consolidated query for all tracked user movies (replaces 7 separate queries)
                movie_rows = conn.execute(
                    """
                    SELECT
                        u.tmdb_id,
                        u.status,
                        u.verdict,
                        u.is_favorite,
                        u.notes,
                        u.updated_at,
                        m.title,
                        m.release_date,
                        m.vote_average
                    FROM user_movie_data u
                    LEFT JOIN movies m ON m.tmdb_id = u.tmdb_id
                    ORDER BY u.updated_at DESC
                    """
                ).fetchall()

                fav_candidates = []
                wl_candidates = []
                excl_with_notes = []
                excl_without_notes = []

                for r in movie_rows:
                    title = r["title"]
                    year = (r["release_date"] or "")[:4]
                    status = r["status"]
                    verdict = r["verdict"]
                    is_fav = r["is_favorite"]
                    notes = r["notes"]
                    vote_avg = r["vote_average"] or 0.0

                    if title and ((verdict is not None and verdict >= 8) or is_fav == 1):
                        fav_candidates.append((verdict or 0, vote_avg, {
                            "title": title,
                            "year": year,
                            "verdict": verdict,
                            "notes": notes,
                        }))

                    if status == "watch_later" and title:
                        wl_candidates.append((vote_avg, {
                            "tmdb_id": r["tmdb_id"],
                            "title": title,
                            "year": year,
                            "rating": r["vote_average"],
                        }))
                    elif status == "watched" and title:
                        v_str = f" ({verdict}/10)" if verdict is not None else ""
                        watched_titles.append(f"{title}{v_str}")
                    elif status == "rewatch" and title:
                        v_str = f" ({verdict}/10)" if verdict is not None else ""
                        rewatch_list.append(f"{title}{v_str}")
                    elif status == "new_discovery" and title:
                        new_discovery_list.append(f"{title} ({year})" if year else title)
                    elif status == "excluded":
                        discarded_count += 1
                        if title:
                            excluded_titles.append(title)
                            sample_obj = {
                                "title": title,
                                "year": year,
                                "notes": notes if notes else None,
                            }
                            if notes and str(notes).strip():
                                excl_with_notes.append(sample_obj)
                            elif len(excl_without_notes) < 8:
                                excl_without_notes.append(sample_obj)

                fav_candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
                favorites = [x[2] for x in fav_candidates[:15]]

                wl_candidates.sort(key=lambda x: x[0], reverse=True)
                watchlist = [x[1] for x in wl_candidates[:20]]

                discarded_samples = (excl_with_notes + excl_without_notes)[:8]

                # Query 2: Single consolidated query for journal entries + tags (replaces 10 N+1 queries)
                j_rows = conn.execute(
                    """
                    SELECT
                        e.entry_id,
                        e.title,
                        e.status,
                        GROUP_CONCAT(t.name, '||') AS tag_names
                    FROM general_entries e
                    LEFT JOIN general_entry_tag_links l ON e.entry_id = l.entry_id
                    LEFT JOIN general_entry_tags t ON l.tag_id = t.tag_id
                    WHERE e.is_deleted = 0 AND e.is_archived = 0 AND e.status = 'published'
                    GROUP BY e.entry_id
                    ORDER BY e.updated_at DESC
                    LIMIT 50
                    """
                ).fetchall()

                for idx, jr in enumerate(j_rows):
                    journal_notes_list.append({
                        "entry_id": jr["entry_id"],
                        "title": jr["title"],
                        "status": jr["status"],
                    })
                    if idx < 8:
                        raw_tags = jr["tag_names"] or ""
                        tags = [t for t in raw_tags.split("||") if t]
                        journal_digest.append({
                            "title": jr["title"],
                            "tags": tags,
                        })

                result = {
                    "high_rated": favorites,
                    "watchlist": watchlist,
                    "discarded_count": discarded_count,
                    "discarded_samples": discarded_samples,
                    "journal_digest": journal_digest,
                    "journal_notes_list": journal_notes_list,
                    "all_watched_titles": watched_titles,
                    "rewatch_list": rewatch_list,
                    "all_excluded_titles": excluded_titles,
                    "new_discovery_list": new_discovery_list,
                }
                self._dossier_cache = (cache_key, result)
                return result
        except Exception as e:
            logger.warning(f"Error fetching taste dossier: {e}")

        return {
            "high_rated": favorites,
            "watchlist": watchlist,
            "discarded_count": discarded_count,
            "discarded_samples": discarded_samples,
            "journal_digest": journal_digest,
            "journal_notes_list": journal_notes_list,
            "all_watched_titles": watched_titles,
            "rewatch_list": rewatch_list,
            "all_excluded_titles": excluded_titles,
            "new_discovery_list": new_discovery_list,
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
        """Delegate note deduplication and formatting to app.grey.note_formatter."""
        return deduplicate_and_format_note_body(
            existing_body=existing_body,
            new_body=new_body,
            mode=mode,
            user_message=user_message,
            inspected_movie_id=inspected_movie_id,
            inspected_movie_title=inspected_movie_title,
            get_connection=self._get_connection,
        )

    def _select_target_model(self, lower_msg: str, model_mode: str) -> tuple[str, str]:
        """Select Gemini model without false-positive slowdowns on common words like 'rating' or 'review'."""
        research_triggers = [
            "rotten tomatoes",
            "metacritic",
            "rt score",
            "tomatometer",
            "critical reception",
            "box office",
            "thematic analysis",
            "cinematography breakdown",
            "film essay",
            "deep dive",
            "behind the scenes",
        ]
        is_research = any(t in lower_msg for t in research_triggers)

        if model_mode == "pro":
            return DEFAULT_PRO_MODEL, "Gemini Pro"
        if model_mode == "flash":
            return DEFAULT_FLASH_MODEL, "Gemini 3.8 Flash"
        if is_research:
            return DEFAULT_PRO_MODEL, "Gemini Pro (Research)"
        return DEFAULT_FLASH_MODEL, "Gemini 3.8 Flash"

    def _resolve_active_skill(
        self,
        message: str,
        current_view: str,
        inspected_note_id: Any,
        active_person: dict[str, Any] | None,
        active_skill_key: str | None,
        history: list[dict[str, str]] | None,
    ) -> tuple[str | None, dict[str, Any] | None, str, str, bool]:
        """Resolve slash commands and Tier 1/Tier 2 progressive skill instructions."""
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

        lq = user_query.lower()

        # 2. Natural language skill match fallback
        if not active_skill_key:
            if any(
                p in lq
                for p in [
                    "related movie",
                    "related titles",
                    "worth my attention",
                    "worth my time",
                    "any of these good",
                    "which related",
                ]
            ):
                active_skill_key = "related"
            elif any(
                p in lq for p in ["add the yes movies", "add all yes", "batch add", "batch move"]
            ):
                active_skill_key = "batch"
            elif any(
                p in lq
                for p in [
                    "save this chat",
                    "save this conversation",
                    "save as research",
                    "save research",
                    "add to my research",
                    "add this to research",
                    "append to research",
                    "research session",
                    "research index",
                    "show research index",
                    "what research do i have",
                ]
            ):
                active_skill_key = "research"

        active_skill = SKILLS_REGISTRY.get(active_skill_key) if active_skill_key else None
        if active_skill and not user_query:
            user_query = active_skill.get("default_query", user_query)

        active_rf_stems = (
            [f.stem.lower() for f in self.research_dir.glob("*.md")]
            if self.research_dir.exists()
            else []
        )
        last_turn_text = (history[-1].get("text") or "").lower() if history else ""
        is_research_followup = any(
            w in lq
            for w in [
                "try again",
                "what about",
                "tell me more",
                "show it",
                "what is in",
                "what's in",
                "read",
                "check again",
            ]
        ) and any(stem in last_turn_text for stem in active_rf_stems)

        wants_research_context = (
            active_skill_key == "research"
            or any(
                w in lq
                for w in [
                    "research file",
                    "research files",
                    "save this chat",
                    "save as research",
                    "save to research",
                    "create research",
                    "new research",
                    "research session",
                    "research index",
                    "add to my research",
                    "append to research",
                    "what research do i have",
                ]
            )
            or any(stem in lq for stem in active_rf_stems if len(stem) >= 4)
            or is_research_followup
        )

        has_note_write_intent = any(
            re.search(rf"\b{re.escape(v)}\b", lq)
            for v in (*NOTE_WRITE_VERBS, "help", "improve", "fix", "clean")
        )
        mentions_note_topic = (
            current_view in ("movie-notes", "notes")
            or bool(inspected_note_id)
            or any(
                w in lq
                for w in ["note", "draft", "journal", "post", "essay", "blog", "write-up", "entry"]
            )
        )

        # Determine primary skill file from active skill or active screen/intent
        skill_filename = None
        if active_skill and active_skill.get("skill_file"):
            skill_filename = active_skill["skill_file"]
        elif wants_research_context:
            skill_filename = "research_partner.md"
        elif mentions_note_topic:
            if has_note_write_intent:
                skill_filename = "notes_editor.md"
            else:
                skill_directive_text = (
                    "### ACTIVE SKILL: READ-ONLY NOTE DISCUSSION\n"
                    "- The user is reading or asking a question about a note.\n"
                    "- Use the note content in {{INSPECTED_NOTE_INFO}} (or call `get_note` via `tool_call` if not loaded on screen) to answer their question.\n"
                    "- STRICT READ-ONLY RULE: Do NOT modify the note and NEVER emit `update_entry` or `create_draft`."
                )
                return (
                    active_skill_key,
                    active_skill,
                    user_query,
                    skill_directive_text,
                    wants_research_context,
                )
        elif current_view == "filmography" or (
            active_person and isinstance(active_person, dict) and active_person.get("name")
        ):
            skill_filename = "filmography_explorer.md"
        elif any(
            w in lq
            for w in ["related", "similar to this", "worth my attention", "recommend from these"]
        ):
            skill_filename = "related_curator.md"
        else:
            skill_filename = "library_ops.md"

        skill_path = self.prompts_dir / "skills" / skill_filename
        skill_directive_text = self._read_cached_file(skill_path).strip() or "None"

        return active_skill_key, active_skill, user_query, skill_directive_text, wants_research_context

    def _resolve_screen_and_mentioned_context(
        self,
        lower_msg: str,
        inspected_movie_id: int | None,
        inspected_note: dict[str, Any] | None,
        related_movies: list[dict[str, Any]] | None,
        live_movie_notes: str | None,
    ) -> dict[str, Any]:
        """Resolve open screen movie/note and strictly boundary-matched mentions without 4-letter hijacking."""
        inspected_info = "None"
        inspected_title = None
        relevant_journal_excerpt = "None"
        ui_had_inspected_movie = bool(inspected_movie_id)

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
                        inspected_title = row["title"]
                        year_str = f" ({(row['release_date'] or '')[:4]})" if row["release_date"] else ""
                        effective_notes = (
                            live_movie_notes.strip()
                            if live_movie_notes and live_movie_notes.strip()
                            else None
                        ) or row["notes"]
                        inspected_info = (
                            f"{row['title']}{year_str} (TMDB ID: {inspected_movie_id}), "
                            f"TMDB Rating {row['vote_average']} | Status: {row['status'] or 'unseen'} | "
                            f"User Verdict: {row['verdict'] or 'None'} | User Notes: {effective_notes or 'None'} | "
                            f"Overview: {(row['overview'] or '')[:200]}..."
                        )
                else:
                    # Strict whole-title word-boundary match (never match random 4-letter substrings!)
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
                    stopwords = {
                        "time", "good", "dark", "life", "hard", "dead", "part", "find",
                        "movie", "notes", "note", "from", "library", "then", "this", "that",
                        "with", "have", "what", "list", "show", "watch", "seen", "like",
                    }
                    for r in rows:
                        t = (r["title"] or "").lower().strip()
                        t_norm = re.sub(r"^(?:the|a|an)\s+", "", t).strip()
                        matched = False
                        if len(t) >= 4 and t not in stopwords and re.search(rf"\b{re.escape(t)}\b", lower_msg):
                            matched = True
                        elif len(t_norm) >= 5 and t_norm not in stopwords and re.search(rf"\b{re.escape(t_norm)}\b", lower_msg):
                            matched = True

                        if matched:
                            inspected_movie_id = r["tmdb_id"]
                            inspected_title = r["title"]
                            year_str = f" ({(r['release_date'] or '')[:4]})" if r["release_date"] else ""
                            inspected_info = (
                                f"{r['title']}{year_str} (TMDB ID: {inspected_movie_id}), "
                                f"TMDB Rating {r['vote_average']} | Status: {r['status']} | "
                                f"User Verdict: {r['verdict'] or 'None'} | User Notes: {r['notes'] or 'None'} | "
                                f"Overview: {(r['overview'] or '')[:200]}..."
                            )
                            break

                # Frugal on-demand journal excerpt: fetch full text only if asked or directly relevant
                wants_journal = any(
                    w in lower_msg
                    for w in [
                        "my blog",
                        "my essay",
                        "my note",
                        "my journal",
                        "my writing",
                        "what did i write",
                        "based on my",
                    ]
                )
                if wants_journal or inspected_title:
                    j_entries = conn.execute(
                        """
                        SELECT title, body FROM general_entries
                        WHERE is_deleted = 0 AND is_archived = 0 AND status = 'published'
                        ORDER BY updated_at DESC
                        LIMIT 15
                        """
                    ).fetchall()
                    for er in j_entries:
                        et = (er["title"] or "").lower()
                        if (
                            wants_journal
                            and (
                                et in lower_msg
                                or any(word in lower_msg for word in et.split() if len(word) > 4)
                            )
                        ) or (inspected_title and inspected_title.lower() in et):
                            body_preview = (er["body"] or "")[:700]
                            relevant_journal_excerpt = f"Title: {er['title']}\nExcerpt: {body_preview}"
                            break
        except Exception as exc:
            logger.debug("Could not query journal entries for Grey: %s", exc)

        # Note context resolution (only open note or explicit full-title match, never random 5-letter word hijacking)
        inspected_note_info = "None"
        inspected_note_title = None
        inspected_note_id = None
        has_write_intent = any(re.search(rf"\b{re.escape(v)}\b", lower_msg) for v in NOTE_WRITE_VERBS)

        if inspected_note and isinstance(inspected_note, dict):
            inspected_note_id = inspected_note.get("id")
            inspected_note_title = inspected_note.get("title", "Current Note")
            nbody = inspected_note.get("body", "")
            nstatus = inspected_note.get("status", "note")
            ntags = inspected_note.get("tags", [])
            tag_str = f" | Tags: {', '.join(ntags)}" if ntags else ""
            id_str = f" (ID: {inspected_note_id})" if inspected_note_id else ""
            mode_hint = (
                " [WRITE/EDIT MODE ENABLED]"
                if has_write_intent
                else " [READ-ONLY DISCUSSION MODE — DO NOT MODIFY UNLESS ASKED]"
            )
            inspected_note_info = (
                f"Title: {inspected_note_title}{id_str} (Status: {nstatus}{tag_str}){mode_hint}\n"
                f"Content:\n{nbody[:25000]}"
            )
        else:
            try:
                with self._get_connection() as conn:
                    matched_rows = conn.execute(
                        """
                        SELECT entry_id, title, body, status
                        FROM general_entries
                        WHERE is_deleted = 0 AND is_archived = 0
                        ORDER BY LENGTH(title) DESC, updated_at DESC
                        LIMIT 50
                        """
                    ).fetchall()
                    for mr in matched_rows:
                        m_title = (mr["title"] or "").strip().lower()
                        if len(m_title) >= 3 and m_title in lower_msg:
                            inspected_note_id = mr["entry_id"]
                            inspected_note_title = mr["title"]
                            nbody = mr["body"] or ""
                            nstatus = mr["status"] or "published"
                            mode_hint = (
                                " [WRITE/EDIT MODE ENABLED]"
                                if has_write_intent
                                else " [READ-ONLY DISCUSSION MODE — DO NOT MODIFY UNLESS ASKED]"
                            )
                            inspected_note_info = (
                                f"Title: {inspected_note_title} (ID: {inspected_note_id}) "
                                f"(Status: {nstatus}){mode_hint}\nContent:\n{nbody[:25000]}"
                            )
                            break
            except Exception as exc:
                logger.debug("Could not match note rows for Grey: %s", exc)

        # Format related movies list (never fire a live TMDB fetch unless UI had a movie open and no related list was passed)
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
        elif ui_had_inspected_movie and inspected_movie_id and related_movies is None:
            try:
                movie_svc = MovieService()
                rel_data = movie_svc.get_related_movies(
                    inspected_movie_id, limit=12, include_previously_watched=True
                )
                results = rel_data.get("results") or []
                items = []
                for rm in results[:12]:
                    t = rm.get("title") or rm.get("original_title") or "Unknown"
                    yr = f" ({(rm.get('release_date') or '')[:4]})" if rm.get("release_date") else ""
                    rt = f", TMDB {rm.get('vote_average')}" if rm.get("vote_average") else ""
                    st = (rm.get("user_data") or {}).get("status") or "unseen"
                    vd = (
                        f", User Verdict {rm.get('user_data', {}).get('verdict')}/10"
                        if (rm.get("user_data") or {}).get("verdict")
                        else ""
                    )
                    mid = rm.get("tmdb_id") or ""
                    id_str = f" [ID: {mid}]" if mid else ""
                    items.append(f"- {t}{yr}{id_str}: Status: {st}{rt}{vd}")
                if items:
                    related_movies_str = "\n".join(items)
            except Exception as exc:
                logger.debug("Could not fetch related movies for Grey: %s", exc)

        return {
            "inspected_movie_id": inspected_movie_id,
            "inspected_title": inspected_title,
            "inspected_info": inspected_info,
            "relevant_journal_excerpt": relevant_journal_excerpt,
            "inspected_note_id": inspected_note_id,
            "inspected_note_title": inspected_note_title,
            "inspected_note_info": inspected_note_info,
            "related_movies_str": related_movies_str,
        }

    def _execute_tool_call(self, params: dict[str, Any]) -> str:
        """Execute an on-demand read tool requested by Gemini in ~1ms."""
        tool_name = (params.get("tool") or "").strip().lower()
        try:
            if tool_name == "get_shelf_movies":
                raw_st = (params.get("status") or "watched").strip().lower()
                status = STATUS_NORMALIZATION_MAP.get(raw_st, raw_st)
                limit = min(int(params.get("limit") or 50), 200)
                with self._get_connection() as conn:
                    rows = conn.execute(
                        """
                        SELECT m.tmdb_id, m.title, m.release_date, u.verdict, u.notes
                        FROM user_movie_data u
                        LEFT JOIN movies m ON m.tmdb_id = u.tmdb_id
                        WHERE u.status = ?
                        ORDER BY u.updated_at DESC
                        LIMIT ?
                        """,
                        (status, limit),
                    ).fetchall()
                if not rows:
                    return f"No movies found on shelf '{status}'."
                lines = []
                for r in rows:
                    yr = f" ({(r['release_date'] or '')[:4]})" if r["release_date"] else ""
                    vd = f" [{r['verdict']}/10]" if r["verdict"] is not None else ""
                    nt = f" — Note: {r['notes']}" if r["notes"] else ""
                    m_label = r["title"] or f"TMDB #{r['tmdb_id']}"
                    lines.append(f"- {m_label}{yr}{vd}{nt}")
                return f"Shelf '{status}' ({len(lines)} movies):\n" + "\n".join(lines)

            if tool_name == "get_note":
                entry_id = params.get("entry_id")
                query = (params.get("query") or "").strip()
                with self._get_connection() as conn:
                    row = None
                    if entry_id and str(entry_id).isdigit():
                        row = conn.execute(
                            "SELECT entry_id, title, body, status FROM general_entries WHERE entry_id = ? AND is_deleted = 0",
                            (int(entry_id),),
                        ).fetchone()
                    if not row and query:
                        row = conn.execute(
                            """
                            SELECT e.entry_id, e.title, e.body, e.status
                            FROM general_entries e
                            LEFT JOIN general_entry_tag_links l ON e.entry_id = l.entry_id
                            LEFT JOIN general_entry_tags t ON l.tag_id = t.tag_id
                            WHERE e.is_deleted = 0
                              AND (lower(e.title) LIKE lower(?) OR lower(t.name) LIKE lower(?) OR lower(e.body) LIKE lower(?))
                            ORDER BY (lower(e.title) LIKE lower(?)) DESC, e.updated_at DESC
                            LIMIT 1
                            """,
                            (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"),
                        ).fetchone()
                    if row:
                        return f"Note #{row['entry_id']} '{row['title']}' ({row['status']}):\n{row['body']}"
                    all_notes = conn.execute(
                        "SELECT entry_id, title FROM general_entries WHERE is_deleted = 0 ORDER BY updated_at DESC LIMIT 30"
                    ).fetchall()
                    menu = ", ".join(f"{r['entry_id']}='{r['title']}'" for r in all_notes)
                    return f"No exact note matched '{query}'. Available notes: {menu}"

            if tool_name == "search_library_movie":
                query = (params.get("query") or "").strip()
                with self._get_connection() as conn:
                    rows = conn.execute(
                        """
                        SELECT m.tmdb_id, m.title, m.release_date, u.status, u.verdict, u.notes
                        FROM movies m
                        LEFT JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                        WHERE lower(m.title) LIKE lower(?) OR lower(COALESCE(u.notes, '')) LIKE lower(?)
                        LIMIT 10
                        """,
                        (f"%{query}%", f"%{query}%"),
                    ).fetchall()
                if not rows:
                    return f"No library movies matched '{query}'."
                return "\n".join(
                    f"- {r['title']} ({(r['release_date'] or '')[:4]}) [ID: {r['tmdb_id']}]: "
                    f"Status={r['status'] or 'untracked'}, Verdict={r['verdict'] or 'None'}, Notes={r['notes'] or 'None'}"
                    for r in rows
                )

            if tool_name == "read_research_file":
                fname = params.get("filename") or params.get("query") or ""
                matched = self.resolve_research_file(str(fname))
                if matched and matched.exists():
                    return f"### Research File `{matched.name}`:\n{matched.read_text(encoding='utf-8', errors='ignore')[:8000]}"
                return self.get_research_files_index()
        except Exception as exc:
            logger.warning("Tool execution error (%s): %s", tool_name, exc)
            return f"Tool error: {exc}"
        return "Unknown tool requested."

    def _call_gemini_cascade(
        self, payload: dict[str, Any], target_model: str, default_label: str
    ) -> tuple[Any, str]:
        """Execute Gemini API call across candidate fallback models."""
        if "pro" in target_model.lower():
            candidate_models = list(dict.fromkeys([target_model, *GEMINI_PRO_CANDIDATE_MODELS]))
        else:
            candidate_models = list(dict.fromkeys([target_model, *GEMINI_FLASH_CANDIDATE_MODELS]))

        resp = None
        model_label = default_label
        for model_candidate in candidate_models:
            try:
                endpoint = f"{GEMINI_API_BASE_URL}/models/{model_candidate}:generateContent?key={self.api_key}"
                resp = requests.post(
                    endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=35,
                )
                if resp.status_code == 200:
                    model_label = f"Gemini {model_candidate.replace('gemini-', '').capitalize()}"
                    break
                logger.info(
                    f"Model {model_candidate} returned {resp.status_code}, trying next in cascade..."
                )
            except requests.exceptions.Timeout:
                logger.warning(f"Model {model_candidate} timed out, trying next in cascade...")
                continue
            except requests.exceptions.RequestException as req_err:
                logger.warning(
                    f"Model {model_candidate} request error: {req_err}, trying next in cascade..."
                )
                continue

        return resp, model_label

    @staticmethod
    def _parse_gemini_json(resp: Any) -> dict[str, Any]:
        """Extract and sanitize JSON response envelope from Gemini candidate parts."""
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
                        data = json.loads(clean_str[start_idx : end_idx + 1])
                    except Exception:
                        data = None

        if not isinstance(data, dict):
            data = {
                "text": clean_str or "I've reviewed your request and library.",
                "action": None,
                "pills": [],
            }
        return data

    def _handle_create_draft(self, action: dict[str, Any], pills: list[dict[str, Any]]) -> None:
        try:
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
            self.invalidate_dossier_cache()
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
                pills.insert(
                    0,
                    {
                        "label": f"📖 Open Draft: {draft_title[:24]}",
                        "action": "open_entry",
                        "payload": {"entry_id": draft_id},
                    },
                )
        except Exception as draft_err:
            logger.error(f"Failed to auto-create draft entry: {draft_err}")

    def _handle_batch_set_movie_status(
        self,
        action: dict[str, Any],
        data: dict[str, Any],
        related_movies: list[dict[str, Any]] | None,
    ) -> None:
        try:
            movie_svc = MovieService()
            user_repo = UserMovieRepository()
            params = action.get("params") or {}
            raw_st = params.get("status")
            target_status = (
                STATUS_NORMALIZATION_MAP.get(str(raw_st).lower().strip(), raw_st)
                if raw_st
                else None
            )

            raw_movies = params.get("movies") or params.get("tmdb_ids") or []
            if not isinstance(raw_movies, list):
                raw_movies = [raw_movies]

            related_title_map: dict[str, int] = {}
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
                                (clean_t, clean_t_noyear),
                            ).fetchone()
                            if row:
                                m_id = row["tmdb_id"]
                                m_title = row["title"]

                if m_id and target_status:
                    user_data = user_repo.get_user_movie_data(m_id)
                    current_status = user_data.get("status") if user_data else None

                    if target_status == "new_discovery" and current_status is not None:
                        preserved_movies.append(
                            {
                                "tmdb_id": m_id,
                                "title": m_title or f"Movie #{m_id}",
                                "status": current_status,
                            }
                        )
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

            self.invalidate_dossier_cache()
            if not isinstance(action.get("params"), dict):
                action["params"] = {}
            action["params"]["movies"] = updated_movies
            action["params"]["status"] = target_status

            if preserved_movies:
                preserved_notes = [
                    f"**{pm['title']}** (kept as {pm['status'].replace('_', ' ').upper()})"
                    for pm in preserved_movies
                ]
                preserved_msg = f"Preserved prior judgments: {', '.join(preserved_notes)}."
                if data.get("text"):
                    data["text"] = f"{data['text']}\n\n{preserved_msg}"
                else:
                    data["text"] = preserved_msg
        except Exception as batch_err:
            logger.error(f"Failed to batch set movie status via Grey: {batch_err}")

    def _convert_status_action_to_note_append(
        self,
        action: dict[str, Any],
        inspected_movie_id: int | None,
        inspected_title: str | None,
        inspected_note_id: Any,
        inspected_note: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Convert a misrouted set_movie_status action into an update_entry append when user targeted a note/post."""
        t_id = action.get("params", {}).get("tmdb_id") or inspected_movie_id
        t_title = action.get("params", {}).get("title") or inspected_title or "Movie"
        m_year = ""
        m_overview = ""
        cast_names = "Unknown"
        if t_id:
            with self._get_connection() as conn:
                m_row = conn.execute(
                    "SELECT title, release_date, overview FROM movies WHERE tmdb_id = ?",
                    (t_id,),
                ).fetchone()
                if m_row:
                    t_title = m_row["title"]
                    m_year = f" ({(m_row['release_date'] or '')[:4]})" if m_row["release_date"] else ""
                    m_overview = (m_row["overview"] or "").strip()
                c_rows = conn.execute(
                    "SELECT name FROM movie_credits WHERE tmdb_id = ? AND credit_type = 'actor' ORDER BY position ASC LIMIT 3",
                    (t_id,),
                ).fetchall()
                if c_rows:
                    cast_names = ", ".join(c["name"] for c in c_rows)

        target_body_format = "toggle"
        existing_body_sample = ""
        if inspected_note_id:
            with self._get_connection() as conn:
                erow = conn.execute(
                    "SELECT body FROM general_entries WHERE entry_id = ?",
                    (inspected_note_id,),
                ).fetchone()
                if erow and erow["body"]:
                    existing_body_sample = erow["body"].strip()
        elif inspected_note and isinstance(inspected_note, dict):
            existing_body_sample = (inspected_note.get("body") or "").strip()

        bullet_char = "•"
        has_imdb = "imdb" in existing_body_sample.lower()
        if existing_body_sample:
            lines = [l.strip() for l in existing_body_sample.splitlines() if l.strip()]
            bullet_lines = [
                l for l in lines if l.startswith("•") or l.startswith("- ") or l.startswith("* ")
            ]
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
                f"- **Synopsis:** {m_overview[:180]}..."
            )

        return {
            "type": "update_entry",
            "params": {
                "title": None,
                "body": appended_body,
                "mode": "append",
            },
        }

    def _handle_set_movie_status(
        self,
        action: dict[str, Any],
        data: dict[str, Any],
        inspected_movie_id: int | None,
    ) -> dict[str, Any] | None:
        try:
            movie_svc = MovieService()
            params = action.get("params") or {}
            param_tmdb_id = params.get("tmdb_id")
            param_title = (params.get("title") or "").strip()
            target_tmdb_id = None

            if param_tmdb_id and str(param_tmdb_id).isdigit():
                target_tmdb_id = int(param_tmdb_id)
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
                        (clean_t, clean_t_noyear),
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
                target_status = STATUS_NORMALIZATION_MAP.get(raw_st, raw_st)

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

                self.invalidate_dossier_cache()
                if not isinstance(action.get("params"), dict):
                    action["params"] = {}
                action["params"]["tmdb_id"] = target_tmdb_id
                action["params"]["status"] = target_status
            return action
        except Exception as status_err:
            logger.error(f"Failed to set movie status via Grey: {status_err}")
            data["text"] = f"I couldn't update the status for this movie due to an error: {status_err}"
            return None

    def _handle_update_entry(
        self,
        action: dict[str, Any],
        data: dict[str, Any],
        pills: list[dict[str, Any]],
        message: str,
        lower_msg: str,
        inspected_note_id: Any,
        inspected_note_title: str | None,
        inspected_movie_id: int | None,
        inspected_title: str | None,
        is_post_target_mention: bool,
    ) -> dict[str, Any] | None:
        try:
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
                        (str(target_title).strip(),),
                    ).fetchone()
                    if not row:
                        row = conn.execute(
                            "SELECT entry_id FROM general_entries WHERE is_deleted = 0 AND lower(title) LIKE lower(?) ORDER BY updated_at DESC LIMIT 1",
                            (f"%{str(target_title).strip()}%",),
                        ).fetchone()
                    if row:
                        existing = repo.get_entry(row["entry_id"])

            if not existing:
                with self._get_connection() as conn:
                    all_titles = conn.execute(
                        "SELECT entry_id, title FROM general_entries WHERE is_deleted = 0"
                    ).fetchall()
                    sorted_titles = sorted(
                        all_titles, key=lambda x: len(x["title"] or ""), reverse=True
                    )
                    for at in sorted_titles:
                        if at["title"] and at["title"].strip().lower() in lower_msg:
                            existing = repo.get_entry(at["entry_id"])
                            break

            if not existing:
                cand_match = re.search(
                    r"(?:add|save|append|put)\s+(?:this\s+)?(?:to\s+|into\s+)?(?:my\s+)?['\"]?([^'\"\n]+?)['\"]?\s+(?:post|note|journal|entry|blog|draft|list)",
                    message,
                    re.IGNORECASE,
                )
                if cand_match:
                    cand_title = cand_match.group(1).strip()
                    with self._get_connection() as conn:
                        row = conn.execute(
                            "SELECT entry_id FROM general_entries WHERE is_deleted = 0 AND lower(title) = lower(?) ORDER BY updated_at DESC LIMIT 1",
                            (cand_title,),
                        ).fetchone()
                        if not row:
                            row = conn.execute(
                                "SELECT entry_id FROM general_entries WHERE is_deleted = 0 AND lower(title) LIKE lower(?) ORDER BY updated_at DESC LIMIT 1",
                                (f"%{cand_title}%",),
                            ).fetchone()
                        if row:
                            existing = repo.get_entry(row["entry_id"])

            explicit_note_request = (
                any(
                    w in lower_msg
                    for w in ["note", "draft", "journal", "essay", "blog", "write-up", "entry", "list", "post"]
                )
                or (bool(target_title) and str(target_title).strip().lower() in lower_msg)
                or (bool(existing) and existing["title"].strip().lower() in lower_msg)
            )

            if not inspected_note_id and not explicit_note_request:
                logger.warning(
                    "Rejected unprompted update_entry action: user did not request note modification."
                )
                return None
            if not existing:
                data["text"] = (
                    f"I couldn't locate the note '{target_title or 'requested'}' in your notebook to update."
                )
                return None

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
            self.invalidate_dossier_cache()
            if updated:
                if not isinstance(action.get("params"), dict):
                    action["params"] = {}
                action["params"]["entry_id"] = updated["entry_id"]
                action["params"]["title"] = updated["title"]
                if is_post_target_mention and (
                    not data.get("text")
                    or "movie" in data.get("text", "").lower()
                    or "status" in data.get("text", "").lower()
                ):
                    data["text"] = f"Added to your '{updated['title']}' post."

                open_pill_found = False
                for p in pills:
                    if (
                        p.get("action") in ("open_entry", "open_note")
                        or "open" in (p.get("label") or "").lower()
                    ):
                        p["action"] = "open_entry"
                        p["payload"] = {"entry_id": updated["entry_id"], "title": updated["title"]}
                        p["label"] = f"📖 Open {updated['title'][:24]}"
                        open_pill_found = True
                        break
                if not open_pill_found:
                    pills.insert(
                        0,
                        {
                            "label": f"📖 Open {updated['title'][:24]}",
                            "action": "open_entry",
                            "payload": {"entry_id": updated["entry_id"], "title": updated["title"]},
                        },
                    )
            return action
        except Exception as update_err:
            logger.error(f"Failed to update entry: {update_err}")
            return action

    def _handle_research_file_action(self, action: dict[str, Any], data: dict[str, Any]) -> None:
        act_type = action.get("type")
        params = action.get("params") or {}
        if act_type == "save_research_file":
            try:
                raw_fname = (params.get("filename") or params.get("title") or "research").strip()
                if not raw_fname.endswith(".md"):
                    raw_fname += ".md"
                clean_fname = re.sub(r"[^\w\.\-]", "_", raw_fname).lower()
                if not clean_fname.endswith(".md"):
                    clean_fname += ".md"
                file_path = self.research_dir / clean_fname
                content = (params.get("content") or "").strip()
                if not content and data.get("text"):
                    content = (
                        f"# {params.get('title') or clean_fname[:-3].replace('_', ' ').title()}\n\n"
                        f"{data['text']}"
                    )
                file_path.write_text(content + "\n", encoding="utf-8")
                if not isinstance(action.get("params"), dict):
                    action["params"] = {}
                action["params"]["filename"] = clean_fname
                action["params"]["filepath"] = str(file_path)
            except Exception as r_save_err:
                logger.error(f"Failed to save research file: {r_save_err}")

        elif act_type == "append_research_file":
            try:
                target_query = params.get("filename") or params.get("title") or ""
                entry_text = (params.get("entry") or params.get("text") or "").strip()
                matched_file = self.resolve_research_file(target_query)
                if not matched_file:
                    raw_fname = (target_query or "research.md").strip()
                    clean_fname = re.sub(r"[^\w\.\-]", "_", raw_fname).lower()
                    if not clean_fname.endswith(".md"):
                        clean_fname += ".md"
                    matched_file = self.research_dir / clean_fname
                    matched_file.write_text(
                        f"# {target_query.replace('_', ' ').title()}\n\n", encoding="utf-8"
                    )

                with open(matched_file, "a", encoding="utf-8") as af:
                    af.write(f"\n{entry_text}\n")

                if not isinstance(action.get("params"), dict):
                    action["params"] = {}
                action["params"]["filename"] = matched_file.name
                action["params"]["filepath"] = str(matched_file)
            except Exception as r_app_err:
                logger.error(f"Failed to append to research file: {r_app_err}")

        elif act_type == "delete_research_file":
            try:
                target_query = params.get("filename") or params.get("title") or ""
                matched_file = self.resolve_research_file(target_query)
                if matched_file and matched_file.exists():
                    matched_file.unlink()
                    if not isinstance(action.get("params"), dict):
                        action["params"] = {}
                    action["params"]["filename"] = matched_file.name
            except Exception as r_del_err:
                logger.error(f"Failed to delete research file: {r_del_err}")

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

        lower_msg = message.lower()
        target_model, model_label = self._select_target_model(lower_msg, model_mode)

        ctx = self._resolve_screen_and_mentioned_context(
            lower_msg=lower_msg,
            inspected_movie_id=inspected_movie_id,
            inspected_note=inspected_note,
            related_movies=related_movies,
            live_movie_notes=live_movie_notes,
        )
        inspected_movie_id = ctx["inspected_movie_id"]
        inspected_title = ctx["inspected_title"]
        inspected_info = ctx["inspected_info"]
        relevant_journal_excerpt = ctx["relevant_journal_excerpt"]
        inspected_note_id = ctx["inspected_note_id"]
        inspected_note_title = ctx["inspected_note_title"]
        inspected_note_info = ctx["inspected_note_info"]
        related_movies_str = ctx["related_movies_str"]

        (
            active_skill_key,
            active_skill,
            user_query,
            skill_directive_text,
            wants_research_context,
        ) = self._resolve_active_skill(
            message=message,
            current_view=current_view,
            inspected_note_id=inspected_note_id,
            active_person=active_person,
            active_skill_key=active_skill_key,
            history=history,
        )

        # Targeted dossier loading from RAM cache
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

        active_person_info = "None"
        if active_person and isinstance(active_person, dict):
            p_name = active_person.get("name") or "Unknown"
            p_dept = (
                active_person.get("known_for_department") or active_person.get("department") or ""
            )
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

        # Load core prompt from in-memory cache
        system_template = self._read_cached_file(self.prompts_dir / "grey_core.md")
        if not system_template:
            system_template = self._read_cached_file(self.prompts_dir / "grey_system_prompt.md")

        # Two-Tier Progressive Context: only inject full 15,000-char research files when research is active
        research_files_str = (
            self.get_research_files_index()
            if wants_research_context
            else self.get_research_files_summary()
        )
        reactions_index_str = self.get_reactions_index()

        # Hybrid 1-Line RAM Title Map for notes (replaces 50-object JSON dump while preserving full title visibility)
        notes_menu_items = [
            f'{n["entry_id"]}="{n["title"]}"'
            for n in dossier.get("journal_notes_list", [])[:35]
        ]
        compact_notes_index = ", ".join(notes_menu_items) if notes_menu_items else "None"

        system_instruction = (
            system_template.replace("{{ACTIVE_SKILL_DIRECTIVE}}", skill_directive_text)
            .replace("{{INSPECTED_INFO}}", inspected_info)
            .replace("{{INSPECTED_TITLE}}", inspected_title or "None")
            .replace("{{INSPECTED_MOVIE_TMDB_ID}}", str(inspected_movie_id or "None"))
            .replace("{{RELATED_MOVIES_LIST}}", related_movies_str)
            .replace("{{INSPECTED_NOTE_INFO}}", inspected_note_info)
            .replace("{{INSPECTED_NOTE_TITLE}}", inspected_note_title or "None")
            .replace("{{INSPECTED_NOTE_ID}}", str(inspected_note_id or "None"))
            .replace("{{ACTIVE_PERSON_INFO}}", active_person_info)
            .replace("{{VISIBLE_MOVIES_LIST}}", visible_movies_str)
            .replace("{{RESEARCH_FILES_INDEX}}", research_files_str)
            .replace("{{AVAILABLE_REACTIONS}}", reactions_index_str)
            .replace("{{FAVORITES_JSON}}", json.dumps(dossier["high_rated"][:5]))
            .replace("{{WATCHLIST_JSON}}", json.dumps(dossier["watchlist"][:12]))
            .replace("{{DISCARDED_COUNT}}", str(dossier["discarded_count"]))
            .replace("{{DISCARDED_SAMPLES_JSON}}", json.dumps(dossier["discarded_samples"][:4]))
            .replace("{{JOURNAL_NOTES_LIST}}", compact_notes_index)
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
            titles_sample = [
                vm.get("title") or vm.get("original_title")
                for vm in visible_movies[:8]
                if (vm.get("title") or vm.get("original_title"))
            ]
            if titles_sample:
                screen_contexts.append(
                    f"Grid shows {len(visible_movies)} titles including: {', '.join(titles_sample)}"
                )
        if notes_shelf_filter:
            screen_contexts.append(f"Movie Notes paired shelf filter: {notes_shelf_filter}")
        if inspected_title:
            id_info = f" (TMDB ID: {inspected_movie_id})" if inspected_movie_id else ""
            screen_contexts.append(f"Currently viewing movie on screen: {inspected_title}{id_info}")
            if live_movie_notes and live_movie_notes.strip():
                screen_contexts.append(
                    f"Active movie Personal Memory on screen: {live_movie_notes.strip()[:300]}"
                )
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

        try:
            resp, model_label = self._call_gemini_cascade(payload, target_model, model_label)
            if not resp or resp.status_code != 200:
                logger.error(
                    f"All Gemini models exhausted. Last error: {resp.status_code if resp else 'None'}"
                )
                return {
                    "text": "I ran into a temporary connection issue reaching the Gemini engine. Please try your request again in a moment.",
                    "action": None,
                    "pills": [],
                    "model_used": "Offline",
                }

            data = self._parse_gemini_json(resp)

            # On-Demand Tool Loop: if Gemini requested a tool_call, execute locally in 1ms and complete in 2nd hop
            action = data.get("action")
            if isinstance(action, dict) and action.get("type") == "tool_call":
                tool_output = self._execute_tool_call(action.get("params") or {})
                contents.append({"role": "model", "parts": [{"text": json.dumps(data)}]})
                contents.append(
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": f"[TOOL RESULT]\n{tool_output}\nNow provide your final JSON response to the user."
                            }
                        ],
                    }
                )
                resp2, model_label = self._call_gemini_cascade(payload, target_model, model_label)
                if resp2 and resp2.status_code == 200:
                    data = self._parse_gemini_json(resp2)
                    action = data.get("action")

            pills = data.get("pills", [])

            # Synthesize batch_set_movie_status if model returned multiple set_movie_status actions
            if isinstance(data.get("actions"), list) and data["actions"]:
                status_actions = [
                    a
                    for a in data["actions"]
                    if isinstance(a, dict) and a.get("type") == "set_movie_status"
                ]
                if len(status_actions) > 1 and not (
                    action and action.get("type") == "batch_set_movie_status"
                ):
                    first_status = status_actions[0].get("params", {}).get("status")
                    action = {
                        "type": "batch_set_movie_status",
                        "params": {
                            "status": first_status,
                            "movies": [a.get("params", {}) for a in status_actions],
                        },
                    }
                elif len(status_actions) == 1 and not action:
                    action = status_actions[0]

            # Only treat as a journal post target when user explicitly targets a post/note/entry (not movie personal notes)
            is_post_target_mention = bool(
                re.search(
                    r"\b(?:to|in|into)\s+(?:my\s+)?.*?\b(?:post|note|journal|entry|draft|blog|write-up)\b",
                    lower_msg,
                )
            )

            if action and action.get("type") == "create_draft":
                self._handle_create_draft(action, pills)
            elif action and action.get("type") == "batch_set_movie_status":
                self._handle_batch_set_movie_status(action, data, related_movies)
            elif action and action.get("type") == "set_movie_status":
                if is_post_target_mention:
                    logger.info(
                        "Intercepted set_movie_status with explicit post/note target; converting to update_entry."
                    )
                    action = self._convert_status_action_to_note_append(
                        action=action,
                        inspected_movie_id=inspected_movie_id,
                        inspected_title=inspected_title,
                        inspected_note_id=inspected_note_id,
                        inspected_note=inspected_note,
                    )
                else:
                    action = self._handle_set_movie_status(action, data, inspected_movie_id)

            if action and action.get("type") == "update_entry":
                action = self._handle_update_entry(
                    action=action,
                    data=data,
                    pills=pills,
                    message=message,
                    lower_msg=lower_msg,
                    inspected_note_id=inspected_note_id,
                    inspected_note_title=inspected_note_title,
                    inspected_movie_id=inspected_movie_id,
                    inspected_title=inspected_title,
                    is_post_target_mention=is_post_target_mention,
                )

            if action and action.get("type") in (
                "save_research_file",
                "append_research_file",
                "delete_research_file",
            ):
                self._handle_research_file_action(action, data)

            reaction = data.get("reaction")
            valid_reaction = None
            if reaction and isinstance(reaction, str):
                reaction_filename = Path(reaction).name
                reaction_path = self.reactions_dir / reaction_filename
                if reaction_path.exists() and reaction_path.is_file():
                    valid_reaction = reaction_filename

            # Filter out unsolicited shelf categorization pills
            sanitized_pills = []
            for p in pills or []:
                if not isinstance(p, dict):
                    continue
                lbl = (p.get("label") or "").lower()
                act = p.get("action")
                payload_st = str((p.get("payload") or {}).get("status", "")).lower()
                is_status_pill = (
                    act == "set_movie_status"
                    or payload_st
                    in ("watch_later", "new_discovery", "watched", "rewatch", "excluded")
                    or any(
                        s in lbl for s in ["watchlist", "new discovery", "add to shelf", "mark as"]
                    )
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
