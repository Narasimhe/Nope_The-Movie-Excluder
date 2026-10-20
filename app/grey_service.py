import json
import logging
import os
import sqlite3
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
    "watchlist": {
        "command": "/watchlist",
        "name": "Toggle Watchlist Builder",
        "description": "Drafts or updates a watchlist note using clean >> Title (Year) toggles.",
        "requires_dossier": True,
        "directive": (
            "ACTIVE SKILL: /watchlist (Toggle Watchlist Builder)\n"
            "Create a new journal draft note using clean Notion-style expandable toggles.\n"
            "Use the 'create_draft' action with 'title', 'tags', and 'body'.\n"
            "Format every single movie inside the body using >> Title (Year):\n"
            ">> [Movie Title] ([Year])\n"
            "- **Cast:** [Actor names]\n"
            "- **Synopsis:** [1-sentence premise]\n"
            "- **Why YES:** [1-sentence cinephile reason]\n\n"
            "NEVER use raw HTML tags like <details> or <summary>. ALWAYS use >> [Title] ([Year])."
        ),
        "default_query": "Create a watchlist draft note using >> Title (Year) toggles.",
    },
    "tonight": {
        "command": "/tonight",
        "name": "Tonight's Pick",
        "description": "Selects 1-2 curated films from your Watchlist or Rewatch shelf.",
        "requires_dossier": True,
        "directive": (
            "ACTIVE SKILL: /tonight (Tonight's Pick)\n"
            "Recommend 1 or 2 specific films from the user's Watchlist or designated Rewatch shelf.\n"
            "State clearly why it fits tonight's viewing with a 1-2 sentence pitch.\n"
            "Provide 'open_movie' pills for the recommended titles."
        ),
        "default_query": "What should I watch tonight from my watchlist or rewatch shelf?",
    },
    "nope": {
        "command": "/nope",
        "name": "Why Did I Nope This?",
        "description": "Diagnoses why a film was rejected or excluded based on your notes and craft criteria.",
        "requires_dossier": False,
        "directive": (
            "ACTIVE SKILL: /nope (Why Did I Nope This?)\n"
            "Diagnose why the inspected film was rejected or excluded.\n"
            "Reference the user's personal memory notes and deliver an honest critique of the script/pacing flaws."
        ),
        "default_query": "Why did I nope/reject this movie?",
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
}


