import datetime
import json
import logging
import os
import re
import sqlite3
import time
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
from app.movie_service import MovieService

logger = logging.getLogger(__name__)

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
}


class GreyService:
    """AI Cinema Companion orchestrator with Two-Tier Progressive Context & RAM caching."""

    _file_cache: dict[str, tuple[float, str]] = {}
    _model_cooldowns: dict[str, float] = {}

    def __init__(self, db_path: str = "data/movie_excluder.db"):
        self.db_path = db_path
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.prompts_dir = Path(__file__).resolve().parent / "prompts"
        self.reactions_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "gifs_n_media"
        self.reactions_dir.mkdir(parents=True, exist_ok=True)
        self.reactions_file = Path(__file__).resolve().parent / "reactions.json"

        self.http_session = requests.Session()
        self._reactions_cache: tuple[float, float, str] | None = None
        self._dossier_cache: tuple[str, dict[str, Any]] | None = None
        self._reception_cache: dict[str, dict[str, Any]] = {}

        # Preload static prompt templates into memory at initialization
        self._preload_prompts()

    def _fetch_live_film_reception(self, title: str, year: str = "") -> dict[str, Any]:
        """Fetch live critical reception, Rotten Tomatoes score & consensus, and Metacritic data via Wikipedia REST API in ~200ms."""
        if not title:
            return {}
        cache_key = f"{title.lower()}::{year}"
        if cache_key in self._reception_cache:
            return self._reception_cache[cache_key]

        headers = {"User-Agent": "MovieExcluderApp/1.0 (contact@movieexcluder.local)"}
        query = f"{title} {year} film" if year else f"{title} film"
        try:
            s_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json"
            r = self.http_session.get(s_url, headers=headers, timeout=3.5)
            if r.status_code != 200:
                self._reception_cache[cache_key] = {}
                return {}
            results = r.json().get("query", {}).get("search", [])
            if not results:
                self._reception_cache[cache_key] = {}
                return {}
            page_title = results[0]["title"]

            sec_url = f"https://en.wikipedia.org/w/api.php?action=parse&page={requests.utils.quote(page_title)}&prop=sections&format=json"
            r2 = self.http_session.get(sec_url, headers=headers, timeout=3.5)
            if r2.status_code != 200:
                self._reception_cache[cache_key] = {}
                return {}
            sections = r2.json().get("parse", {}).get("sections", [])
            target_idx = None
            for s in sections:
                line = s.get("line", "").lower()
                if "critical response" in line or "critical reception" in line:
                    target_idx = s["index"]
                    break
                elif "reception" in line and not target_idx:
                    target_idx = s["index"]
            if not target_idx:
                self._reception_cache[cache_key] = {}
                return {}

            p_url = f"https://en.wikipedia.org/w/api.php?action=parse&page={requests.utils.quote(page_title)}&prop=wikitext&section={target_idx}&format=json"
            r3 = self.http_session.get(p_url, headers=headers, timeout=3.5)
            if r3.status_code != 200:
                self._reception_cache[cache_key] = {}
                return {}
            wikitext = r3.json().get("parse", {}).get("wikitext", {}).get("*", "")

            out: dict[str, Any] = {}
            # Rotten Tomatoes template extraction
            rt_m = re.search(
                r'\{\{(?:Rotten Tomatoes prose|RT prose)\|(\d+)\|([\d.]+)\|(\d+)\|(.*?)(?:\|ref=|\}\})',
                wikitext,
                re.DOTALL,
            )
            if rt_m:
                pct, avg, count, consensus = rt_m.groups()
                out["rt_score"] = f"{pct}%"
                out["rt_avg"] = avg
                out["rt_count"] = count
                clean_cons = re.sub(r"<[^>]+>", "", consensus.replace("''", "").strip())
                out["rt_consensus"] = clean_cons

            # Metacritic extraction
            mc_m = re.search(
                r"score of (\d+) out of 100.*?based on (\d+) critics", wikitext, re.DOTALL
            )
            if mc_m:
                out["metacritic"] = f"{mc_m.group(1)}/100 ({mc_m.group(2)} critics)"

            # Clean prose overview
            clean = re.sub(r"<ref[^>]*>.*?</ref>", "", wikitext, flags=re.DOTALL)
            clean = re.sub(r"<ref[^>]*/>", "", clean)
            clean = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", clean)
            clean = re.sub(r"\{\{[^}]+\}\}", "", clean)
            clean = re.sub(r"[\r\n]+", " ", clean).strip()
            out["summary"] = clean[:500]

            self._reception_cache[cache_key] = out
            return out
        except Exception as e:
            logger.debug(f"Live reception fetch failed for {title}: {e}")
            self._reception_cache[cache_key] = {}
            return {}

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

        metadata: dict[str, Any] = {}
        raw_meta = self._read_cached_file(self.reactions_file)
        if raw_meta:
            try:
                parsed = json.loads(raw_meta)
                if isinstance(parsed, list):
                    metadata = {
                        item["filename"]: item
                        for item in parsed
                        if isinstance(item, dict) and "filename" in item
                    }
                elif isinstance(parsed, dict):
                    metadata = parsed
            except Exception:
                metadata = {}

        items = []
        for f in sorted(files):
            entry = metadata.get(f)
            if isinstance(entry, dict):
                tier = entry.get("verdict_tier", "general")
                ctx = entry.get("trigger_context", "")
                items.append(f"- Tier `[{tier}]` -> `{f}`: {ctx}")
            elif isinstance(entry, str) and entry:
                items.append(f"- `{f}`: {entry}")
            else:
                inferred = re.sub(r"[_\-]+", " ", Path(f).stem).strip()
                items.append(f"- `{f}`: {inferred}")

        result = "\n".join(items)
        self._reactions_cache = (dir_mtime, meta_mtime, result)
        return result

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_taste_dossier(self) -> dict[str, Any]:
        """Extract user taste dossier using 2 consolidated SQLite queries + RAM cache (down from 17 queries)."""
        favorites: list[dict[str, Any]] = []
        watchlist: list[dict[str, Any]] = []
        discarded_count = 0
        discarded_samples: list[dict[str, Any]] = []
        journal_digest: list[dict[str, Any]] = []
        journal_notes_list: list[dict[str, Any]] = []
        all_active_notes: list[dict[str, Any]] = []
        watched_titles: list[str] = []
        rewatch_list: list[str] = []
        excluded_titles: list[str] = []
        new_discovery_list: list[str] = []
        tracked_movies_index: list[dict[str, Any]] = []

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
                    ORDER BY (u.notes IS NOT NULL AND trim(u.notes) != '') DESC, u.updated_at DESC
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

                    if title and status is not None:
                        tracked_movies_index.append({
                            "tmdb_id": r["tmdb_id"],
                            "title": title,
                        })

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
                    WHERE e.is_deleted = 0 AND e.is_archived = 0
                    GROUP BY e.entry_id
                    ORDER BY e.updated_at DESC
                    LIMIT 50
                    """
                ).fetchall()

                for jr in j_rows:
                    note_item = {
                        "entry_id": jr["entry_id"],
                        "title": jr["title"],
                        "status": jr["status"],
                    }
                    all_active_notes.append(note_item)
                    if jr["status"] == "published":
                        journal_notes_list.append(note_item)
                        if len(journal_digest) < 8:
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
                    "all_active_notes": all_active_notes,
                    "all_watched_titles": watched_titles,
                    "rewatch_list": rewatch_list,
                    "all_excluded_titles": excluded_titles,
                    "new_discovery_list": new_discovery_list,
                    "tracked_movies_index": tracked_movies_index,
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
            "all_active_notes": all_active_notes,
            "all_watched_titles": watched_titles,
            "rewatch_list": rewatch_list,
            "all_excluded_titles": excluded_titles,
            "new_discovery_list": new_discovery_list,
            "tracked_movies_index": tracked_movies_index,
        }

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
            return DEFAULT_PRO_MODEL, "Gemini Pro (Deep Dive)"
        return DEFAULT_FLASH_MODEL, "Gemini 3.8 Flash"

    def _resolve_active_skill(
        self,
        message: str,
        current_view: str,
        inspected_note_id: Any,
        active_person: dict[str, Any] | None,
        active_skill_key: str | None,
        history: list[dict[str, str]] | None,
        inspected_movie_id: int | None = None,
    ) -> tuple[str | None, dict[str, Any] | None, str, str]:
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

        active_skill = SKILLS_REGISTRY.get(active_skill_key) if active_skill_key else None
        if active_skill and not user_query:
            user_query = active_skill.get("default_query", user_query)

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
        elif mentions_note_topic:
            skill_directive_text = (
                "### ACTIVE SKILL: READ-ONLY NOTE DISCUSSION\n"
                "- The user is reading, discussing, or asking a question about a personal note/draft.\n"
                "- Use the note content in {{INSPECTED_NOTE_INFO}} (or call `get_note` via `tool_call` if not loaded on screen) to answer conversationally.\n"
                "- STRICT READ-ONLY RULE: You are strictly a conversational partner and critic. Never attempt to edit, create, or overwrite notes."
            )
            return (
                active_skill_key,
                active_skill,
                user_query,
                skill_directive_text,
            )
        elif current_view == "filmography" or (
            active_person and isinstance(active_person, dict) and active_person.get("name")
        ):
            skill_filename = "filmography_explorer.md"
        elif any(
            w in lq
            for w in [
                "related",
                "similar to this",
                "worth my attention",
                "worth my time",
                "recommend from these",
            ]
        ):
            skill_filename = "related_curator.md"
        elif inspected_movie_id or re.search(r"\b(think|thoughts|opinion|critique|review|verdict|worth|good|how is it|is it any good|like this|about this movie|recommend|rubbish|pulse|rate|rt|rotten\s*tomatoes|tomatometer|letterboxd|metacritic|imdb|scores?|ratings?)\b", lq):
            skill_filename = "film_critique.md"

        skill_directive_text = "None"
        if skill_filename:
            skill_path = self.prompts_dir / "skills" / skill_filename
            skill_directive_text = self._read_cached_file(skill_path).strip() or "None"

        return active_skill_key, active_skill, user_query, skill_directive_text

    def _resolve_screen_and_mentioned_context(
        self,
        lower_msg: str,
        inspected_movie_id: int | None,
        inspected_note: dict[str, Any] | None,
        related_movies: list[dict[str, Any]] | None,
        live_movie_notes: str | None,
        dossier: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Resolve open screen movie/note and boundary-matched mentions using RAM dossier cache (0 SQL when unmentioned)."""
        inspected_info = "None"
        inspected_title = None
        live_reception: dict[str, Any] = {}
        ui_had_inspected_movie = bool(inspected_movie_id)
        if dossier is None:
            dossier = self.get_taste_dossier()

        try:
            if not inspected_movie_id:
                # Zero-SQL RAM scan over tracked_movies_index (strict whole-title word-boundary match)
                stopwords = {
                    "time", "good", "dark", "life", "hard", "dead", "part", "find",
                    "movie", "notes", "note", "from", "library", "then", "this", "that",
                    "with", "have", "what", "list", "show", "watch", "seen", "like",
                }
                for r in dossier.get("tracked_movies_index", [])[:200]:
                    t = (r.get("title") or "").lower().strip()
                    t_norm = re.sub(r"^(?:the|a|an)\s+", "", t).strip()
                    matched = False
                    if len(t) >= 4 and t not in stopwords and re.search(rf"\b{re.escape(t)}\b", lower_msg):
                        matched = True
                    elif len(t_norm) >= 5 and t_norm not in stopwords and re.search(rf"\b{re.escape(t_norm)}\b", lower_msg):
                        matched = True

                    if matched:
                        inspected_movie_id = r["tmdb_id"]
                        break

            if inspected_movie_id:
                with self._get_connection() as conn:
                    row = conn.execute(
                        """
                        SELECT m.title, m.release_date, m.vote_average, m.vote_count, u.status, u.verdict, u.notes
                        FROM movies m
                        LEFT JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                        WHERE m.tmdb_id = ?
                        """,
                        (inspected_movie_id,),
                    ).fetchone()
                    if row:
                        inspected_title = row["title"]
                        year_str = f" ({(row['release_date'] or '')[:4]})" if row["release_date"] else ""
                        rel_date = row["release_date"] or ""
                        today_str = datetime.date.today().isoformat()
                        live_reception = self._fetch_live_film_reception(
                            row["title"], (row["release_date"] or "")[:4]
                        )
                        has_live_reviews = bool(live_reception.get("rt_score") or live_reception.get("metacritic"))
                        is_unreleased = False
                        if not has_live_reviews:
                            if rel_date and rel_date > today_str:
                                is_unreleased = True
                            elif not rel_date and (row["vote_count"] or 0) == 0:
                                is_unreleased = True

                        release_tag = f" | Release Date: {rel_date}" if rel_date else ""
                        if is_unreleased:
                            release_tag += " [UPCOMING / UNRELEASED FILM — NOT YET RELEASED]"

                        dir_rows = conn.execute(
                            "SELECT name FROM movie_credits WHERE tmdb_id = ? AND credit_type = 'director' ORDER BY position ASC LIMIT 2",
                            (inspected_movie_id,),
                        ).fetchall()
                        cast_rows = conn.execute(
                            "SELECT name FROM movie_credits WHERE tmdb_id = ? AND credit_type = 'actor' ORDER BY position ASC LIMIT 4",
                            (inspected_movie_id,),
                        ).fetchall()
                        director_str = ", ".join(r["name"] for r in dir_rows) if dir_rows else "Unknown"
                        cast_str = ", ".join(r["name"] for r in cast_rows) if cast_rows else "Unknown"
                        wants_movie_notes = any(
                            w in lower_msg
                            for w in [
                                "note",
                                "notes",
                                "wrote",
                                "write",
                                "from the library",
                                "post",
                                "journal",
                                "entry",
                                "draft",
                                "toggle",
                                "collapse",
                                "format",
                                "append",
                            ]
                        )
                        effective_notes = (
                            live_movie_notes.strip()
                            if ui_had_inspected_movie and live_movie_notes and live_movie_notes.strip()
                            else None
                        ) or row["notes"]
                        notes_part = (
                            f" | User Notes: {effective_notes or 'None'}"
                            if wants_movie_notes
                            else ""
                        )
                        reception_items = []
                        if live_reception.get("rt_score"):
                            reception_items.append(
                                f"Rotten Tomatoes: {live_reception['rt_score']} (Avg {live_reception.get('rt_avg', '')}, {live_reception.get('rt_count', '')} reviews)"
                            )
                        if live_reception.get("rt_consensus"):
                            reception_items.append(f'RT Critics Consensus: "{live_reception["rt_consensus"]}"')
                        if live_reception.get("metacritic"):
                            reception_items.append(f"Metacritic: {live_reception['metacritic']}")
                        if live_reception.get("summary"):
                            reception_items.append(f"Critical Reception Summary: {live_reception['summary'][:350]}")

                        reception_str = ""
                        if reception_items:
                            reception_str = "\n[VERIFIED LIVE CRITICAL RECEPTION (LIVE SEARCH)]:\n" + " | ".join(reception_items)

                        # Zero plot synopsis (and zero user notes unless explicitly requested): Grey cannot parrot the screen
                        inspected_info = (
                            f"{row['title']}{year_str} (TMDB ID: {inspected_movie_id}){release_tag} | "
                            f"Director: {director_str} | Cast: {cast_str} | "
                            f"TMDB Rating {row['vote_average']} (TMDB Votes: {row['vote_count'] or 0}) | "
                            f"Status: {row['status'] or 'unseen'} | "
                            f"User Verdict: {row['verdict'] or 'None'}{notes_part}{reception_str}"
                        )
        except Exception as exc:
            logger.debug("Could not query movie context for Grey: %s", exc)

        # Note context resolution (only open note or explicit full-title match in RAM, 0 SQL when unmentioned)
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
            inspected_note_info = (
                f"Title: {inspected_note_title}{id_str} (Status: {nstatus}{tag_str}) [READ-ONLY DISCUSSION MODE]\n"
                f"Content:\n{nbody[:25000]}"
            )
        else:
            try:
                ram_notes = sorted(
                    dossier.get("all_active_notes") or dossier.get("journal_notes_list", []),
                    key=lambda x: len(x.get("title") or ""),
                    reverse=True,
                )
                matched_entry_id = None
                for mr in ram_notes:
                    m_title = (mr.get("title") or "").strip().lower()
                    if len(m_title) >= 3 and m_title in lower_msg:
                        matched_entry_id = mr["entry_id"]
                        break

                if matched_entry_id is not None:
                    with self._get_connection() as conn:
                        nr = conn.execute(
                            "SELECT entry_id, title, body, status FROM general_entries WHERE entry_id = ? AND is_deleted = 0",
                            (matched_entry_id,),
                        ).fetchone()
                        if nr:
                            inspected_note_id = nr["entry_id"]
                            inspected_note_title = nr["title"]
                            nbody = nr["body"] or ""
                            nstatus = nr["status"] or "published"
                            inspected_note_info = (
                                f"Title: {inspected_note_title} (ID: {inspected_note_id}) "
                                f"(Status: {nstatus}) [READ-ONLY DISCUSSION MODE]\nContent:\n{nbody[:25000]}"
                            )
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
            "inspected_note_id": inspected_note_id,
            "inspected_note_title": inspected_note_title,
            "inspected_note_info": inspected_note_info,
            "related_movies_str": related_movies_str,
            "live_reception": live_reception,
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

        # Prioritize models that haven't hit a 429/404 in the last 5 minutes (saves 3 failed network roundtrips per turn)
        now = time.time()
        healthy_models = [
            m for m in candidate_models if self._model_cooldowns.get(m, 0.0) <= now
        ]
        cooling_models = [
            m for m in candidate_models if self._model_cooldowns.get(m, 0.0) > now
        ]
        ordered_candidates = healthy_models + cooling_models

        resp = None
        model_label = default_label
        # Use persistent TCP/TLS session in production while remaining compatible with monkeypatched requests.post in tests
        post_fn = (
            self.http_session.post
            if getattr(requests.post, "__module__", "") == "requests.api"
            else requests.post
        )
        for model_candidate in ordered_candidates:
            try:
                endpoint = f"{GEMINI_API_BASE_URL}/models/{model_candidate}:generateContent?key={self.api_key}"
                resp = post_fn(
                    endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=14,
                )
                if resp.status_code == 200:
                    self._model_cooldowns.pop(model_candidate, None)
                    model_label = f"Gemini {model_candidate.replace('gemini-', '').capitalize()}"
                    break
                if resp.status_code in (429, 404, 500, 503):
                    self._model_cooldowns[model_candidate] = time.time() + 300.0
                logger.info(
                    f"Model {model_candidate} returned {resp.status_code}, trying next in cascade..."
                )
            except requests.exceptions.Timeout:
                self._model_cooldowns[model_candidate] = time.time() + 300.0
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
            text_chunks = [
                part["text"]
                for part in parts
                if isinstance(part, dict) and "text" in part and part["text"]
            ]
            raw_text = "\n".join(text_chunks)

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
        full_dossier = self.get_taste_dossier()

        ctx = self._resolve_screen_and_mentioned_context(
            lower_msg=lower_msg,
            inspected_movie_id=inspected_movie_id,
            inspected_note=inspected_note,
            related_movies=related_movies,
            live_movie_notes=live_movie_notes,
            dossier=full_dossier,
        )
        inspected_movie_id = ctx["inspected_movie_id"]
        inspected_title = ctx["inspected_title"]
        inspected_info = ctx["inspected_info"]
        inspected_note_id = ctx["inspected_note_id"]
        inspected_note_title = ctx["inspected_note_title"]
        inspected_note_info = ctx["inspected_note_info"]
        related_movies_str = ctx["related_movies_str"]

        (
            active_skill_key,
            active_skill,
            user_query,
            skill_directive_text,
        ) = self._resolve_active_skill(
            message=message,
            current_view=current_view,
            inspected_note_id=inspected_note_id,
            active_person=active_person,
            active_skill_key=active_skill_key,
            history=history,
            inspected_movie_id=ctx.get("inspected_movie_id"),
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
            dossier = full_dossier

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
            .replace("{{AVAILABLE_REACTIONS}}", reactions_index_str)
            .replace("{{FAVORITES_JSON}}", json.dumps(dossier["high_rated"][:5]))
            .replace("{{DISCARDED_COUNT}}", str(dossier["discarded_count"]))
            .replace("{{DISCARDED_SAMPLES_JSON}}", json.dumps(dossier["discarded_samples"][:4]))
            .replace("{{JOURNAL_NOTES_LIST}}", compact_notes_index)
            .replace("{{CURRENT_VIEW}}", current_view)
            .replace("{{ACTIVE_FILTERS_JSON}}", json.dumps(active_filters or {}))
        )

        contents = []
        if history:
            recent_history = history[-16:]
            cutoff_idx = max(0, len(recent_history) - 4)
            for idx, item in enumerate(recent_history):
                role = "user" if item.get("role") == "user" else "model"
                turn_text = item.get("text", "") or ""
                if idx < cutoff_idx and len(turn_text) > 600:
                    turn_text = turn_text[:600] + "\n... [earlier turn truncated]"
                contents.append({"role": role, "parts": [{"text": turn_text}]})

        screen_contexts = []
        if active_person_info != "None":
            screen_contexts.append(f"Filmography on screen: {active_person_info}")
        if notes_shelf_filter:
            screen_contexts.append(f"Movie Notes paired shelf filter: {notes_shelf_filter}")
        if inspected_title:
            id_info = f" (TMDB ID: {inspected_movie_id})" if inspected_movie_id else ""
            screen_contexts.append(f"Currently viewing movie on screen: {inspected_title}{id_info}")
        if inspected_note_title:
            screen_contexts.append(f"Currently viewing note on screen: {inspected_note_title}")

        prefix = f"[{' | '.join(screen_contexts)}]\n" if screen_contexts else ""
        user_content = f"{prefix}{user_query}"
        contents.append({"role": "user", "parts": [{"text": user_content}]})

        payload: dict[str, Any] = {
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "contents": contents,
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.72,
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ],
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

            # Only allow recognized read-only actions (open_movie, apply_filter, tool_call)
            if isinstance(action, dict) and action.get("type") not in ("open_movie", "apply_filter", "tool_call"):
                action = None

            pills = data.get("pills", [])

            reaction = data.get("reaction")
            valid_reaction = None
            if reaction and isinstance(reaction, str):
                reaction_filename = Path(reaction).name
                reaction_path = self.reactions_dir / reaction_filename
                if reaction_path.exists() and reaction_path.is_file():
                    valid_reaction = reaction_filename

            # Filter out unsolicited shelf categorization pills and unsolicited other-movie recommendations
            sanitized_pills = []
            for p in pills or []:
                if not isinstance(p, dict):
                    continue
                lbl = (p.get("label") or "").lower()
                act = p.get("action")
                payload_st = str((p.get("payload") or {}).get("status", "")).lower()
                is_status_pill = (
                    act in ("set_movie_status", "batch_set_movie_status")
                    or payload_st
                    in ("watch_later", "new_discovery", "watched", "rewatch", "excluded")
                    or any(
                        s in lbl for s in ["watchlist", "new discovery", "add to shelf", "mark as"]
                    )
                )
                is_unsolicited_rec = (
                    act == "open_movie"
                    and not any(w in lower_msg for w in ["recommend", "instead", "similar", "more like", "alternative", "suggest", "better", "what should i watch"])
                )
                if not is_status_pill and not is_unsolicited_rec:
                    sanitized_pills.append(p)

            # Strip all third-party rating pills from LLM response (scoreboards belong in Movie Details)
            sanitized_pills = [
                p
                for p in sanitized_pills
                if not any(
                    tag in (p.get("label") or "")
                    for tag in ["RT:", "IMDb:", "Letterboxd:", "Metacritic:"]
                )
            ]

            pills = sanitized_pills

            text = (data.get("text") or "Here are the matching titles from your library.").strip()
            # Defensive clean: strip accidental score-reciting clauses from prose (e.g. ", holding an 87% on Rotten Tomatoes...")
            text = re.sub(
                r',?\s*(?:holding|with|boasting|carrying)\s+(?:an?\s+)?\d+%\s+on\s+Rotten\s+Tomatoes(?:\s+and\s+(?:an?\s+)?\d+(?:/100)?\s+on\s+Metacritic)?\.?',
                '.',
                text,
                flags=re.IGNORECASE,
            ).strip()
            # Defensive clean: if Gemini leaked raw JSON arrays into text, extract them to pills and strip from text
            leaked_json_match = re.search(r'\[\s*\{.*?"label"\s*:.*?\}\s*\]', text, re.DOTALL)
            if leaked_json_match:
                try:
                    leaked_data = json.loads(leaked_json_match.group(0))
                    if isinstance(leaked_data, list) and not pills:
                        pills = leaked_data
                except Exception:
                    pass
                text = text[:leaked_json_match.start()].strip()

            return {
                "text": text,
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
