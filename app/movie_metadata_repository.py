from typing import Any

from app.database import get_connection


MAX_TMDB_KEYWORDS = 5


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

        if isinstance(keyword_id, bool) or not isinstance(keyword_id, int):
            raise ValueError("Keyword ID must be an integer.")

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
