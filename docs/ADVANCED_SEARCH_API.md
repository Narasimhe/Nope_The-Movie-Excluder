# Advanced Search API

Advanced Search loads a saved search preference and executes it against TMDB
Discover.

```http
GET /movies/discover/advanced
```

Query parameters:

- `preference_id`: optional saved preference ID
- `page`: TMDB results page, starting at `1`

If `preference_id` is omitted, the default search preference is used.

Example:

```http
GET /movies/discover/advanced?preference_id=1&page=1
```

## Processing

1. Load and validate the selected preference.
2. Send supported filters to TMDB Discover.
3. Check local original-language rules.
4. Fetch movie details when origin-country rules require them.
5. Exclude any movie matching an excluded origin or production country.
6. Return the filtered page.

Advanced Search deliberately ignores all personal movie statuses. Super
Advanced Search will add status-aware rules later.

The response includes:

- The preference used
- TMDB page totals
- Candidate count before local filtering
- Result count after local filtering
- Number of country-detail lookups
- Filtered movies

TMDB totals describe the server-side filter results before local exclusions.
Therefore, a returned page can contain fewer than 20 movies after country or
language exclusions.
