# Search Preference API

These FastAPI endpoints manage reusable Advanced Search profiles. Swagger
generates its testing interface automatically from these real endpoints.

## Endpoints

```http
POST   /search-preferences
GET    /search-preferences
GET    /search-preferences/{preference_id}
PUT    /search-preferences/{preference_id}
PUT    /search-preferences/{preference_id}/default
DELETE /search-preferences/{preference_id}
```

## Example: create a preference

```json
{
  "name": "American Sci-Fi",
  "filters": {
    "include_genre_ids": [878],
    "exclude_genre_ids": [],
    "genre_logic": "or",
    "include_keyword_ids": [],
    "exclude_keyword_ids": [],
    "keyword_logic": "or",
    "include_original_languages": ["en"],
    "exclude_original_languages": ["hi", "te"],
    "include_origin_countries": ["US"],
    "exclude_origin_countries": ["IN", "PK"],
    "country_logic": "or",
    "minimum_rating": 7,
    "maximum_rating": null,
    "minimum_vote_count": 100,
    "release_year_from": 2000,
    "release_year_to": null,
    "runtime_min": null,
    "runtime_max": 180,
    "sort_by": "vote_average.desc",
    "include_adult": false
  },
  "is_default": true
}
```

Creating or updating a profile validates all filters before writing to SQLite.
Invalid ranges, codes, logic values, duplicate names, and include/exclude
conflicts return HTTP `400`. Missing profiles return HTTP `404`.

These endpoints manage saved preferences only. The Advanced Search execution
endpoint will be added separately.
