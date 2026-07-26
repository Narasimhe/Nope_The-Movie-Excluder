# Local Keyword Search

The app can search cached movies using their saved official TMDB keywords or
personal custom tags. This search never calls TMDB.

## Endpoint

`GET /movies/keywords/search`

Query parameters:

- `query`: full or partial keyword name, such as `marvel`
- `keyword_type`: `all`, `custom`, or `tmdb`

Example:

```text
GET /movies/keywords/search?query=marvel&keyword_type=all
```

The search is case-insensitive. Each movie appears only once even when several
matching keywords are linked to it. Results are sorted alphabetically by movie
title.

The response contains:

- all matching keyword records and their movie counts;
- cached movies with genres and personal user status;
- `matched_keywords` on each movie, explaining why it matched.

## Franchise use

A custom tag such as `Marvel` is the most reliable way to maintain a personal
franchise group. Official TMDB keywords are also searchable, but only the Top
5 official keywords are cached for each movie.
