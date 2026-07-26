# TMDB Genre and Keyword Integration

Opening a movie's detail view now requests TMDB movie details with
`append_to_response=keywords`. The same response supplies the movie's official
genres and keyword payload.

`MovieService.get_movie()` then:

1. saves or updates the movie record;
2. replaces its official genre links;
3. replaces its official keyword links, keeping only the first five;
4. preserves all custom keywords;
5. records `metadata_fetched_at`; and
6. returns the movie with local `genres` and `keywords`.

Movies saved before this feature have no `metadata_fetched_at` value. They are
automatically enriched the next time their details are opened. Later openings
use the saved local metadata instead of immediately calling TMDB again.

## Verification

Run from the project root:

```powershell
python -m unittest discover -s tests -p "test_movie_service_metadata_integration.py" -v
python -m unittest discover -s tests -p "test_tmdb_client_movie_details.py" -v
```

## Swagger

`GET /movies/{tmdb_id}` exposes the enriched movie-detail result. Enter an
official TMDB movie ID in Swagger to fetch or read the movie and display its
saved genres and keywords.
