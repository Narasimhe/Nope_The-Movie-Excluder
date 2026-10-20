import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from app import database
from app.database import initialize_database
from app.general_entry_repository import GeneralEntryRepository
from app.grey_service import GreyService


def test_grey_loads_prompt_file_and_replaces_placeholders():
    service = GreyService()
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": json.dumps({
                                    "text": "Nordic thrillers from 2010 onward.",
                                    "action": {"type": "none"},
                                    "pills": [],
                                })
                            }
                        ]
                    }
                }
            ]
        }
        mock_post.return_value = mock_resp

        service.api_key = "test_key"
        res = service.chat("Show me Scandinavian thrillers", current_view="library")

        self_call = mock_post.call_args
        payload = self_call.kwargs.get("json") or self_call[1].get("json")
        system_instruction = payload["systemInstruction"]["parts"][0]["text"]

        assert "You are Grey, the native cinema curator" in system_instruction
        assert "ACTIVE MOVIE SCREEN FOCUS (CRITICAL OVERRIDE RULE)" in system_instruction
        assert "CORE CINEMA TASTE PHILOSOPHY (CRAFT OVER GENRE)" in system_instruction
        assert "RUNTIME IS NEVER A CONSTRAINT" in system_instruction
        assert "JOURNAL & NOTE ACTIONS (CREATE VS. UPDATE)" in system_instruction
        assert res["text"] == "Nordic thrillers from 2010 onward."


def test_grey_create_draft_action_saves_to_database():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            repo = GeneralEntryRepository()
            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            fake_model_reply = {
                "text": "I've drafted a breakdown comparing Blade Runner and Dark City into your journal drafts.",
                "action": {
                    "type": "create_draft",
                    "params": {
                        "title": "Neon Shadows: Blade Runner vs Dark City",
                        "body": "Both films construct rain-soaked architectural mazes where memory is commodity...",
                        "tags": ["sci-fi", "neo-noir", "comparison"],
                    },
                },
                "pills": [],
            }

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [
                        {
                            "content": {
                                "parts": [
                                    {"text": json.dumps(fake_model_reply)}
                                ]
                            }
                        }
                    ]
                }
                mock_post.return_value = mock_resp

                result = service.chat("Draft a comparison between Blade Runner and Dark City")

                assert "I've drafted a breakdown" in result["text"]
                action = result["action"]
                assert action["type"] == "create_draft"
                entry_id = action["params"]["entry_id"]
                assert entry_id > 0

                draft_entry = repo.get_entry(entry_id)
                assert draft_entry is not None
                assert draft_entry["title"] == "Neon Shadows: Blade Runner vs Dark City"
                assert draft_entry["status"] == "draft"
                assert any(t["name"] == "neo-noir" for t in draft_entry["tags"])

                pills = result["pills"]
                open_pills = [p for p in pills if p["action"] == "open_entry"]
                assert len(open_pills) == 1
                assert open_pills[0]["payload"]["entry_id"] == entry_id


def test_grey_ingests_published_journal_digest_and_on_demand_excerpt():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            repo = GeneralEntryRepository()
            # Create a published essay
            repo.create_entry(
                "note",
                "The Desolation of Settlers",
                "Settlers strips away Martian romanticism into claustrophobic domestic dread.",
                tags=["sci-fi", "minimalism"],
                status="published",
            )
            # Create a draft essay (should NOT be in taste dossier)
            repo.create_entry(
                "note",
                "Unpublished Ramblings",
                "Just rough thoughts that shouldn't leak into memory yet.",
                tags=["draft"],
                status="draft",
            )

            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [
                        {
                            "content": {
                                "parts": [
                                    {"text": json.dumps({"text": "Answer referencing Settlers", "action": None, "pills": []})}
                                ]
                            }
                        }
                    ]
                }
                mock_post.return_value = mock_resp

                # Ask about the published essay
                service.chat("Based on my essay on Settlers, what should I watch?")

                self_call = mock_post.call_args
                payload = self_call.kwargs.get("json") or self_call[1].get("json")
                system_instruction = payload["systemInstruction"]["parts"][0]["text"]

                # Journal digest has the published essay title and tags
                assert "The Desolation of Settlers" in system_instruction
                assert "Unpublished Ramblings" not in system_instruction

                # On-demand excerpt was pulled because user asked about their essay on Settlers
                assert "Title: The Desolation of Settlers" in system_instruction
                assert "Settlers strips away Martian romanticism" in system_instruction


