import re
from typing import Any

from app.database import get_connection
from app.movie_status import MovieStatus, validate_movie_status

_ACRONYM_DOT_RE = re.compile(r"\b([a-zA-Z])(?:\.([a-zA-Z]))+\.?")
_PREFIX_QUERY_RE = re.compile(r"^(title|plot|notes?)\s*:\s*(.*)$", re.IGNORECASE)
_WORD_TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def _normalize_search_text(text: str | None) -> str:
    if not text:
        return ""
    collapsed_acronyms = _ACRONYM_DOT_RE.sub(
        lambda m: m.group(0).replace(".", ""),
        str(text),
    )
    return " ".join(collapsed_acronyms.split()).lower()


def _parse_library_search_query(raw_query: str | None) -> tuple[str, str]:
    cleaned = " ".join((raw_query or "").split())
    if not cleaned:
        return "all", ""
    match = _PREFIX_QUERY_RE.match(cleaned)
    if match:
        prefix = match.group(1).lower()
        mode = "notes" if prefix in ("note", "notes") else prefix
        term = " ".join((match.group(2) or "").split())
        return mode, term
    return "all", cleaned


def _build_word_boundary_pattern(normalized_term: str) -> re.Pattern | None:
    if not normalized_term:
        return None
    tokens = _WORD_TOKEN_RE.findall(normalized_term)
    if tokens:
        joined = r"[\s\-_:,.;!?'\"/()+]+".join(re.escape(t) for t in tokens)
        pattern_str = rf"(?<![a-z0-9]){joined}(?![a-z0-9])"
    else:
        pattern_str = re.escape(normalized_term)
    return re.compile(pattern_str, re.IGNORECASE)


def _stem_search_word(word: str) -> str:
    w = word.lower().strip()
    for s in ("ence", "ency", "ent", "ing", "tion", "able", "ible", "ical"):
        if len(w) > 5 and w.endswith(s):
            return w[:-len(s)]
    for s in ("es", "ed", "er", "ly"):
        if len(w) > 4 and w.endswith(s):
            return w[:-len(s)]
    if len(w) > 3 and w.endswith("s"):
        return w[:-1]
    return w


def _text_matches_term(norm_term: str, norm_text: str, pattern: re.Pattern | None = None) -> bool:
    if not norm_term or not norm_text:
        return False
    if norm_term in norm_text:
        return True
    if pattern and pattern.search(norm_text):
        return True
    q_tokens = _WORD_TOKEN_RE.findall(norm_term)
    if not q_tokens:
        return False
    text_tokens = _WORD_TOKEN_RE.findall(norm_text)
    if not text_tokens:
        return False
    if len(q_tokens) == 1:
        q_stem = _stem_search_word(q_tokens[0])
        if len(q_stem) >= 4:
            for tt in text_tokens:
                t_stem = _stem_search_word(tt)
                if len(t_stem) >= 4:
                    if q_stem == t_stem or t_stem.startswith(q_stem) or q_stem.startswith(t_stem):
                        return True
    return False


