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
        assert "CORE CINEMA TASTE PHILOSOPHY" in system_instruction
        assert "CRAFT OVER GENRE" in system_instruction
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

                # Ask about the published essay (read-only question)
                service.chat("Based on my essay The Desolation of Settlers, what should I watch?")

                self_call = mock_post.call_args
                payload = self_call.kwargs.get("json") or self_call[1].get("json")
                system_instruction = payload["systemInstruction"]["parts"][0]["text"]

                # Compact 1-line note title index has the published essay title
                assert "The Desolation of Settlers" in system_instruction
                assert "Unpublished Ramblings" not in system_instruction

                # Full note content was loaded in READ-ONLY mode without loading the 85-line editor manual
                assert "Title: The Desolation of Settlers" in system_instruction
                assert "Settlers strips away Martian romanticism" in system_instruction
                assert "ACTIVE SKILL: READ-ONLY NOTE DISCUSSION" in system_instruction
                assert "ACTIVE SKILL: NOTES & JOURNAL EDITOR" not in system_instruction


def test_grey_ingests_all_watched_and_excluded_titles():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            # Seed a high-rated favorite, a watched movie, and an excluded movie
            with database.get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO movies (tmdb_id, title, release_date, vote_average, overview)
                    VALUES (100, 'Fargo', '1996-03-08', 8.1, 'A Minnesota car salesman...')
                    """
                )
                conn.execute(
                    """
                    INSERT INTO user_movie_data (tmdb_id, status, verdict, is_favorite, updated_at)
                    VALUES (100, 'watched', 9.0, 1, '2026-10-17 12:00:00')
                    """
                )
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
                    INSERT INTO user_movie_data (tmdb_id, status, verdict, notes, updated_at)
                    VALUES (102, 'excluded', NULL, 'Mindless CGI slop', '2026-10-17 12:05:00')
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

                # Base prompt contains only the compact taste fingerprint (Fargo + Transformers 5 sample) and get_shelf_movies tool
                assert "Fargo" in system_instruction
                assert "Transformers 5" in system_instruction
                assert "Sicario (7.0/10)" not in system_instruction
                assert "get_shelf_movies" in system_instruction
                assert "LIBRARY, WATCHED & REWATCH AWARENESS" in system_instruction
                assert "REWATCHING & REVISITING IS WELCOMED" in system_instruction

                # And calling get_shelf_movies on demand returns the watched shelf including Sicario
                shelf_out = service._execute_tool_call({"tool": "get_shelf_movies", "status": "watched", "limit": 20})
                assert "Sicario (2015)" in shelf_out


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


def test_grey_pruned_skills():
    from app.grey_service import SKILLS_REGISTRY
    # /tonight, /nope, and /watchlist pruned from registry
    assert "tonight" not in SKILLS_REGISTRY
    assert "nope" not in SKILLS_REGISTRY
    assert "watchlist" not in SKILLS_REGISTRY
    assert "related" in SKILLS_REGISTRY


def test_grey_intercepts_set_movie_status_when_post_mentioned_and_appends():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            repo = GeneralEntryRepository()
            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            # Create an existing post titled "Watchlist 1"
            entry = repo.create_entry(
                entry_type="note",
                title="Watchlist 1",
                body=">> Thief (1981)\n- **Cast:** James Caan\n- **Synopsis:** Master safecracker.\n- **Why YES:** Mann craft.",
                tags=["watchlist"],
                status="draft",
            )
            target_entry_id = entry["entry_id"]

            # Insert inspected movie into movies table
            with service._get_connection() as conn:
                conn.execute(
                    "INSERT INTO movies (tmdb_id, title, release_date, overview, vote_average) VALUES (?, ?, ?, ?, ?)",
                    (1392, "Carlito's Way", "1993-11-12", "An ex-con tries to stay straight.", 7.9)
                )

            # Model errantly returns set_movie_status instead of updating note
            fake_model_reply = {
                "text": "Added Carlito's Way to your Watchlist 1 post.",
                "action": {
                    "type": "set_movie_status",
                    "params": {"status": "watch_later", "tmdb_id": 1392, "title": "Carlito's Way"}
                },
                "pills": [],
            }

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": json.dumps(fake_model_reply)}]}}]
                }
                mock_post.return_value = mock_resp

                res = service.chat("Add this to my Watchlist 1 post", inspected_movie_id=1392, related_movies=[])

                # Verify set_movie_status was intercepted and redirected to update_entry
                assert res["action"]["type"] == "update_entry"
                assert res["action"]["params"]["entry_id"] == target_entry_id

                # Verify post body preserved existing content and appended Carlito's Way
                updated = repo.get_entry(target_entry_id)
                assert ">> Thief (1981)" in updated["body"]
                assert ">> Carlito's Way (1993)" in updated["body"]


def test_grey_resolves_specific_post_title_over_generic():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            repo = GeneralEntryRepository()
            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            # Create two notes: "Watchlist" and "Watchlist 2"
            repo.create_entry(entry_type="note", title="Watchlist", body="Base list", tags=[], status="published")
            e2 = repo.create_entry(entry_type="note", title="Watchlist 2", body="Second tranche", tags=[], status="published")

            with service._get_connection() as conn:
                conn.execute(
                    "INSERT INTO movies (tmdb_id, title, release_date, overview, vote_average) VALUES (?, ?, ?, ?, ?)",
                    (1393, "Strange Days", "1995-10-06", "A former cop turned street peddler.", 7.2)
                )

            fake_model_reply = {
                "text": "Appended Strange Days to Watchlist 2.",
                "action": {
                    "type": "update_entry",
                    "params": {
                        "mode": "append",
                        "body": ">> Strange Days (1995)\n- **Synopsis:** Cyberpunk noir.",
                    }
                },
                "pills": [],
            }

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": json.dumps(fake_model_reply)}]}}]
                }
                mock_post.return_value = mock_resp

                res = service.chat("Add this to my Watchlist 2 post", inspected_movie_id=1393, related_movies=[])
                assert res["action"]["params"]["entry_id"] == e2["entry_id"]

                updated = repo.get_entry(e2["entry_id"])
                assert "Second tranche" in updated["body"]
                assert ">> Strange Days (1995)" in updated["body"]


def test_grey_appends_respecting_bullet_list_format():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            repo = GeneralEntryRepository()
            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            # Create existing note with simple bullet list and IMDb links
            initial_body = "• The Naked Gun (Leslie Nielsen) - IMDb\n• Top Secret! (Val Kilmer) - IMDb"
            entry = repo.create_entry(
                entry_type="note",
                title="Spoof Movies",
                body=initial_body,
                tags=["spoofs"],
                status="published",
            )
            target_id = entry["entry_id"]

            with service._get_connection() as conn:
                conn.execute(
                    "INSERT INTO movies (tmdb_id, title, release_date, overview, vote_average) VALUES (?, ?, ?, ?, ?)",
                    (2457, "The Kentucky Fried Movie", "1977-08-10", "A sketch comedy satire.", 6.5)
                )

            # Fallback action interceptor formats as matching bullet point
            fake_model_reply = {
                "text": "Added to your Spoof Movies note.",
                "action": {
                    "type": "set_movie_status",
                    "params": {"status": "watch_later", "tmdb_id": 2457, "title": "The Kentucky Fried Movie"}
                },
                "pills": [],
            }

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": json.dumps(fake_model_reply)}]}}]
                }
                mock_post.return_value = mock_resp

                res = service.chat("Add to my Spoof Movies note", inspected_movie_id=2457)
                updated = repo.get_entry(target_id)
                assert updated is not None
                # Should NOT contain toggle syntax
                assert ">>" not in updated["body"]
                assert "- **Why YES:**" not in updated["body"]
                # Should contain bullet matching original style
                assert "• The Kentucky Fried Movie (1977)" in updated["body"]


def test_grey_deduplicate_and_format_note_body():
    service = GreyService()

    # Case 1: Deduplicate and convert to toggle when redundant entry was already in note
    existing_note = (
        "• The Settlers (Sofia Boutella)\n"
        "• Kill the messenger (Jeremy Runner)\n"
        "• Red Lights (Cillian Murphy & Sigourney Weaver)\n"
        "• Syriana\n\n"
        "• Red Lights (Cillian Murphy & Sigourney Weaver)\n\n"
        "OK -- 1st and 2nd acts are mostly about our protagonists,\n"
        "Cillian Murphy and Sigourney debunking fraudulent psychics.\n\n"
        "Another silly twist -- De Niro is not blind, just pretends to be."
    )

    result = service._deduplicate_and_format_note_body(
        existing_body=existing_note,
        new_body="",
        mode="append",
        user_message="yeah good -- but toggle collpase for this",
        inspected_movie_title="Red Lights",
    )

    # Must contain clean human-readable Notion toggle (>> Title)
    assert ">> Red Lights (Cillian Murphy & Sigourney Weaver)" in result
    assert "<details" not in result
    assert "<summary" not in result
    assert "</details>" not in result
    assert "Cillian Murphy and Sigourney debunking fraudulent psychics." in result
    # Must preserve other movies in order
    assert "• The Settlers (Sofia Boutella)" in result
    assert "• Kill the messenger (Jeremy Runner)" in result
    assert "• Syriana" in result
    # Red Lights must appear only ONCE (in the >> header)
    assert result.count("Red Lights") == 1
    # Syriana must still be after Red Lights toggle
    assert result.index("Red Lights") < result.index("Syriana")


def test_grey_converts_clumsy_html_details_to_clean_toggle():
    service = GreyService()

    clumsy_note = (
        "<details><summary>Nightcrawler (2014)</summary>\n\n"
        "Oh this is a well done movie -- jake plays that nocturnal psychopath\n"
        "</details>"
    )

    result = service._deduplicate_and_format_note_body(
        existing_body=clumsy_note,
        new_body="",
        mode="replace",
        user_message="format this properly",
        inspected_movie_title="Nightcrawler",
    )

    # Clumsy HTML tags must be converted to clean >> Notion toggle
    assert "<details" not in result
    assert "<summary" not in result
    assert "</details>" not in result
    assert ">> Nightcrawler (2014)" in result
    assert "jake plays that nocturnal psychopath" in result


def test_grey_in_place_upsert_existing_bullet():
    service = GreyService()

    existing_note = (
        "• The Settlers (Sofia Boutella)\n"
        "• Kill the messenger (Jeremy Runner)\n"
        "• Red Lights (Cillian Murphy & Sigourney Weaver)\n"
        "• Syriana"
    )

    new_entry = (
        "• Red Lights (Cillian Murphy & Sigourney Weaver)\n\n"
        "Great atmosphere and acting, though the twist is divisive."
    )

    result = service._deduplicate_and_format_note_body(
        existing_body=existing_note,
        new_body=new_entry,
        mode="append",
        user_message="Add my thoughts on Red Lights",
        inspected_movie_title="Red Lights",
    )

    # Must replace the bare bullet in-place without adding duplicate after Syriana
    assert result.count("Red Lights") == 1
    assert result.index("Red Lights") < result.index("Syriana")
    assert "Great atmosphere and acting" in result


def test_grey_new_movie_appends_normally():
    service = GreyService()

    existing_note = (
        "• The Settlers (Sofia Boutella)\n"
        "• Syriana"
    )

    new_entry = "• Heat (1995)"

    result = service._deduplicate_and_format_note_body(
        existing_body=existing_note,
        new_body=new_entry,
        mode="append",
        user_message="Add Heat to my note",
        inspected_movie_title="Heat",
    )

    assert "• The Settlers (Sofia Boutella)" in result
    assert "• Syriana" in result
    assert "• Heat (1995)" in result
    assert result.index("Syriana") < result.index("Heat")


def test_grey_modular_skill_routing():
    service = GreyService()
    service.api_key = "test_key"

    fake_model_reply = {
        "text": "Skill test response.",
        "action": None,
        "pills": [],
    }

    with patch("requests.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": json.dumps(fake_model_reply)}]}}]
        }
        mock_post.return_value = mock_resp

        # 1. Notes view loads notes_editor skill and does NOT load unrelated skills
        service.chat("Help with this note", current_view="notes", inspected_note={"id": 1, "title": "Test", "body": "Body"})
        call_args = mock_post.call_args
        payload = call_args.kwargs.get("json") or call_args[1].get("json")
        system_instruction = payload["systemInstruction"]["parts"][0]["text"]
        assert "ACTIVE SKILL: NOTES & JOURNAL EDITOR" in system_instruction
        assert "CAREER FILMOGRAPHY EXPLORER" not in system_instruction

        # 2. Filmography view loads filmography_explorer skill
        service.chat("Tell me about his career", current_view="filmography", active_person={"id": 123, "name": "Daniel Kaluuya"})
        call_args = mock_post.call_args
        payload = call_args.kwargs.get("json") or call_args[1].get("json")
        system_instruction = payload["systemInstruction"]["parts"][0]["text"]
        assert "CAREER FILMOGRAPHY EXPLORER" in system_instruction
        assert "NOTES & JOURNAL EDITOR" not in system_instruction

        # 3. Related skill load
        service.chat("Which of these are good?", current_view="movie", active_skill_key="related")
        call_args = mock_post.call_args
        payload = call_args.kwargs.get("json") or call_args[1].get("json")
        system_instruction = payload["systemInstruction"]["parts"][0]["text"]
        assert "RELATED MOVIES REALITY CHECK" in system_instruction
        assert "NOTES & JOURNAL EDITOR" not in system_instruction


def test_grey_deduplicate_replaces_existing_toggle_in_place():
    service = GreyService()

    existing_note = (
        ">> The Settlers (2021)\n"
        "Old brief note here.\n\n"
        ">> Funny games (Michael Haneke)\n"
        "Dark and funny at times."
    )

    new_entry = (
        ">> The Settlers (2021)\n"
        "Expanded in-depth critique with much more craft detail."
    )

    result = service._deduplicate_and_format_note_body(
        existing_body=existing_note,
        new_body=new_entry,
        mode="append",
        user_message="Update my thoughts on Settlers",
        inspected_movie_title="The Settlers",
    )

    # Should appear only once
    assert result.count("The Settlers") == 1
    assert "Expanded in-depth critique" in result
    assert "Old brief note here" not in result
    assert "Funny games" in result


def test_grey_raw_format_precedence_avoids_toggle():
    service = GreyService()

    existing_note = ">> Funny games\nDark and funny."
    new_entry = ">> Settlers\nLiked it as it is."

    result = service._deduplicate_and_format_note_body(
        existing_body=existing_note,
        new_body=new_entry,
        mode="append",
        user_message="add it as it is",
        inspected_movie_title="Settlers",
    )

    assert "Liked it as it is." in result
    # Should not keep the generated toggle header when explicitly asked for raw / as it is
    assert not result.endswith(">> Settlers\nLiked it as it is.")


def test_grey_reactions_indexing_and_delivery():
    service = GreyService()
    index_str = service.get_reactions_index()
    # gangster_cat.gif is present in assets/gifs_n_media
    assert "gangster_cat.gif" in index_str

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
                                    "text": "As far back as I can remember, I always wanted to be a gangster.",
                                    "reaction": "gangster_cat.gif",
                                    "action": None,
                                    "pills": [],
                                })
                            }
                        ]
                    }
                }
            ]
        }
        mock_post.return_value = mock_resp

        res = service.chat("What do you think of Goodfellas?")
        assert res["reaction"] == "gangster_cat.gif"
        assert "gangster" in res["text"]


def test_grey_reactions_sanitizes_nonexistent_files():
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
                                    "text": "Nice movie.",
                                    "reaction": "non_existent_fake_cat.gif",
                                    "action": None,
                                    "pills": [],
                                })
                            }
                        ]
                    }
                }
            ]
        }
        mock_post.return_value = mock_resp

        res = service.chat("What do you think of Fargo?")
        assert res["reaction"] is None


def test_grey_does_not_hijack_movie_on_common_four_letter_words():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            with database.get_connection() as conn:
                conn.execute(
                    "INSERT INTO movies (tmdb_id, title, release_date, vote_average, overview) VALUES (999, 'Time', '2020-01-01', 7.0, 'Doc')"
                )
                conn.execute(
                    "INSERT INTO user_movie_data (tmdb_id, status, updated_at) VALUES (999, 'watched', '2026-10-17 12:00:00')"
                )

            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": json.dumps({"text": "Reply", "action": None, "pills": []})}]}}]
                }
                mock_post.return_value = mock_resp

                service.chat("What movie is worth my time tonight?")
                payload = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1].get("json")
                system_instruction = payload["systemInstruction"]["parts"][0]["text"]
                assert "Active Movie TMDB ID: None" in system_instruction


def test_grey_two_tier_progressive_research_context_avoids_bloat_on_normal_turns():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        research_dir = Path(temp_dir) / "research"
        research_dir.mkdir(parents=True, exist_ok=True)
        (research_dir / "noir_notes.md").write_text("# Secret Noir Body Content 12345\n", encoding="utf-8")

        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            service = GreyService(db_path=str(temp_db))
            service.research_dir = research_dir
            service.api_key = "test_key"

            with patch("requests.post") as mock_post:
                mock_resp = MagicMock()
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "candidates": [{"content": {"parts": [{"text": json.dumps({"text": "Reply", "action": None, "pills": []})}]}}]
                }
                mock_post.return_value = mock_resp

                # Normal movie turn: only filename summary, NOT full body content
                service.chat("Is Sicario good?")
                payload = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1].get("json")
                sys_normal = payload["systemInstruction"]["parts"][0]["text"]
                assert "noir_notes.md" in sys_normal
                assert "Secret Noir Body Content 12345" not in sys_normal

                # Research turn: full body content is injected
                service.chat("/research what is in noir_notes?")
                payload_res = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1].get("json")
                sys_res = payload_res["systemInstruction"]["parts"][0]["text"]
                assert "Secret Noir Body Content 12345" in sys_res


def test_grey_on_demand_tool_call_fetches_note_and_shelf():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        temp_db = Path(temp_dir) / "test.db"
        with patch.object(database, "DATABASE_PATH", temp_db):
            initialize_database()
            repo = GeneralEntryRepository()
            note = repo.create_entry(
                entry_type="note",
                title="Spoof Movies",
                body="• Top Secret! (1984)\n• Airplane! (1980)",
                tags=["parody", "comedy"],
                status="published",
            )
            service = GreyService(db_path=str(temp_db))
            service.api_key = "test_key"

            hop1_reply = {
                "text": "Fetching spoof note...",
                "action": {
                    "type": "tool_call",
                    "params": {"tool": "get_note", "entry_id": note["entry_id"], "query": "parody"},
                },
                "pills": [],
            }
            hop2_reply = {
                "text": "Your Spoof Movies note includes Top Secret! (1984) and Airplane! (1980).",
                "action": {"type": "none"},
                "pills": [],
            }

            with patch("requests.post") as mock_post:
                resp1 = MagicMock()
                resp1.status_code = 200
                resp1.json.return_value = {"candidates": [{"content": {"parts": [{"text": json.dumps(hop1_reply)}]}}]}
                resp2 = MagicMock()
                resp2.status_code = 200
                resp2.json.return_value = {"candidates": [{"content": {"parts": [{"text": json.dumps(hop2_reply)}]}}]}
                mock_post.side_effect = [resp1, resp2]

                res = service.chat("What movies are in my parody list?")
                assert "Top Secret!" in res["text"]
                assert mock_post.call_count == 2