def test_grey_ingests_all_watched_and_excluded_titles():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            # Seed a movie and marked as watched
            with database.get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO movies (tmdb_id, title, release_date, vote_average, overview)
                    VALUES (101, 'Sicario', '2015-09-17', 7.4, 'An idealistic FBI agent...')
                    """
                )
                conn.execute(
                    """
                    INSERT INTO user_movie_data (tmdb_id, status, verdict, updated_at)
                    VALUES (101, 'watched', 7.0, '2026-10-17 12:00:00')
                    """
                )
                conn.execute(
                    """
                    INSERT INTO movies (tmdb_id, title, release_date, vote_average, overview)
                    VALUES (102, 'Transformers 5', '2017-06-21', 5.2, 'Autobots and Decepticons...')
                    """
                )
                conn.execute(
                    """
                    INSERT INTO user_movie_data (tmdb_id, status, verdict, updated_at)
                    VALUES (102, 'excluded', NULL, '2026-10-17 12:05:00')
                    """
                )

            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [
                        {
                            "content": {
                                "parts": [
                                    {"text": json.dumps({"text": "Recommendation", "action": None, "pills": []})}
                                ]
                            }
                        }
                    ]
                }
                mock_post.return_value = mock_resp

                service.chat("What should I watch next?")

                self_call = mock_post.call_args
                payload = self_call.kwargs.get("json") or self_call[1].get("json")
                system_instruction = payload["systemInstruction"]["parts"][0]["text"]

                assert "Sicario (7.0/10)" in system_instruction
                assert "Transformers 5" in system_instruction
                assert "LIBRARY, WATCHED & REWATCH AWARENESS" in system_instruction
                assert "REWATCHING & REVISITING IS WELCOMED" in system_instruction


def test_grey_handles_markdown_fenced_json_and_plain_text():
    service = GreyService()
    service.api_key = "test_key"

    # Test 1: Markdown fenced json
    fenced_output = "```json\n{\n  \"text\": \"Fenced response text\",\n  \"action\": {\"type\": \"none\"},\n  \"pills\": []\n}\n```"
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": fenced_output}]}}]
        }
        mock_post.return_value = mock_resp

        res = service.chat("Test query 1")
        assert res["text"] == "Fenced response text"

    # Test 2: Raw plain text without json
    plain_output = "I recommend checking out The Third Man for its stark atmospheric cinematography."
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": plain_output}]}}]
        }
        mock_post.return_value = mock_resp

        res = service.chat("Test query 2")
        assert res["text"] == plain_output
        assert res["action"] is None
        assert res["pills"] == []


def test_grey_update_entry_action_updates_existing_note():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            repo = GeneralEntryRepository()
            initial_note = repo.create_entry(
                entry_type="note",
                title="Watchlist",
                body="- Red Riding\n- Payback",
                tags=["watchlist"],
                status="published",
            )
            entry_id = initial_note["entry_id"]

            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            fake_model_reply = {
                "text": "Added IMDb links to your Watchlist note.",
                "action": {
                    "type": "update_entry",
                    "params": {
                        "entry_id": entry_id,
                        "title": "Watchlist",
                        "body": "- Red Riding [IMDb](https://imdb.com/title/123)\n- Payback [IMDb](https://imdb.com/title/456)",
                        "mode": "replace",
                    },
                },
                "pills": [],
            }

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [
                        {
                            "content": {
                                "parts": [
                                    {"text": json.dumps(fake_model_reply)}
                                ]
                            }
                        }
                    ]
                }
                mock_post.return_value = mock_resp

                res = service.chat("Add IMDb links to my Watchlist note")
                assert "Added IMDb links" in res["text"]
                assert res["action"]["type"] == "update_entry"
                assert res["action"]["params"]["entry_id"] == entry_id

                updated = repo.get_entry(entry_id)
                assert updated["status"] == "published"
                assert "[IMDb](https://imdb.com/title/123)" in updated["body"]
                # Verify no duplicate was created
                all_notes = repo.list_entries(status=None)
                assert all_notes["total_results"] == 1


def test_grey_related_movies_injected_into_prompt():
    service = GreyService()
    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": json.dumps({
                                    "text": "From the related titles, Thief is the standout pick.",
                                    "action": {"type": "open_movie", "params": {"tmdb_id": 11524}},
                                    "pills": [{"label": "🎬 Open Thief", "action": "open_movie", "payload": {"tmdb_id": 11524}}],
                                })
                            }
                        ]
                    }
                }
            ]
        }
        mock_post.return_value = mock_resp

        service.api_key = "test_key"
        related = [
            {"id": 11524, "title": "Thief", "year": "1981", "rating": 7.6, "status": "watchlist", "verdict": None},
            {"id": 979, "title": "Heat", "year": "1995", "rating": 8.3, "status": "watched", "verdict": 9},
        ]
        res = service.chat(
            "Which related movie should I watch next?",
            current_view="movie",
            inspected_movie_id=100,
            related_movies=related,
        )

        call_args = mock_post.call_args
        payload = call_args.kwargs.get("json") or call_args[1].get("json")
        system_instruction = payload["systemInstruction"]["parts"][0]["text"]

        assert "Related movies carousel shown on screen:" in system_instruction
        assert "Thief (1981)" in system_instruction
        assert "Heat (1995)" in system_instruction
        assert "watchlist" in system_instruction
        assert res["action"]["type"] == "open_movie"
        assert res["action"]["params"]["tmdb_id"] == 11524


def test_grey_set_movie_status_action():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            from app.movie_repository import MovieRepository
            from app.movie_service import MovieService
            movie_svc = MovieService()
            movie_repo = MovieRepository()
            movie_repo.save_movie({
                "id": 76726,
                "title": "Chronicle",
                "original_title": "Chronicle",
                "release_date": "2012-02-01",
                "overview": "Three high school friends gain superpowers.",
                "vote_average": 6.8,
            })

            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            fake_reply = {
                "text": "Added Chronicle to your New discovery shelf.",
                "action": {
                    "type": "set_movie_status",
                    "params": {
                        "tmdb_id": 76726,
                        "status": "new_discovery",
                    },
                },
                "pills": [],
            }

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": json.dumps(fake_reply)}]}}]
                }
                mock_post.return_value = mock_resp

                res = service.chat("add this to new discovery", inspected_movie_id=76726)
                assert res["action"]["type"] == "set_movie_status"
                assert res["action"]["params"]["status"] == "new_discovery"
                assert res["action"]["params"]["tmdb_id"] == 76726

                movie = movie_svc.get_movie(76726)
                assert movie["user_data"]["status"] == "new_discovery"


def test_grey_update_entry_guardrail_rejects_unprompted_note_modification():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            repo = GeneralEntryRepository()
            entry = repo.create_entry(entry_type="note", title="Soul vs Soulless Movies", body="Original essay body", tags=["cinema"])
            entry_id = entry["entry_id"]

            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            hallucinated_reply = {
                "text": "Added Chronicle to your note.",
                "action": {
                    "type": "update_entry",
                    "params": {
                        "entry_id": entry_id,
                        "title": "Soul vs Soulless Movies",
                        "body": "Corrupted essay body",
                    },
                },
                "pills": [],
            }

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": json.dumps(hallucinated_reply)}]}}]
                }
                mock_post.return_value = mock_resp

                # User asked a movie question without mentioning notes or having a note open
                res = service.chat("add this to new discovery", inspected_movie_id=76726)
                # The action must be stripped by the guardrail
                assert res["action"] is None

                # Essay must remain untouched
                essay = repo.get_entry(entry_id)
                assert essay["body"] == "Original essay body"


def test_grey_batch_set_movie_status_updates_all_titles():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            from app.movie_repository import MovieRepository
            movie_repo = MovieRepository()
            movie_repo.save_movie({
                "id": 1391,
                "title": "Cape Fear",
                "release_date": "1991-11-15",
                "overview": "A convicted rapist, released from prison...",
                "vote_average": 7.3,
            })
            movie_repo.save_movie({
                "id": 1392,
                "title": "Carlito's Way",
                "release_date": "1993-11-12",
                "overview": "An ex-con tries to stay straight...",
                "vote_average": 7.9,
            })

            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            batch_reply = {
                "text": "Added Cape Fear and Carlito's Way to your New Discovery shelf.",
                "action": {
                    "type": "batch_set_movie_status",
                    "params": {
                        "status": "new_discovery",
                        "movies": [
                            {"tmdb_id": 1391, "title": "Cape Fear"},
                            {"tmdb_id": 1392, "title": "Carlito's Way"},
                        ],
                    },
                },
                "pills": [],
            }

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": json.dumps(batch_reply)}]}}]
                }
                mock_post.return_value = mock_resp

                res = service.chat(
                    "add the YES movies to new discovery",
                    related_movies=[
                        {"id": 1391, "title": "Cape Fear"},
                        {"id": 1392, "title": "Carlito's Way"},
                    ]
                )
                assert res["action"]["type"] == "batch_set_movie_status"
                assert len(res["action"]["params"]["movies"]) == 2

                from app.user_movie_repository import UserMovieRepository
                user_repo = UserMovieRepository()
                m1 = user_repo.get_user_movie_data(1391)
                m2 = user_repo.get_user_movie_data(1392)
                assert m1["status"] == "new_discovery"
                assert m2["status"] == "new_discovery"


def test_grey_batch_set_movie_status_protects_existing_judgments():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            from app.movie_repository import MovieRepository
            from app.user_movie_repository import UserMovieRepository
            movie_repo = MovieRepository()
            user_repo = UserMovieRepository()

            # Cape Fear was previously NOPE'd (excluded)
            movie_repo.save_movie({
                "id": 1391,
                "title": "Cape Fear",
                "release_date": "1991-11-15",
                "overview": "A convicted rapist...",
                "vote_average": 7.3,
            })
            user_repo.set_status(1391, "excluded")

            # Carlito's Way is untracked
            movie_repo.save_movie({
                "id": 1392,
                "title": "Carlito's Way",
                "release_date": "1993-11-12",
                "overview": "An ex-con tries to stay straight...",
                "vote_average": 7.9,
            })

            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            batch_reply = {
                "text": "Added the YES films to New Discovery.",
                "action": {
                    "type": "batch_set_movie_status",
                    "params": {
                        "status": "new_discovery",
                        "movies": [
                            {"tmdb_id": 1391, "title": "Cape Fear"},
                            {"tmdb_id": 1392, "title": "Carlito's Way"},
                        ],
                    },
                },
                "pills": [],
            }

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": json.dumps(batch_reply)}]}}]
                }
                mock_post.return_value = mock_resp

                res = service.chat(
                    "add the YES movies to new discovery",
                    related_movies=[
                        {"id": 1391, "title": "Cape Fear"},
                        {"id": 1392, "title": "Carlito's Way"},
                    ]
                )

                # Cape Fear MUST still be excluded (protected!)
                m1 = user_repo.get_user_movie_data(1391)
                assert m1["status"] == "excluded"

                # Carlito's Way was untracked, so it safely became new_discovery
                m2 = user_repo.get_user_movie_data(1392)
                assert m2["status"] == "new_discovery"

                # Grey reports preserved judgment in message
                assert "Cape Fear" in res["text"]
                assert "EXCLUDED" in res["text"]


def test_grey_slash_command_skill_routing():
    service = GreyService()
    service.api_key = "test_key"

    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": json.dumps({
                                    "text": "**Carlito's Way (1993)**\nMasterpiece crime tragedy.\nVerdict: **YES**",
                                    "action": {"type": "none"},
                                    "pills": [],
                                })
                            }
                        ]
                    }
                }
            ]
        }
        mock_post.return_value = mock_resp

        # Call with slash command
        res = service.chat("/related")
        assert res["active_skill"] == "related"
        assert res["active_skill_name"] == "Related Movies Reality Check"

        # Verify that the active skill directive was injected into system instructions
        self_call = mock_post.call_args
        payload = self_call.kwargs.get("json") or self_call[1].get("json")
        system_instruction = payload["systemInstruction"]["parts"][0]["text"]
        assert "ACTIVE SKILL: /related" in system_instruction