class MovieRepository:
    PAGE_SIZE = 20

    def save_movie(self, movie: dict[str, Any]) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO movies (
                    tmdb_id,
                    title,
                    original_title,
                    release_date,
                    overview,
                    poster_path,
                    backdrop_path,
                    vote_average,
                    vote_count,
                    original_language,
                    fetched_at,
                    last_accessed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(tmdb_id) DO UPDATE SET
                    title = excluded.title,
                    original_title = excluded.original_title,
                    release_date = excluded.release_date,
                    overview = excluded.overview,
                    poster_path = excluded.poster_path,
                    backdrop_path = excluded.backdrop_path,
                    vote_average = excluded.vote_average,
                    vote_count = excluded.vote_count,
                    original_language = excluded.original_language,
                    fetched_at = CURRENT_TIMESTAMP,
                    last_accessed_at = CURRENT_TIMESTAMP
                """,
                (
                    movie.get("id") or movie.get("tmdb_id"),
                    movie.get("title") or movie.get("original_title") or "Untitled movie",
                    movie.get("original_title"),
                    movie.get("release_date"),
                    movie.get("overview"),
                    movie.get("poster_path"),
                    movie.get("backdrop_path"),
                    movie.get("vote_average"),
                    movie.get("vote_count") or 0,
                    movie.get("original_language"),
                ),
            )

    def get_movie(self, tmdb_id: int) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM movies
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            ).fetchone()

        if row is None:
            return None

        return dict(row)

    def touch_movie(self, tmdb_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE movies
                SET last_accessed_at = CURRENT_TIMESTAMP
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            )

    def get_movies_by_ids(
        self,
        tmdb_ids: list[int],
    ) -> list[dict]:
        unique_ids = list(dict.fromkeys(tmdb_ids))

        if not unique_ids:
            return []

        placeholders = ",".join("?" for _ in unique_ids)

        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT *
                FROM movies
                WHERE tmdb_id IN ({placeholders})
                """,
                unique_ids,
            ).fetchall()

        movies_by_id = {
            row["tmdb_id"]: dict(row)
            for row in rows
        }
        return [
            movies_by_id[tmdb_id]
            for tmdb_id in unique_ids
            if tmdb_id in movies_by_id
        ]

    def search_movies(self, query: str) -> list[dict]:
        cleaned = " ".join((query or "").split())
        if not cleaned:
            return []
        exact = cleaned
        starts = f"{cleaned}%"
        contains = f"%{cleaned}%"
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM movies
                WHERE title LIKE ? COLLATE NOCASE
                   OR original_title LIKE ? COLLATE NOCASE
                ORDER BY
                    CASE
                        WHEN lower(title) = lower(?) THEN 1
                        WHEN title LIKE ? COLLATE NOCASE THEN 2
                        WHEN title LIKE ? COLLATE NOCASE THEN 3
                        ELSE 4
                    END ASC,
                    title COLLATE NOCASE ASC
                """,
                (contains, contains, exact, starts, contains),
            ).fetchall()

        return [dict(row) for row in rows]

    def search_user_library(
        self,
        query: str = "",
        status: str | None = None,
    ) -> list[dict]:
        field_mode, search_term = _parse_library_search_query(query)
        normalized_term = _normalize_search_text(search_term)
        pattern = _build_word_boundary_pattern(normalized_term)

        raw_subterms = [t.strip() for t in search_term.split(",") if t.strip()]
        is_multi_term = len(raw_subterms) > 1
        subterm_patterns = [
            (
                _normalize_search_text(t),
                _build_word_boundary_pattern(_normalize_search_text(t)),
            )
            for t in raw_subterms
            if _normalize_search_text(t)
        ]

        where_parts: list[str] = []
        where_params: list[Any] = []

        effective_status = status
        if status and status.startswith("movie-notes:"):
            where_parts.append("u.notes IS NOT NULL AND TRIM(u.notes) <> ''")
            effective_status = status.split(":", 1)[1].strip() or None

        if effective_status:
            if effective_status == "favorites":
                where_parts.append("u.is_favorite = 1 AND u.status IN ('watched', 'rewatch')")
            elif effective_status == "movie-notes":
                where_parts.append("u.notes IS NOT NULL AND TRIM(u.notes) <> ''")
            elif effective_status == "watched":
                where_parts.append("u.status IN ('watched', 'rewatch')")
            else:
                target_status = "excluded" if effective_status == "nope" else effective_status
                validated_status = validate_movie_status(target_status)
                where_parts.append("u.status = ?")
                where_params.append(validated_status)
        elif not (status and status.startswith("movie-notes:")):
            where_parts.append("(u.status IS NOT NULL OR u.is_favorite = 1 OR (u.notes IS NOT NULL AND TRIM(u.notes) <> ''))")

        where_clause = " AND ".join(where_parts) if where_parts else "1=1"

        with get_connection() as connection:
            if not normalized_term or pattern is None:
                rows = connection.execute(
                    f"""
                    SELECT m.*
                    FROM movies m
                    JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                    WHERE {where_clause}
                    ORDER BY m.title COLLATE NOCASE ASC
                    """,
                    tuple(where_params),
                ).fetchall()
                return [dict(row) for row in rows]

            rows = connection.execute(
                f"""
                SELECT
                    m.*,
                    u.notes AS _user_notes,
                    GROUP_CONCAT(DISTINCT k.name) AS _keyword_names,
                    GROUP_CONCAT(DISTINCT g.name) AS _genre_names
                FROM movies m
                JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                LEFT JOIN movie_keywords mk ON m.tmdb_id = mk.tmdb_id
                LEFT JOIN keywords k ON mk.keyword_id = k.keyword_id
                LEFT JOIN movie_genres mg ON m.tmdb_id = mg.tmdb_id
                LEFT JOIN genres g ON mg.tmdb_genre_id = g.tmdb_genre_id
                WHERE {where_clause}
                GROUP BY m.tmdb_id
                """,
                tuple(where_params),
            ).fetchall()

        effective_field_mode = field_mode
        if field_mode == "all" and status and status.startswith("movie-notes"):
            effective_field_mode = "notes"

        ranked_results: list[tuple[int, int, str, dict[str, Any]]] = []
        for row in rows:
            movie = dict(row)
            user_notes = movie.pop("_user_notes", None)
            raw_keywords = movie.pop("_keyword_names", None) or ""
            keyword_list = [kw for kw in raw_keywords.split(",") if kw]
            raw_genres = movie.pop("_genre_names", None) or ""
            genre_list = [g for g in raw_genres.split(",") if g]

            norm_title = _normalize_search_text(movie.get("title"))
            norm_orig_title = _normalize_search_text(movie.get("original_title"))
            norm_overview = _normalize_search_text(movie.get("overview"))
            norm_notes = _normalize_search_text(user_notes)
            norm_keywords = [_normalize_search_text(kw) for kw in keyword_list if kw]
            norm_genres = [_normalize_search_text(g) for g in genre_list if g]

            tier: int | None = None
            subtier = 0

            if is_multi_term:
                matches_all = True
                for norm_sub, sub_pat in subterm_patterns:
                    if not sub_pat:
                        continue
                    term_matched = False
                    if effective_field_mode == "title":
                        term_matched = bool(
                            norm_title == norm_sub
                            or (norm_orig_title and norm_orig_title == norm_sub)
                            or sub_pat.search(norm_title)
                            or (norm_orig_title and sub_pat.search(norm_orig_title))
                        )
                    elif effective_field_mode == "plot":
                        term_matched = bool(sub_pat.search(norm_overview))
                    elif effective_field_mode == "notes":
                        term_matched = bool(
                            _text_matches_term(norm_sub, norm_notes, sub_pat)
                            or _text_matches_term(norm_sub, norm_title, sub_pat)
                            or (norm_orig_title and _text_matches_term(norm_sub, norm_orig_title, sub_pat))
                            or any(_text_matches_term(norm_sub, g, sub_pat) for g in norm_genres)
                        )
                    else:
                        term_matched = bool(
                            _text_matches_term(norm_sub, norm_title, sub_pat)
                            or (norm_orig_title and _text_matches_term(norm_sub, norm_orig_title, sub_pat))
                            or _text_matches_term(norm_sub, norm_overview, sub_pat)
                            or _text_matches_term(norm_sub, norm_notes, sub_pat)
                            or any(kw == norm_sub or _text_matches_term(norm_sub, kw, sub_pat) for kw in norm_keywords)
                            or any(_text_matches_term(norm_sub, g, sub_pat) for g in norm_genres)
                        )
                    if not term_matched:
                        matches_all = False
                        break

                if matches_all:
                    tier = 4 if effective_field_mode == "notes" else 2
                    subtier = 0
            elif effective_field_mode == "title":
                if norm_title == normalized_term or (norm_orig_title and norm_orig_title == normalized_term):
                    tier = 1
                elif pattern.search(norm_title) or (norm_orig_title and pattern.search(norm_orig_title)):
                    tier = 2
                    subtier = 0 if norm_title.startswith(normalized_term) else 1
            elif effective_field_mode == "plot":
                if pattern.search(norm_overview):
                    tier = 3
            elif effective_field_mode == "notes":
                if _text_matches_term(normalized_term, norm_notes, pattern):
                    tier = 4
            else:
                if norm_title == normalized_term or (norm_orig_title and norm_orig_title == normalized_term):
                    tier = 1
                elif pattern.search(norm_title) or (norm_orig_title and pattern.search(norm_orig_title)):
                    tier = 2
                    subtier = 0 if norm_title.startswith(normalized_term) else 1
                elif pattern.search(norm_overview):
                    tier = 3
                elif pattern.search(norm_notes):
                    tier = 4
                elif any(kw == normalized_term for kw in norm_keywords):
                    tier = 5
                    subtier = 0
                elif any(pattern.search(kw) for kw in norm_keywords):
                    tier = 5
                    subtier = 1

            if tier is not None:
                movie["search_tier"] = tier
                movie["search_subtier"] = subtier
                ranked_results.append((tier, subtier, norm_title, movie))

        ranked_results.sort(key=lambda item: (item[0], item[1], item[2]))
        return [item[3] for item in ranked_results]

    def get_watched_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status IN (?, ?)
                ORDER BY m.title
                """,
                (
                    MovieStatus.WATCHED.value,
                    MovieStatus.REWATCH.value,
                ),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_watchlist_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status = ?
                ORDER BY m.title
                """,
                (MovieStatus.WATCH_LATER.value,),
            ).fetchall()

        return [dict(row) for row in rows]
    
    def get_rewatch_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status = ?
                ORDER BY m.title
                """,
                (MovieStatus.REWATCH.value,),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_excluded_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status = ?
                ORDER BY m.title
                """,
                (MovieStatus.EXCLUDED.value,),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_favorite_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.is_favorite = 1
                  AND u.status IN (?, ?)
                ORDER BY m.title
                """,
                (
                    MovieStatus.WATCHED.value,
                    MovieStatus.REWATCH.value,
                ),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_new_discovery_movies(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status = ?
                ORDER BY m.title
                """,
                (MovieStatus.NEW_DISCOVERY.value,),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_movies_by_status(
        self,
        status: str | MovieStatus,
    ) -> list[dict]:
        validated_status = validate_movie_status(status)

        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u
                    ON m.tmdb_id = u.tmdb_id
                WHERE u.status = ?
                ORDER BY m.title
                """,
                (validated_status,),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_movies_by_status_page(
        self,
        status: str | MovieStatus,
        page: int = 1,
        page_size: int = PAGE_SIZE,
    ) -> dict:
        validated_status = validate_movie_status(status)
        return self._get_user_movie_page(
            "u.status = ?",
            (validated_status,),
            page,
            page_size=page_size,
        )

    def get_watched_movies_page(self, page: int = 1, page_size: int = PAGE_SIZE) -> dict:
        return self._get_user_movie_page(
            "u.status IN (?, ?)",
            (MovieStatus.WATCHED.value, MovieStatus.REWATCH.value),
            page,
            page_size=page_size,
        )

    def get_favorite_movies_page(self, page: int = 1, page_size: int = PAGE_SIZE) -> dict:
        return self._get_user_movie_page(
            "u.is_favorite = 1 AND u.status IN (?, ?)",
            (MovieStatus.WATCHED.value, MovieStatus.REWATCH.value),
            page,
            page_size=page_size,
        )

    def get_movies_with_notes_page(self, page: int = 1, page_size: int = PAGE_SIZE) -> dict:
        return self._get_user_movie_page(
            "u.notes IS NOT NULL AND TRIM(u.notes) <> ''",
            (),
            page,
            page_size=page_size,
        )

    def _get_user_movie_page(
        self,
        where_clause: str,
        parameters: tuple,
        page: int,
        page_size: int = PAGE_SIZE,
    ) -> dict:
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ValueError("Movie page must be at least 1.")
        if isinstance(page_size, bool) or not isinstance(page_size, int) or page_size < 1:
            page_size = self.PAGE_SIZE
        offset = (page - 1) * page_size
        with get_connection() as connection:
            total = connection.execute(
                f"""
                SELECT COUNT(*)
                FROM movies m
                JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                WHERE {where_clause}
                """,
                parameters,
            ).fetchone()[0]
            rows = connection.execute(
                f"""
                SELECT m.*
                FROM movies m
                JOIN user_movie_data u ON m.tmdb_id = u.tmdb_id
                WHERE {where_clause}
                ORDER BY m.title COLLATE NOCASE, m.tmdb_id
                LIMIT ? OFFSET ?
                """,
                (*parameters, page_size, offset),
            ).fetchall()
        return {
            "page": page,
            "page_size": page_size,
            "total_results": total,
            "total_pages": max(1, (total + page_size - 1) // page_size),
            "results": [dict(row) for row in rows],
        }

    def mark_metadata_fetched(self, tmdb_id: int) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE movies
                SET metadata_fetched_at = CURRENT_TIMESTAMP,
                    metadata_version = 2
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            )
