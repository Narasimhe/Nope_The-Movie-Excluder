# Favorites API

Favorite is a personal flag and a strict subset of watched movies. A favorite
must have either `watched` or `rewatch` status.

## Favorite a movie

```http
PUT /movies/{tmdb_id}/favorite
```

```json
{
  "is_favorite": true
}
```

Use `false` to remove the movie from Favorites. Status, notes, verdict, and
custom keywords are preserved.

If the movie is `new_discovery`, `watch_later`, `excluded`, or untracked, the
API rejects the favorite action. It does not change the movie's status.

In the future UI, the heart control belongs on watched and rewatch movies.
Watched movies start with an empty heart and become favorites only when the
user explicitly selects them.

Changing a favorite movie to `new_discovery`, `watch_later`, or `excluded`
automatically removes it from Favorites. Moving between `watched` and
`rewatch` preserves the favorite.

## List favorites

```http
GET /movies/favorites
```

This returns favorite `watched` and `rewatch` movies with genres and personal
data. Every favorite also appears in the general Watched list.

## Super Advanced Search

`POST /movies/discover/super-advanced` accepts:

```json
{
  "included_statuses": [
    "watched",
    "rewatch"
  ],
  "favorite_only": true
}
```

This combines with the selected statuses, saved Advanced Search preference, and
optional notes query.

## Existing databases

Database initialization adds `is_favorite` safely with a default value of
`false`. Existing statuses, notes, verdicts, and other movie data are not
changed. Any inconsistent old favorite flag outside `watched` or `rewatch` is
normalized to `false`.
