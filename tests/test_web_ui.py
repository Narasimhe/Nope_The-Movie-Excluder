import unittest
from pathlib import Path

from app import main


class WebUITests(unittest.TestCase):
    def test_homepage_and_static_routes_are_registered(self) -> None:
        route_paths = {
            route.path
            for route in main.app.routes
        }

        self.assertIn("/", route_paths)
        self.assertIn("/static", route_paths)

    def test_homepage_returns_the_ui_document(self) -> None:
        response = main.web_home()

        self.assertEqual(
            Path(response.path),
            main.WEB_DIR / "index.html",
        )
        self.assertTrue(Path(response.path).is_file())

    def test_ui_assets_are_present_and_connected(self) -> None:
        index = (main.WEB_DIR / "index.html").read_text(
            encoding="utf-8"
        )
        styles = (main.STATIC_DIR / "styles.css").read_text(
            encoding="utf-8"
        )
        script = (main.STATIC_DIR / "app.js").read_text(
            encoding="utf-8"
        )

        self.assertIn('/static/styles.css', index)
        self.assertIn('/static/app.js', index)
        self.assertIn('/static/favicon.svg', index)
        self.assertIn('id="movie-search"', index)
        self.assertIn('id="movie-detail-page"', index)
        self.assertIn('id="movie-notes"', index)
        self.assertIn('data-discovery-mode="simple"', index)
        self.assertIn('data-discovery-mode="advanced"', index)
        self.assertIn('data-discovery-mode="super"', index)
        self.assertIn('id="profile-select"', index)
        self.assertIn('id="advanced-search-form"', index)
        self.assertIn('id="pagination"', index)
        self.assertIn('id="entries-page"', index)
        self.assertIn('id="verdict-stars"', index)
        self.assertIn('id="workspace-collapse"', index)
        self.assertIn('id="dialog-keywords"', index)
        self.assertIn('id="profile-dialog-title"', index)
        self.assertIn('data-footer-view="looking-out"', index)
        self.assertIn('id="return-to-origin"', index)
        self.assertIn('id="detail-trail"', index)
        self.assertIn('id="related-movies"', index)
        self.assertIn('id="entry-reader"', index)
        self.assertIn('id="looking-out-page"', index)
        self.assertIn('id="storage-page"', index)
        self.assertIn('id="entry-tags"', index)
        self.assertLess(
            index.index('id="dialog-genres"'),
            index.index('class="personal-panel"'),
        )
        self.assertLess(
            index.index('id="dialog-keywords"'),
            index.index('class="personal-panel"'),
        )
        self.assertIn("--accent: #f2c94c", styles)
        self.assertIn("/movies/search?query=", script)
        self.assertIn("/movies/status/", script)
        self.assertIn("/favorite", script)
        self.assertIn("/notes", script)
        self.assertIn("/movies/discover/advanced", script)
        self.assertIn("/movies/discover/super-advanced", script)
        self.assertIn("/search-preferences", script)
        self.assertIn("/search-state", script)
        self.assertIn("/entries", script)
        self.assertIn("/movies/notes?page=", script)
        self.assertIn("pagination_exact", script)
        self.assertIn("function renderPeople", script)
        self.assertIn("function renderDetailTrail", script)
        self.assertIn("include_previously_watched", script)
        self.assertIn("/movies/looking-out-for", script)
        self.assertIn("function openEntryReader", script)
        self.assertIn("JOURNAL_TIME_ZONE", script)
        self.assertIn('"Untracked"', script)


if __name__ == "__main__":
    unittest.main()
