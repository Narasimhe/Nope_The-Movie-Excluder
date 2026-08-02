from typing import Any

from app.database import get_connection


class GeneralEntryRepository:
    PAGE_SIZE = 20

    def create_entry(
        self,
        entry_type: str,
        title: str,
        body: str | None = None,
        url: str | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        values = self._clean_values(entry_type, title, body, url)
        cleaned_tags = self._clean_tags(tags)
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO general_entries (
                    entry_type,
                    title,
                    body,
                    url
                )
                VALUES (?, ?, ?, ?)
                """,
                values,
            )
            entry_id = cursor.lastrowid
            self._replace_tags(connection, entry_id, cleaned_tags)
        entry = self.get_entry(entry_id)
        if entry is None:
            raise RuntimeError("Entry was saved but could not be read.")
        return entry

    def get_entry(self, entry_id: int) -> dict[str, Any] | None:
        self._validate_entry_id(entry_id)
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM general_entries
                WHERE entry_id = ?
                  AND is_deleted = 0
                """,
                (entry_id,),
            ).fetchone()
        if row is None:
            return None
        return self._attach_tags([dict(row)])[0]

    def update_entry(
        self,
        entry_id: int,
        entry_type: str,
        title: str,
        body: str | None = None,
        url: str | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any] | None:
        self._validate_entry_id(entry_id)
        values = self._clean_values(entry_type, title, body, url)
        cleaned_tags = self._clean_tags(tags)
        with get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE general_entries
                SET entry_type = ?,
                    title = ?,
                    body = ?,
                    url = ?,
                    updated_at = STRFTIME(
                        '%Y-%m-%d %H:%M:%f',
                        'now'
                    )
                WHERE entry_id = ?
                  AND is_deleted = 0
                """,
                (*values, entry_id),
            )
            if cursor.rowcount:
                self._replace_tags(connection, entry_id, cleaned_tags)
        if cursor.rowcount == 0:
            return None
        return self.get_entry(entry_id)

    def delete_entry(self, entry_id: int) -> bool:
        self._validate_entry_id(entry_id)
        with get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE general_entries
                SET is_deleted = 1,
                    updated_at = STRFTIME(
                        '%Y-%m-%d %H:%M:%f',
                        'now'
                    )
                WHERE entry_id = ?
                  AND is_deleted = 0
                """,
                (entry_id,),
            )
        return cursor.rowcount > 0

    def list_entries(
        self,
        *,
        page: int = 1,
        query: str | None = None,
        entry_type: str | None = None,
        tag: str | None = None,
        year: int | None = None,
        month: int | None = None,
    ) -> dict[str, Any]:
        self._validate_page(page)
        clauses = ["is_deleted = 0"]
        parameters: list[Any] = []

        if query is not None:
            cleaned_query = " ".join(query.split())
            if cleaned_query:
                escaped = (
                    cleaned_query.replace("!", "!!")
                    .replace("%", "!%")
                    .replace("_", "!_")
                )
                clauses.append(
                    "(title LIKE ? ESCAPE '!' COLLATE NOCASE "
                    "OR body LIKE ? ESCAPE '!' COLLATE NOCASE "
                    "OR url LIKE ? ESCAPE '!' COLLATE NOCASE "
                    "OR EXISTS ("
                    "SELECT 1 FROM general_entry_tag_links search_links "
                    "JOIN general_entry_tags search_tags "
                    "ON search_tags.tag_id = search_links.tag_id "
                    "WHERE search_links.entry_id = general_entries.entry_id "
                    "AND search_tags.name LIKE ? ESCAPE '!' COLLATE NOCASE"
                    "))"
                )
                term = f"%{escaped}%"
                parameters.extend([term, term, term, term])

        if entry_type is not None:
            cleaned_type = self._validate_entry_type(entry_type)
            clauses.append("entry_type = ?")
            parameters.append(cleaned_type)

        if tag is not None:
            cleaned_tag = " ".join(tag.split())
            if cleaned_tag:
                clauses.append(
                    "EXISTS ("
                    "SELECT 1 FROM general_entry_tag_links filter_links "
                    "JOIN general_entry_tags filter_tags "
                    "ON filter_tags.tag_id = filter_links.tag_id "
                    "WHERE filter_links.entry_id = general_entries.entry_id "
                    "AND filter_tags.name = ? COLLATE NOCASE"
                    ")"
                )
                parameters.append(cleaned_tag)

        if year is not None:
            if isinstance(year, bool) or not isinstance(year, int):
                raise ValueError("Entry year must be an integer.")
            clauses.append(
                "strftime('%Y', datetime(updated_at, "+
                "'+5 hours', '+30 minutes')) = ?"
            )
            parameters.append(f"{year:04d}")

        if month is not None:
            if (
                isinstance(month, bool)
                or not isinstance(month, int)
                or month < 1
                or month > 12
            ):
                raise ValueError("Entry month must be between 1 and 12.")
            clauses.append(
                "strftime('%m', datetime(updated_at, "+
                "'+5 hours', '+30 minutes')) = ?"
            )
            parameters.append(f"{month:02d}")

        where_clause = " AND ".join(clauses)
        offset = (page - 1) * self.PAGE_SIZE
        with get_connection() as connection:
            total = connection.execute(
                f"SELECT COUNT(*) FROM general_entries WHERE {where_clause}",
                parameters,
            ).fetchone()[0]
            rows = connection.execute(
                f"""
                SELECT *
                FROM general_entries
                WHERE {where_clause}
                ORDER BY updated_at DESC, entry_id DESC
                LIMIT ? OFFSET ?
                """,
                [*parameters, self.PAGE_SIZE, offset],
            ).fetchall()

        entries = self._attach_tags([dict(row) for row in rows])
        return {
            "page": page,
            "page_size": self.PAGE_SIZE,
            "total_results": total,
            "total_pages": max(1, (total + self.PAGE_SIZE - 1) // self.PAGE_SIZE),
            "results": entries,
        }

    def _attach_tags(
        self,
        entries: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        if not entries:
            return entries
        entry_ids = [entry["entry_id"] for entry in entries]
        placeholders = ",".join("?" for _ in entry_ids)
        with get_connection() as connection:
            rows = connection.execute(
                f"""
                SELECT links.entry_id, tags.tag_id, tags.name
                FROM general_entry_tag_links links
                JOIN general_entry_tags tags ON tags.tag_id = links.tag_id
                WHERE links.entry_id IN ({placeholders})
                ORDER BY tags.name COLLATE NOCASE, tags.tag_id
                """,
                entry_ids,
            ).fetchall()
        tags_by_entry: dict[int, list[dict[str, Any]]] = {}
        for row in rows:
            tags_by_entry.setdefault(row["entry_id"], []).append({
                "tag_id": row["tag_id"],
                "name": row["name"],
            })
        for entry in entries:
            entry["tags"] = tags_by_entry.get(entry["entry_id"], [])
        return entries

    @staticmethod
    def _replace_tags(
        connection,
        entry_id: int,
        tags: list[str],
    ) -> None:
        connection.execute(
            "DELETE FROM general_entry_tag_links WHERE entry_id = ?",
            (entry_id,),
        )
        for name in tags:
            connection.execute(
                """
                INSERT INTO general_entry_tags (name)
                VALUES (?)
                ON CONFLICT(name) DO NOTHING
                """,
                (name,),
            )
            row = connection.execute(
                """
                SELECT tag_id
                FROM general_entry_tags
                WHERE name = ? COLLATE NOCASE
                """,
                (name,),
            ).fetchone()
            connection.execute(
                """
                INSERT OR IGNORE INTO general_entry_tag_links (entry_id, tag_id)
                VALUES (?, ?)
                """,
                (entry_id, row["tag_id"]),
            )
        connection.execute(
            """
            DELETE FROM general_entry_tags
            WHERE NOT EXISTS (
                SELECT 1 FROM general_entry_tag_links links
                WHERE links.tag_id = general_entry_tags.tag_id
            )
            """
        )

    @staticmethod
    def _clean_tags(tags: list[str] | None) -> list[str]:
        if tags is None:
            return []
        if not isinstance(tags, list):
            raise ValueError("Entry tags must be a list of text values.")
        cleaned: list[str] = []
        seen: set[str] = set()
        for value in tags:
            if not isinstance(value, str):
                raise ValueError("Every entry tag must be text.")
            name = " ".join(value.split())
            if not name:
                continue
            if len(name) > 40:
                raise ValueError("Entry tags cannot exceed 40 characters.")
            key = name.casefold()
            if key not in seen:
                seen.add(key)
                cleaned.append(name)
        if len(cleaned) > 20:
            raise ValueError("An entry cannot have more than 20 tags.")
        return cleaned

    @staticmethod
    def _clean_values(
        entry_type: str,
        title: str,
        body: str | None,
        url: str | None,
    ) -> tuple[str, str, str | None, str | None]:
        cleaned_type = GeneralEntryRepository._validate_entry_type(
            entry_type
        )
        if not isinstance(title, str):
            raise ValueError("Entry title must be text.")
        cleaned_title = " ".join(title.split())
        if not cleaned_title:
            raise ValueError("Entry title cannot be empty.")
        if len(cleaned_title) > 200:
            raise ValueError("Entry title cannot exceed 200 characters.")
        if body is not None and not isinstance(body, str):
            raise ValueError("Entry body must be text or null.")
        if url is not None and not isinstance(url, str):
            raise ValueError("Entry URL must be text or null.")
        cleaned_body = body.strip() if body and body.strip() else None
        cleaned_url = None
        if url and url.strip():
            urls = [line.strip() for line in url.splitlines() if line.strip()]
            cleaned_url = "\n".join(urls) or None
        if cleaned_type == "link" and cleaned_url is None:
            raise ValueError("A link entry needs a URL.")
        return cleaned_type, cleaned_title, cleaned_body, cleaned_url

    @staticmethod
    def _validate_entry_type(entry_type: str) -> str:
        if not isinstance(entry_type, str):
            raise ValueError("Entry type must be note or link.")
        cleaned = entry_type.strip().casefold()
        if cleaned not in {"note", "link"}:
            raise ValueError("Entry type must be note or link.")
        return cleaned

    @staticmethod
    def _validate_entry_id(entry_id: int) -> None:
        if (
            isinstance(entry_id, bool)
            or not isinstance(entry_id, int)
            or entry_id <= 0
        ):
            raise ValueError("Entry ID must be a positive integer.")

    @staticmethod
    def _validate_page(page: int) -> None:
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ValueError("Entry page must be at least 1.")
