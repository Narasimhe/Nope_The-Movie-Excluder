import unittest

from app.tmdb_client import BASE_URL, TMDBClient


class FakeResponse:
    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return {
            "id": 329865,
            "title": "Arrival",
            "genres": [{"id": 878, "name": "Science Fiction"}],
            "keywords": {
                "keywords": [{"id": 161176, "name": "linguist"}]
            },
        }


class FakeSession:
    def __init__(self) -> None:
        self.last_request: dict | None = None

    def get(self, url: str, **kwargs) -> FakeResponse:
        self.last_request = {
            "url": url,
            **kwargs,
        }
        return FakeResponse()


class TMDBClientMovieDetailsTests(unittest.TestCase):
    def test_movie_details_appends_keywords_and_credits(self) -> None:
        client = TMDBClient.__new__(TMDBClient)
        client.headers = {"Authorization": "Bearer test"}
        client.session = FakeSession()

        result = client.get_movie(329865)

        self.assertEqual(result["title"], "Arrival")
        self.assertEqual(
            client.session.last_request["url"],
            f"{BASE_URL}/movie/329865",
        )
        self.assertEqual(
            client.session.last_request["params"],
            {"append_to_response": "keywords,credits"},
        )
        self.assertEqual(
            client.session.last_request["timeout"],
            10,
        )


if __name__ == "__main__":
    unittest.main()
