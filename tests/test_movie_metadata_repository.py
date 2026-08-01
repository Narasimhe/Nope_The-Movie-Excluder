import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database
from app.database import initialize_database
from app.movie_metadata_repository import MovieMetadataRepository


class MovieMetadataRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)

        database_path = (
            Path(self.temporary_directory.name)
            / "movie_metadata_test.db"
        )
        database_path_patch = patch.object(
            database,
            "DATABASE_PATH",
            database_path,
        )
        database_path_patch.start()
        self.addCleanup(database_path_patch.stop)

        initialize_database()

        with database.get_connection() as connection:
            connection.executemany(
                """
                INSERT INTO movies (tmdb_id, title)
                VALUES (?, ?)
                """,
                [
                    (101, "Movie One"),
                    (202, "Movie Two"),
                ],
            )

        self.repository = MovieMetadataRepository()

    def test_genres_have_a_many_to_many_relationship(self) -> None:
        science_fiction = {"id": 878, "name": "Science Fiction"}
        drama = {"id": 18, "name": "Drama"}

        self.repository.replace_movie_genres(
            101,
            [science_fiction, drama],
        )
        self.repository.replace_movie_genres(
            202,
            [science_fiction],
        )

        first_movie_genres = self.repository.get_movie_genres(101)
        second_movie_genres = self.repository.get_movie_genres(202)

        self.assertEqual(
            {genre["tmdb_genre_id"] for genre in first_movie_genres},
            {878, 18},
        )
        self.assertEqual(
            {genre["tmdb_genre_id"] for genre in second_movie_genres},
            {878},
        )

        with database.get_connection() as connection:
            science_fiction_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM genres
                WHERE tmdb_genre_id = 878
                """
            ).fetchone()[0]

        self.assertEqual(science_fiction_count, 1)

    def test_replacing_genres_replaces_only_movie_links(self) -> None:
        self.repository.replace_movie_genres(
            101,
            [
                {"id": 878, "name": "Science Fiction"},
                {"id": 18, "name": "Drama"},
            ],
        )
        updated = self.repository.replace_movie_genres(
            101,
            [{"id": 53, "name": "Thriller"}],
        )

        self.assertEqual(
            [genre["tmdb_genre_id"] for genre in updated],
            [53],
        )

    def test_only_first_ten_tmdb_keywords_are_saved(self) -> None:
        keywords = [
            {"id": number, "name": f"Keyword {number}"}
            for number in range(1, 13)
        ]

        saved = self.repository.replace_tmdb_keywords(101, keywords)

        self.assertEqual(len(saved), 10)
        self.assertEqual(
            [keyword["tmdb_keyword_id"] for keyword in saved],
            list(range(1, 11)),
        )
        self.assertEqual(
            [keyword["position"] for keyword in saved],
            list(range(1, 11)),
        )
        self.assertTrue(
            all(not keyword["is_custom"] for keyword in saved)
        )

    def test_replacing_tmdb_keywords_preserves_custom_tags(self) -> None:
        custom = self.repository.add_custom_keyword(
            101,
            "cold ambience",
        )
        self.repository.replace_tmdb_keywords(
            101,
            [{"id": 1001, "name": "alien"}],
        )
        self.repository.replace_tmdb_keywords(
            101,
            [{"id": 1002, "name": "first contact"}],
        )

        all_keywords = self.repository.get_movie_keywords(101)

        self.assertEqual(
            {
                (
                    keyword["name"],
                    keyword["is_custom"],
                )
                for keyword in all_keywords
            },
            {
                ("first contact", False),
                ("cold ambience", True),
            },
        )
        self.assertIn(custom, all_keywords)

    def test_custom_keyword_is_reused_case_insensitively(self) -> None:
        first = self.repository.add_custom_keyword(
            101,
            "Cold Ambience",
        )
        second = self.repository.add_custom_keyword(
            202,
            "  cold   ambience  ",
        )

        self.assertEqual(first["keyword_id"], second["keyword_id"])
        self.assertTrue(first["is_custom"])
        self.assertIsNone(first["tmdb_keyword_id"])

        with database.get_connection() as connection:
            custom_keyword_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM keywords
                WHERE is_custom = 1
                """
            ).fetchone()[0]

        self.assertEqual(custom_keyword_count, 1)

    def test_official_and_custom_keyword_can_share_a_name(self) -> None:
        self.repository.replace_tmdb_keywords(
            101,
            [{"id": 1001, "name": "alien"}],
        )
        self.repository.add_custom_keyword(101, "alien")

        keywords = self.repository.get_movie_keywords(101)

        self.assertEqual(len(keywords), 2)
        self.assertEqual(
            {keyword["is_custom"] for keyword in keywords},
            {False, True},
        )

    def test_custom_keyword_can_be_removed_from_one_movie(self) -> None:
        first = self.repository.add_custom_keyword(101, "slow burn")
        self.repository.add_custom_keyword(202, "slow burn")

        removed = self.repository.remove_custom_keyword(
            101,
            first["keyword_id"],
        )

        self.assertTrue(removed)
        self.assertEqual(
            self.repository.get_custom_keywords(101),
            [],
        )
        self.assertEqual(
            len(self.repository.get_custom_keywords(202)),
            1,
        )

    def test_custom_keyword_can_be_deleted_from_every_movie(self) -> None:
        custom = self.repository.add_custom_keyword(
            101,
            "cold ambience",
        )
        self.repository.add_custom_keyword(202, "cold ambience")

        deleted = self.repository.delete_custom_keyword(
            custom["keyword_id"]
        )

        self.assertEqual(deleted["name"], "cold ambience")
        self.assertEqual(deleted["affected_movie_count"], 2)
        self.assertEqual(
            self.repository.get_custom_keywords(101),
            [],
        )
        self.assertEqual(
            self.repository.get_custom_keywords(202),
            [],
        )

    def test_official_keyword_cannot_be_globally_deleted(self) -> None:
        self.repository.replace_tmdb_keywords(
            101,
            [{"id": 1001, "name": "alien"}],
        )
        official = self.repository.get_tmdb_keywords(101)[0]

        deleted = self.repository.delete_custom_keyword(
            official["keyword_id"]
        )

        self.assertIsNone(deleted)
        self.assertEqual(
            len(self.repository.get_tmdb_keywords(101)),
            1,
        )

    def test_custom_keyword_can_be_renamed_globally(self) -> None:
        custom = self.repository.add_custom_keyword(
            101,
            "cold ambience",
        )
        self.repository.add_custom_keyword(202, "cold ambience")

        renamed = self.repository.rename_custom_keyword(
            custom["keyword_id"],
            "wintry atmosphere",
        )

        self.assertEqual(renamed["action"], "renamed")
        self.assertEqual(
            renamed["keyword_id"],
            custom["keyword_id"],
        )
        self.assertEqual(renamed["affected_movie_count"], 2)
        self.assertEqual(
            self.repository.get_custom_keywords(101)[0]["name"],
            "wintry atmosphere",
        )
        self.assertEqual(
            self.repository.get_custom_keywords(202)[0]["name"],
            "wintry atmosphere",
        )

    def test_renaming_to_existing_custom_keyword_merges_them(self) -> None:
        source = self.repository.add_custom_keyword(
            101,
            "cold ambience",
        )
        self.repository.add_custom_keyword(202, "cold ambience")
        target = self.repository.add_custom_keyword(
            101,
            "wintry atmosphere",
        )

        merged = self.repository.rename_custom_keyword(
            source["keyword_id"],
            "  WINTRY   ATMOSPHERE ",
        )

        self.assertEqual(merged["action"], "merged")
        self.assertEqual(
            merged["keyword_id"],
            target["keyword_id"],
        )
        self.assertEqual(
            merged["merged_from_keyword_id"],
            source["keyword_id"],
        )
        self.assertEqual(merged["affected_movie_count"], 2)

        first_movie_keywords = (
            self.repository.get_custom_keywords(101)
        )
        second_movie_keywords = (
            self.repository.get_custom_keywords(202)
        )

        self.assertEqual(len(first_movie_keywords), 1)
        self.assertEqual(len(second_movie_keywords), 1)
        self.assertEqual(
            first_movie_keywords[0]["keyword_id"],
            target["keyword_id"],
        )
        self.assertEqual(
            second_movie_keywords[0]["keyword_id"],
            target["keyword_id"],
        )

        with database.get_connection() as connection:
            source_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM keywords
                WHERE keyword_id = ?
                """,
                (source["keyword_id"],),
            ).fetchone()[0]

        self.assertEqual(source_count, 0)

    def test_official_keyword_cannot_be_globally_renamed(self) -> None:
        self.repository.replace_tmdb_keywords(
            101,
            [{"id": 1001, "name": "alien"}],
        )
        official = self.repository.get_tmdb_keywords(101)[0]

        renamed = self.repository.rename_custom_keyword(
            official["keyword_id"],
            "visitors",
        )

        self.assertIsNone(renamed)
        self.assertEqual(
            self.repository.get_tmdb_keywords(101)[0]["name"],
            "alien",
        )

    def test_blank_global_custom_keyword_name_is_rejected(
        self,
    ) -> None:
        custom = self.repository.add_custom_keyword(
            101,
            "cold ambience",
        )

        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            self.repository.rename_custom_keyword(
                custom["keyword_id"],
                "   ",
            )

    def test_blank_custom_keyword_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            self.repository.add_custom_keyword(101, "   ")


if __name__ == "__main__":
    unittest.main()
