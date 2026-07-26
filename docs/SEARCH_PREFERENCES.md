# Search Preferences

Search preferences are reusable Advanced Search filter profiles stored in the
same local SQLite database as the rest of Movie Excluder.

They are separate from `user_movie_data`:

- `user_movie_data` stores a status, notes, and personal rating for a movie.
- `search_preferences` stores reusable discovery filter combinations.

## Table

The `search_preferences` table contains:

- `preference_id`
- `name`
- `filters_json`
- `is_default`
- `created_at`
- `updated_at`

The filter JSON is validated by `AdvancedMovieFilters` before it is saved.
Only one preference can be marked as the default.

Example profile:

```json
{
  "name": "American Sci-Fi",
  "filters": {
    "include_genre_ids": [878],
    "include_origin_countries": ["US"],
    "exclude_origin_countries": ["IN", "PK"],
    "minimum_rating": 7,
    "minimum_vote_count": 100
  }
}
```

The repository supports creating, updating, reading, listing, deleting, and
selecting a default preference.

Swagger endpoints and Advanced Search execution will be added separately.
