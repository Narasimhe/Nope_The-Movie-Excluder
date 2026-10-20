from typing import Any

from app.database import get_connection


MAX_TMDB_KEYWORDS = 10
MAX_MAIN_ACTORS = 5


class MovieMetadataRepository:
    def _validate_movie_id(self, tmdb_id: int) -> None:
        if isinstance(tmdb_id, bool) or not isinstance(tmdb_id, int):
            raise ValueError("TMDB movie ID must be an integer.")

        if tmdb_id <= 0:
            raise ValueError("TMDB movie ID must be greater than zero.")

    def _clean_name(self, name: Any, label: str) -> str:
        if not isinstance(name, str):
            raise ValueError(f"{label} name must be text.")

        cleaned_name = " ".join(name.split())

        if not cleaned_name:
            raise ValueError(f"{label} name cannot be empty.")

        return cleaned_name

    def _validate_keyword_id(self, keyword_id: int) -> None:
        if (
            isinstance(keyword_id, bool)
            or not isinstance(keyword_id, int)
        ):
            raise ValueError("Keyword ID must be an integer.")

        if keyword_id <= 0:
            raise ValueError("Keyword ID must be greater than zero.")

    def _normalize_tmdb_items(
        self,
        items: list[dict[str, Any]],
        label: str,
        limit: int | None = None,
    ) -> list[tuple[int, str]]:
        normalized_items: list[tuple[int, str]] = []
        seen_ids: set[int] = set()

        for item in items:
            item_id = item.get("id")

            if isinstance(item_id, bool) or not isinstance(item_id, int):
                raise ValueError(f"{label} ID must be an integer.")

            if item_id <= 0:
                raise ValueError(
                    f"{label} ID must be greater than zero."
                )

            if item_id in seen_ids:
                continue

            item_name = self._clean_name(item.get("name"), label)
            normalized_items.append((item_id, item_name))
            seen_ids.add(item_id)

            if limit is not None and len(normalized_items) == limit:
                break

        return normalized_items

    def replace_movie_genres(
        self,
        tmdb_id: int,
        genres: list[dict[str, Any]],
    ) -> list[dict]:
        self._validate_movie_id(tmdb_id)
        normalized_genres = self._normalize_tmdb_items(
            genres,
            "Genre",
        )

        with get_connection() as connection:
            connection.execute(
                """
                DELETE FROM movie_genres
                WHERE tmdb_id = ?
                """,
                (tmdb_id,),
            )

            for genre_id, genre_name in normalized_genres:
                connection.execute(
                    """
                    INSERT INTO genres (tmdb_genre_id, name)
                    VALUES (?, ?)
                    ON CONFLICT(tmdb_genre_id) DO UPDATE SET
                        name = excluded.name
                    """,
                    (genre_id, genre_name),
                )
                connection.execute(
                    """
                    INSERT INTO movie_genres (
                        tmdb_id,
                        tmdb_genre_id
                    )
                    VALUES (?, ?)
                    """,
                    (tmdb_id, genre_id),
                )

        return self.get_movie_genres(tmdb_id)

    def get_movie_genres(self, tmdb_id: int) -> list[dict]:
        self._validate_movie_id(tmdb_id)

        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    g.tmdb_genre_id,
                    g.name
                FROM genres g
                JOIN movie_genres mg
                    ON g.tmdb_genre_id = mg.tmdb_genre_id
                WHERE mg.tmdb_id = ?
                ORDER BY g.name COLLATE NOCASE
                """,
                (tmdb_id,),
            ).fetchall()

        return [dict(row) for row in rows]

    def get_movie_genres_bulk(
        self,
        tmdb_ids: list[int],
    ) -> dict[int, list[dict]]:
        unique_ids = list(dict.fromkeys(tmdb_ids))

        if not unique_ids:
            return {}

        for tmdb_id in unique_ids:
            self._validate_movie_id(tmdb_id)

        placeholders = ",".join("?" for _ in unique_ids)

        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT
                    mg.tmdb_id,
                    g.tmdb_genre_id,
                    g.name
                FROM movie_genres mg
                JOIN genres g
                    ON mg.tmdb_genre_id = g.tmdb_genre_id
                WHERE mg.tmdb_id IN ({placeholders})
                ORDER BY
                    mg.tmdb_id,
                    g.name COLLATE NOCASE
                """,
                unique_ids,
            ).fetchall()

        results = {
            tmdb_id: []
            for tmdb_id in unique_ids
        }

        for row in rows:
            results[row["tmdb_id"]].append(
                {
                    "tmdb_genre_id": row["tmdb_genre_id"],
                    "name": row["name"],
                }
            )

        return results

    def replace_tmdb_keywords(
        self,
        tmdb_id: int,
        keywords: list[dict[str, Any]],
    ) -> list[dict]:
        self._validate_movie_id(tmdb_id)
        normalized_keywords = self._normalize_tmdb_items(
            keywords,
            "Keyword",
            limit=MAX_TMDB_KEYWORDS,
        )

        with get_connection() as connection:
            connection.execute(
                """
                DELETE FROM movie_keywords
                WHERE tmdb_id = ?
                  AND keyword_id IN (
                      SELECT keyword_id
                      FROM keywords
                      WHERE is_custom = 0
                  )
                """,
                (tmdb_id,),
            )

            for position, keyword in enumerate(
                normalized_keywords,
                start=1,
            ):
                keyword_id, keyword_name = keyword
                connection.execute(
                    """
                    INSERT INTO keywords (
                        tmdb_keyword_id,
                        name,
                        is_custom
                    )
                    VALUES (?, ?, 0)
                    ON CONFLICT(tmdb_keyword_id) DO UPDATE SET
                        name = excluded.name
                    """,
                    (keyword_id, keyword_name),
                )
                row = connection.execute(
                    """
                    SELECT keyword_id
                    FROM keywords
                    WHERE tmdb_keyword_id = ?
                      AND is_custom = 0
                    """,
                    (keyword_id,),
                ).fetchone()

                if row is None:
                    raise RuntimeError(
                        "Official TMDB keyword could not be saved."
                    )

                connection.execute(
                    """
                    INSERT INTO movie_keywords (
                        tmdb_id,
                        keyword_id,
                        position
                    )
                    VALUES (?, ?, ?)
                    """,
                    (tmdb_id, row["keyword_id"], position),
                )

            connection.execute(
                """
                DELETE FROM keywords
                WHERE is_custom = 0
                  AND NOT EXISTS (
                      SELECT 1
                      FROM movie_keywords mk
                      WHERE mk.keyword_id = keywords.keyword_id
                  )
                """
            )

        return self.get_tmdb_keywords(tmdb_id)

    def add_custom_keyword(
        self,
        tmdb_id: int,
        name: str,
    ) -> dict:
        self._validate_movie_id(tmdb_id)
        cleaned_name = self._clean_name(name, "Custom keyword")

        with get_connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO keywords (
                    tmdb_keyword_id,
                    name,
                    is_custom
                )
                VALUES (NULL, ?, 1)
                """,
                (cleaned_name,),
            )
            row = connection.execute(
                """
                SELECT keyword_id
                FROM keywords
                WHERE is_custom = 1
                  AND name = ? COLLATE NOCASE
                """,
                (cleaned_name,),
            ).fetchone()

            if row is None:
                raise RuntimeError(
                    "Custom keyword could not be saved."
                )

            keyword_id = row["keyword_id"]
            connection.execute(
                """
                INSERT INTO movie_keywords (
                    tmdb_id,
                    keyword_id,
                    position
                )
                VALUES (?, ?, NULL)
                ON CONFLICT(tmdb_id, keyword_id) DO NOTHING
                """,
                (tmdb_id, keyword_id),
            )

        keyword = self._get_movie_keyword(tmdb_id, keyword_id)

        if keyword is None:
            raise RuntimeError(
                "Custom keyword link could not be read."
            )

        return keyword

    def remove_custom_keyword(
        self,
        tmdb_id: int,
        keyword_id: int,
    ) -> bool:
        self._validate_movie_id(tmdb_id)
        self._validate_keyword_id(keyword_id)

        with get_connection() as connection:
            cursor = connection.execute(
                """
                DELETE FROM movie_keywords
                WHERE tmdb_id = ?
                  AND keyword_id = ?
                  AND keyword_id IN (
                      SELECT keyword_id
                      FROM keywords
                      WHERE is_custom = 1
                  )
                """,
                (tmdb_id, keyword_id),
            )
            removed = cursor.rowcount > 0
            connection.execute(
                """
                DELETE FROM keywords
                WHERE keyword_id = ?
                  AND is_custom = 1
                  AND NOT EXISTS (
                      SELECT 1
                      FROM movie_keywords mk
                      WHERE mk.keyword_id = keywords.keyword_id
                  )
                """,
                (keyword_id,),
            )

        return removed

    def delete_custom_keyword(
        self,
        keyword_id: int,
    ) -> dict | None:
        self._validate_keyword_id(keyword_id)

        with get_connection() as connection:
            keyword = connection.execute(
                """
                SELECT
                    keyword_id,
                    name
                FROM keywords
                WHERE keyword_id = ?
                  AND is_custom = 1
                """,
                (keyword_id,),
            ).fetchone()

            if keyword is None:
                return None

            affected_movie_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM movie_keywords
                WHERE keyword_id = ?
                """,
                (keyword_id,),
            ).fetchone()[0]

            # Delete links explicitly because SQLite foreign-key cascades
            # may be disabled in an existing local database connection.
            connection.execute(
                """
                DELETE FROM movie_keywords
                WHERE keyword_id = ?
                """,
                (keyword_id,),
            )
            connection.execute(
                """
                DELETE FROM keywords
                WHERE keyword_id = ?
                  AND is_custom = 1
                """,
                (keyword_id,),
            )

        return {
            "keyword_id": keyword["keyword_id"],
            "name": keyword["name"],
            "is_custom": True,
            "affected_movie_count": affected_movie_count,
        }

    def rename_custom_keyword(
        self,
        keyword_id: int,
        name: str,
    ) -> dict | None:
        self._validate_keyword_id(keyword_id)
        cleaned_name = self._clean_name(name, "Custom keyword")

        with get_connection() as connection:
            keyword = connection.execute(
                """
                SELECT
                    keyword_id,
                    name
                FROM keywords
                WHERE keyword_id = ?
                  AND is_custom = 1
                """,
                (keyword_id,),
            ).fetchone()

            if keyword is None:
                return None

            affected_movie_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM movie_keywords
                WHERE keyword_id = ?
                """,
                (keyword_id,),
            ).fetchone()[0]

            existing_keyword = connection.execute(
                """
                SELECT
                    keyword_id,
                    name
                FROM keywords
                WHERE is_custom = 1
                  AND name = ? COLLATE NOCASE
                  AND keyword_id != ?
                """,
                (cleaned_name, keyword_id),
            ).fetchone()

            if existing_keyword is None:
                connection.execute(
                    """
                    UPDATE keywords
                    SET name = ?
                    WHERE keyword_id = ?
                      AND is_custom = 1
                    """,
                    (cleaned_name, keyword_id),
                )

                return {
                    "action": "renamed",
                    "keyword_id": keyword_id,
                    "name": cleaned_name,
                    "previous_name": keyword["name"],
                    "is_custom": True,
                    "affected_movie_count": affected_movie_count,
                    "merged_from_keyword_id": None,
                }

            surviving_keyword_id = existing_keyword["keyword_id"]
            connection.execute(
                """
                INSERT INTO movie_keywords (
                    tmdb_id,
                    keyword_id,
                    position
                )
                SELECT
                    tmdb_id,
                    ?,
                    NULL
                FROM movie_keywords
                WHERE keyword_id = ?
                ON CONFLICT(tmdb_id, keyword_id) DO NOTHING
                """,
                (surviving_keyword_id, keyword_id),
            )
            connection.execute(
                """
                DELETE FROM movie_keywords
                WHERE keyword_id = ?
                """,
                (keyword_id,),
            )
            connection.execute(
                """
                DELETE FROM keywords
                WHERE keyword_id = ?
                  AND is_custom = 1
                """,
                (keyword_id,),
            )

            return {
                "action": "merged",
                "keyword_id": surviving_keyword_id,
                "name": existing_keyword["name"],
                "previous_name": keyword["name"],
                "is_custom": True,
                "affected_movie_count": affected_movie_count,
                "merged_from_keyword_id": keyword_id,
            }

    def _get_movie_keyword(
        self,
        tmdb_id: int,
        keyword_id: int,
    ) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    k.keyword_id,
                    k.tmdb_keyword_id,
                    k.name,
                    k.is_custom,
                    mk.position
                FROM keywords k
                JOIN movie_keywords mk
                    ON k.keyword_id = mk.keyword_id
                WHERE mk.tmdb_id = ?
                  AND k.keyword_id = ?
                """,
                (tmdb_id, keyword_id),
            ).fetchone()

        if row is None:
            return None

        result = dict(row)
        result["is_custom"] = bool(result["is_custom"])
        return result

    def get_movie_keywords(self, tmdb_id: int) -> list[dict]:
        self._validate_movie_id(tmdb_id)

        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    k.keyword_id,
                    k.tmdb_keyword_id,
                    k.name,
                    k.is_custom,
                    mk.position
                FROM keywords k
                JOIN movie_keywords mk
                    ON k.keyword_id = mk.keyword_id
                WHERE mk.tmdb_id = ?
                ORDER BY
                    k.is_custom,
                    mk.position,
                    k.name COLLATE NOCASE
                """,
                (tmdb_id,),
            ).fetchall()

        results = [dict(row) for row in rows]

        for result in results:
            result["is_custom"] = bool(result["is_custom"])

        return results

    def get_tmdb_keywords(self, tmdb_id: int) -> list[dict]:
        return [
            keyword
            for keyword in self.get_movie_keywords(tmdb_id)
            if not keyword["is_custom"]
        ]

    def get_custom_keywords(self, tmdb_id: int) -> list[dict]:
        return [
            keyword
            for keyword in self.get_movie_keywords(tmdb_id)
            if keyword["is_custom"]
        ]

    def replace_movie_credits(
        self,
        tmdb_id: int,
        credits: dict[str, Any],
    ) -> dict[str, list[dict]]:
        self._validate_movie_id(tmdb_id)
        if not isinstance(credits, dict):
            raise ValueError("Movie credits must be an object.")

        directors = []
        seen_directors = set()
        for person in credits.get("crew") or []:
            if str(person.get("job") or "").casefold() != "director":
                continue
            person_id = person.get("id")
            if (
                isinstance(person_id, bool)
                or not isinstance(person_id, int)
                or person_id <= 0
                or person_id in seen_directors
            ):
                continue
            name = self._clean_name(person.get("name"), "Director")
            directors.append((person_id, name, None))
            seen_directors.add(person_id)

        actors = []
        seen_actors = set()
        cast = sorted(
            credits.get("cast") or [],
            key=lambda person: person.get("order", 999999),
        )
        for person in cast:
            person_id = person.get("id")
            if (
                isinstance(person_id, bool)
                or not isinstance(person_id, int)
                or person_id <= 0
                or person_id in seen_actors
            ):
                continue
            name = self._clean_name(person.get("name"), "Actor")
            character = " ".join(str(person.get("character") or "").split())
            actors.append((person_id, name, character or None))
            seen_actors.add(person_id)
            if len(actors) == MAX_MAIN_ACTORS:
                break

        with get_connection() as connection:
            connection.execute(
                "DELETE FROM movie_credits WHERE tmdb_id = ?",
                (tmdb_id,),
            )
            for position, (person_id, name, character) in enumerate(
                directors, start=1
            ):
                connection.execute(
                    """
                    INSERT INTO movie_credits (
                        tmdb_id, tmdb_person_id, name, credit_type,
                        character_name, position
                    )
                    VALUES (?, ?, ?, 'director', ?, ?)
                    """,
                    (tmdb_id, person_id, name, character, position),
                )
            for position, (person_id, name, character) in enumerate(
                actors, start=1
            ):
                connection.execute(
                    """
                    INSERT INTO movie_credits (
                        tmdb_id, tmdb_person_id, name, credit_type,
                        character_name, position
                    )
                    VALUES (?, ?, ?, 'actor', ?, ?)
                    """,
                    (tmdb_id, person_id, name, character, position),
                )

        return self.get_movie_credits(tmdb_id)

    def get_movie_credits(self, tmdb_id: int) -> dict[str, list[dict]]:
        self._validate_movie_id(tmdb_id)
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT tmdb_person_id, name, credit_type,
                       character_name, position
                FROM movie_credits
                WHERE tmdb_id = ?
                ORDER BY credit_type DESC, position
                """,
                (tmdb_id,),
            ).fetchall()
        result = {"directors": [], "actors": []}
        for row in rows:
            credit = {
                "tmdb_person_id": row["tmdb_person_id"],
                "name": row["name"],
                "character": row["character_name"],
                "position": row["position"],
            }
            key = "directors" if row["credit_type"] == "director" else "actors"
            result[key].append(credit)
        return result

    def get_movie_credits_bulk(
        self, tmdb_ids: list[int]
    ) -> dict[int, dict[str, list[dict]]]:
        if not tmdb_ids:
            return {}
        result: dict[int, dict[str, list[dict]]] = {
            mid: {"directors": [], "actors": []} for mid in tmdb_ids
        }
        placeholders = ",".join("?" for _ in tmdb_ids)
        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT tmdb_id, tmdb_person_id, name, credit_type,
                       character_name, position
                FROM movie_credits
                WHERE tmdb_id IN ({placeholders})
                ORDER BY credit_type DESC, position
                """,
                tuple(tmdb_ids),
            ).fetchall()
        for row in rows:
            mid = row["tmdb_id"]
            if mid not in result:
                result[mid] = {"directors": [], "actors": []}
            credit = {
                "tmdb_person_id": row["tmdb_person_id"],
                "name": row["name"],
                "character": row["character_name"],
                "position": row["position"],
            }
            key = "directors" if row["credit_type"] == "director" else "actors"
            result[mid][key].append(credit)
        return result

    def get_movie_keywords_bulk(
        self,
        tmdb_ids: list[int],
    ) -> dict[int, list[dict]]:
        unique_ids = list(dict.fromkeys(tmdb_ids))
        if not unique_ids:
            return {}
        for tmdb_id in unique_ids:
            self._validate_movie_id(tmdb_id)
        placeholders = ",".join("?" for _ in unique_ids)
        result: dict[int, list[dict]] = {mid: [] for mid in unique_ids}
        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT
                    mk.tmdb_id,
                    k.keyword_id,
                    k.tmdb_keyword_id,
                    k.name,
                    k.is_custom,
                    mk.position
                FROM movie_keywords mk
                JOIN keywords k ON mk.keyword_id = k.keyword_id
                WHERE mk.tmdb_id IN ({placeholders})
                ORDER BY mk.position, k.name COLLATE NOCASE
                """,
                tuple(unique_ids),
            ).fetchall()
        for row in rows:
            result[row["tmdb_id"]].append(dict(row))
        return result

    def search_library_people(
        self,
        query: str,
        credit_type: str | None = None,
        status: str | None = None,
    ) -> list[dict]:
        cleaned = " ".join((query or "").split())
        if not cleaned:
            return []
        escaped = (
            cleaned.replace("!", "!!")
            .replace("%", "!%")
            .replace("_", "!_")
        )
        like_pattern = f"%{escaped}%"

        where_parts = [
            "c.name LIKE ? ESCAPE '!' COLLATE NOCASE"
        ]
        params: list[Any] = [like_pattern]

        if credit_type in ("director", "actor"):
            where_parts.append("c.credit_type = ?")
            params.append(credit_type)

        if status:
            if status == "favorites":
                where_parts.append("u.is_favorite = 1")
            elif status == "movie-notes":
                where_parts.append("u.notes IS NOT NULL AND TRIM(u.notes) <> ''")
            else:
                from app.movie_status import validate_movie_status
                where_parts.append("u.status = ?")
                params.append(validate_movie_status(status))
        else:
            where_parts.append(
                "(u.status IS NOT NULL OR u.is_favorite = 1 OR (u.notes IS NOT NULL AND TRIM(u.notes) <> ''))"
            )

        where_clause = " AND ".join(where_parts)

        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT DISTINCT c.tmdb_person_id, c.name, c.credit_type
                FROM movie_credits c
                JOIN user_movie_data u ON c.tmdb_id = u.tmdb_id
                WHERE {where_clause}
                ORDER BY c.name COLLATE NOCASE
                LIMIT 20
                """,
                tuple(params),
            ).fetchall()

        return [
            {
                "id": row["tmdb_person_id"],
                "name": row["name"],
                "credit_type": row["credit_type"],
            }
            for row in rows
        ]

    def search_library_keywords(
        self,
        query: str,
        limit: int = 15,
    ) -> list[dict]:
        cleaned = " ".join((query or "").split())
        if not cleaned:
            return []
        escaped = (
            cleaned.replace("!", "!!")
            .replace("%", "!%")
            .replace("_", "!_")
        )
        like_pattern = f"%{escaped}%"
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT DISTINCT k.keyword_id, k.tmdb_keyword_id, k.name, k.is_custom
                FROM keywords k
                JOIN movie_keywords mk ON k.keyword_id = mk.keyword_id
                JOIN user_movie_data u ON mk.tmdb_id = u.tmdb_id
                WHERE k.name LIKE ? ESCAPE '!' COLLATE NOCASE
                ORDER BY k.is_custom DESC, k.name COLLATE NOCASE ASC
                LIMIT ?
                """,
                (like_pattern, limit),
            ).fetchall()
        return [
            {
                "id": row["keyword_id"],
                "name": f"🏷️ {row['name']}" if row["is_custom"] else row["name"],
                "raw_name": row["name"],
                "is_custom": bool(row["is_custom"]),
            }
            for row in rows
        ]

    def search_movie_keyword_links(
        self,
        query: str,
        keyword_type: str = "all",
    ) -> dict:
        cleaned_query = self._clean_name(query, "Keyword search")

        if not isinstance(keyword_type, str):
            raise ValueError(
                "Keyword type must be all, custom, or tmdb."
            )

        normalized_type = keyword_type.strip().casefold()

        if normalized_type not in {"all", "custom", "tmdb"}:
            raise ValueError(
                "Keyword type must be all, custom, or tmdb."
            )

        escaped_query = (
            cleaned_query
            .replace("\\", "\\\\")
            .replace("%", "\\%")
            .replace("_", "\\_")
        )
        parameters: list[Any] = [f"%{escaped_query}%"]
        type_condition = ""

        if normalized_type == "custom":
            type_condition = "AND k.is_custom = ?"
            parameters.append(1)
        elif normalized_type == "tmdb":
            type_condition = "AND k.is_custom = ?"
            parameters.append(0)

        parameters.append(cleaned_query)

        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT
                    mk.tmdb_id,
                    k.keyword_id,
                    k.tmdb_keyword_id,
                    k.name,
                    k.is_custom,
                    mk.position
                FROM keywords k
                JOIN movie_keywords mk
                    ON k.keyword_id = mk.keyword_id
                WHERE k.name LIKE ? ESCAPE '\\' COLLATE NOCASE
                  {type_condition}
                ORDER BY
                    CASE
                        WHEN k.name = ? COLLATE NOCASE THEN 0
                        ELSE 1
                    END,
                    k.name COLLATE NOCASE,
                    mk.tmdb_id
                """,
                parameters,
            ).fetchall()

        links = [dict(row) for row in rows]

        for link in links:
            link["is_custom"] = bool(link["is_custom"])

        return {
            "query": cleaned_query,
            "keyword_type": normalized_type,
            "links": links,
        }

    def search_movie_keyword_links_page(
        self,
        query: str,
        keyword_type: str = "all",
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ValueError("Keyword search page must be at least 1.")
        if page_size != 20:
            raise ValueError("Keyword search page size must be 20.")

        base = self.search_movie_keyword_links(query, keyword_type)
        movie_ids = list(dict.fromkeys(link["tmdb_id"] for link in base["links"]))
        total = len(movie_ids)
        start = (page - 1) * page_size
        selected_ids = set(movie_ids[start:start + page_size])
        return {
            "query": base["query"],
            "keyword_type": base["keyword_type"],
            "page": page,
            "page_size": page_size,
            "total_results": total,
            "total_pages": max(1, (total + page_size - 1) // page_size),
            "links": [
                link for link in base["links"]
                if link["tmdb_id"] in selected_ids
            ],
            "movie_ids": [
                movie_id for movie_id in movie_ids
                if movie_id in selected_ids
            ],
        }
