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
        self.assertIn('id="movie-search"', index)
        self.assertIn('id="movie-dialog"', index)
        self.assertIn("--accent: #f2c94c", styles)
        self.assertIn("/movies/search?query=", script)
        self.assertIn("/movies/status/", script)
        self.assertIn("/favorite", script)


if __name__ == "__main__":
    unittest.main()