class GreyService:
    def __init__(self, db_path: str = "data/movie_excluder.db"):
        self.db_path = db_path
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()

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
            "all_watched_titles": watched_titles if 'watched_titles' in locals() else [],
            "rewatch_list": rewatch_list if 'rewatch_list' in locals() else [],
            "all_excluded_titles": excluded_titles if 'excluded_titles' in locals() else [],
        }

    def chat(
        self,
        message: str,
        current_view: str = "library",
        inspected_movie_id: int | None = None,
        inspected_note: dict[str, Any] | None = None,
        related_movies: list[dict[str, Any]] | None = None,
        active_filters: dict[str, Any] | None = None,
        history: list[dict[str, str]] | None = None,
        model_mode: str = "auto",
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
        active_skill_key = None
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
            elif any(p in lq for p in ["why did i nope", "why is this noped", "why did i exclude", "why was this rejected", "why was it rejected"]):
                active_skill_key = "nope"
            elif any(p in lq for p in ["what should i watch tonight", "what to watch tonight", "pick something to watch", "tonight's pick", "pick for tonight"]):
                active_skill_key = "tonight"
            elif any(p in lq for p in ["make a watchlist", "create a watchlist", "draft a watchlist", "toggle watchlist"]):
                active_skill_key = "watchlist"
            elif any(p in lq for p in ["add the yes movies", "add all yes", "batch add", "batch move"]):
                active_skill_key = "batch"

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
                        inspected_info = f"{row['title']}{year_str} (TMDB ID: {inspected_movie_id}), TMDB Rating {row['vote_average']} | Status: {row['status'] or 'unseen'} | User Verdict: {row['verdict'] or 'None'} | User Notes: {row['notes'] or 'None'} | Overview: {row['overview'][:200]}..."
                else:
                    # Search if user mentioned a specific movie title in their message
                    rows = conn.execute(
                        """
                        SELECT m.tmdb_id, m.title, m.release_date, m.overview, m.vote_average, u.status, u.verdict, u.notes
                        FROM movies m
                        LEFT JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                        WHERE u.status IS NOT NULL
                        ORDER BY u.updated_at DESC
                        LIMIT 100
                        """
                    ).fetchall()
                    for r in rows:
                        t = (r["title"] or "").lower()
                        if len(t) > 3 and t in lower_msg:
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

        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "grey_system_prompt.md")
        system_template = ""
        if os.path.exists(prompt_path):
            try:
                with open(prompt_path, "r", encoding="utf-8") as f:
                    system_template = f.read()
            except Exception as e:
                logger.warning(f"Could not read prompt file {prompt_path}: {e}")

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
Active filters: {{ACTIVE_FILTERS_JSON}}
"""

        system_instruction = (
            system_template
            .replace("{{ACTIVE_SKILL_DIRECTIVE}}", active_skill["directive"] if active_skill else "None")
            .replace("{{INSPECTED_INFO}}", inspected_info)
            .replace("{{INSPECTED_TITLE}}", inspected_title or "None")
            .replace("{{INSPECTED_MOVIE_TMDB_ID}}", str(inspected_movie_id or "None"))
            .replace("{{RELATED_MOVIES_LIST}}", related_movies_str)
            .replace("{{INSPECTED_NOTE_INFO}}", inspected_note_info)
            .replace("{{INSPECTED_NOTE_TITLE}}", inspected_note_title or "None")
            .replace("{{INSPECTED_NOTE_ID}}", str(inspected_note_id or "None"))
            .replace("{{FAVORITES_JSON}}", json.dumps(dossier["high_rated"][:8]))
            .replace("{{WATCHLIST_JSON}}", json.dumps(dossier["watchlist"][:12]))
            .replace("{{DISCARDED_COUNT}}", str(dossier["discarded_count"]))
            .replace("{{DISCARDED_SAMPLES_JSON}}", json.dumps(dossier["discarded_samples"][:6]))
            .replace("{{JOURNAL_DIGEST}}", json.dumps(dossier.get("journal_digest", [])))
            .replace("{{RELEVANT_JOURNAL_EXCERPT}}", relevant_journal_excerpt)
            .replace("{{ALL_WATCHED_TITLES}}", ", ".join(dossier.get("all_watched_titles", [])) or "None")
            .replace("{{REWATCH_LIST}}", ", ".join(dossier.get("rewatch_list", [])) or "None")
            .replace("{{ALL_EXCLUDED_TITLES}}", ", ".join(dossier.get("all_excluded_titles", [])) or "None")
            .replace("{{CURRENT_VIEW}}", current_view)
            .replace("{{ACTIVE_FILTERS_JSON}}", json.dumps(active_filters or {}))
        )

        contents = []
        if history:
            for item in history[-6:]:
                role = "user" if item.get("role") == "user" else "model"
                contents.append({"role": role, "parts": [{"text": item.get("text", "")}]})

        screen_contexts = []
        if inspected_title:
            id_info = f" (TMDB ID: {inspected_movie_id})" if inspected_movie_id else ""
            screen_contexts.append(f"Currently viewing movie on screen: {inspected_title}{id_info}")
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
                    import re
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
                try:
                    from app.movie_service import MovieService
                    import re
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

            elif action and action.get("type") == "update_entry":
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
                    if not existing:
                        with self._get_connection() as conn:
                            all_titles = conn.execute("SELECT entry_id, title FROM general_entries WHERE is_deleted = 0").fetchall()
                            for at in all_titles:
                                if at["title"] and at["title"].strip().lower() in lower_msg:
                                    existing = repo.get_entry(at["entry_id"])
                                    break

                    # The user must either have the note open on screen, OR explicitly request note modification in chat message
                    explicit_note_request = (
                        any(w in lower_msg for w in ["note", "draft", "journal", "essay", "blog", "write-up", "entry", "list"])
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
                        final_body = new_body
                        if mode == "append" and existing.get("body"):
                            final_body = f"{existing['body'].rstrip()}\n\n{new_body.lstrip()}"

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

            return {
                "text": data.get("text", "Here are the matching titles from your library."),
                "action": action,
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
