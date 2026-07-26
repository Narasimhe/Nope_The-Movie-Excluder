# Genres and Keywords

Movie genres and keywords are stored through shared catalogue tables and
many-to-many links.

## Tables

- `genres`: official TMDB genre IDs and names
- `movie_genres`: links saved movies to genres
- `keywords`: official TMDB keywords and personal custom tags
- `movie_keywords`: links saved movies to keywords

Official keywords have a `tmdb_keyword_id` and `is_custom = 0`. Personal tags
have no TMDB keyword ID and use `is_custom = 1`.

The optional `position` in `movie_keywords` stores the order of official TMDB
keywords. Only positions 1 through 5 are allowed. Custom keywords have no
position.

## Repository behaviour

`MovieMetadataRepository` provides:

- `replace_movie_genres()`
- `get_movie_genres()`
- `replace_tmdb_keywords()`
- `add_custom_keyword()`
- `remove_custom_keyword()`
- `get_movie_keywords()`
- `get_tmdb_keywords()`
- `get_custom_keywords()`

Replacing official TMDB keywords keeps only the first five unique keywords and
does not remove custom tags.

## Verification

Run from the project root:

```powershell
python -m unittest discover -s tests -p "test_movie_metadata_repository.py" -v
```
