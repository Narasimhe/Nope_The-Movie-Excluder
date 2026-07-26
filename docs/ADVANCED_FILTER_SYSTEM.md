# Advanced Filter System

## Purpose

Advanced Search filters TMDB movies without considering personal movie
statuses. Watched, rewatch, watch-later, new-discovery, and excluded records do
not affect Advanced Search results.

Super Advanced Search will reuse the same filters later and then apply personal
status rules separately.

## Supported filters

- Include or exclude TMDB genres
- Include or exclude TMDB keywords
- Include or exclude original languages
- Include or exclude origin countries
- Genre, keyword, and country AND/OR logic
- Minimum and maximum TMDB rating
- Minimum TMDB vote count
- Release-year range
- Runtime range
- TMDB sorting
- Adult-content switch

## Filtering process

TMDB-native filters are sent together to:

```http
GET /discover/movie
```

Country and original-language rules that TMDB cannot express directly are
checked locally after results are returned.

Examples:

```text
(USA OR UK)
AND original language English
AND rating >= 7
AND (Science Fiction OR Thriller)
AND NOT (India OR Pakistan)
```

If an origin-country rule is active but a discovery result does not contain
country information, the filter system marks that movie as requiring a movie
details lookup before it can be accepted.

## Current scope

This step provides the reusable filter model, validation, TMDB query builder,
local country/language checks, and TMDB Discover client method.

Preference storage, service orchestration, status filtering, Swagger
endpoints, and the desktop UI are intentionally separate later steps.
