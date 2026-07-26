# Movie Status List API

## Endpoint

```http
GET /movies/status/{status}
```

This endpoint returns movies whose saved status exactly matches the requested
status.

Valid status values:

- `new_discovery`
- `watch_later`
- `watched`
- `rewatch`
- `excluded`

Example:

```http
GET /movies/status/watch_later
```

Each movie includes its cached movie fields, `genres`, and `user_data`.
Keywords remain available from the individual movie details endpoint:

```http
GET /movies/{tmdb_id}
```

An invalid status returns HTTP `400`.

## Existing watched endpoint

```http
GET /movies/watched
```

This older endpoint remains unchanged for compatibility. It returns both
`watched` and `rewatch` movies. Use the generic status endpoint when an exact
status match is required.
