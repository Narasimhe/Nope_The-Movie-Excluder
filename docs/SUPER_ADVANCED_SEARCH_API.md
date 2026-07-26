# Super Advanced Search API

Super Advanced Search combines a saved Advanced Search preference with
selectable personal-status filtering.

```http
POST /movies/discover/super-advanced
```

Default request:

```json
{
  "preference_id": null,
  "page": 1,
  "included_statuses": [
    "new_discovery",
    "watch_later"
  ],
  "include_untracked": true,
  "notes_query": null,
  "favorite_only": false
}
```

If `preference_id` is `null`, the default search preference is used.

`include_untracked` controls movies that do not have a `user_movie_data`
record. Untracked is a computed search state, not a sixth stored status.

Every stored status is independently selectable:

- `new_discovery`
- `watch_later`
- `watched`
- `rewatch`
- `excluded`

`notes_query` is optional. When supplied, it performs a case-insensitive,
partial search inside personal notes. Untracked movies cannot match a notes
query because they have no personal record.

`favorite_only` is optional and defaults to `false`. When it is `true`, only
movies whose personal data has `is_favorite = true` can match. Favorites are
always `watched` or `rewatch`, so those statuses must be selected. Notes
filters still apply.

Examples:

Fresh movies only:

```json
{
  "preference_id": null,
  "page": 1,
  "included_statuses": [],
  "include_untracked": true,
  "notes_query": null,
  "favorite_only": false
}
```

Watched and rewatch movies only:

```json
{
  "preference_id": null,
  "page": 1,
  "included_statuses": [
    "watched",
    "rewatch"
  ],
  "include_untracked": false,
  "notes_query": null,
  "favorite_only": false
}
```

Notes containing "cold ambience" within the default visible statuses:

```json
{
  "preference_id": null,
  "page": 1,
  "included_statuses": [
    "new_discovery",
    "watch_later"
  ],
  "include_untracked": false,
  "notes_query": "cold ambience",
  "favorite_only": false
}
```

Favorites within selected statuses:

```json
{
  "preference_id": null,
  "page": 1,
  "included_statuses": [
    "watched",
    "rewatch"
  ],
  "include_untracked": false,
  "notes_query": null,
  "favorite_only": true
}
```

The service bulk-loads user data before making country-detail calls. Movies
hidden by the selected status rules therefore do not cause unnecessary TMDB
detail requests.

Each returned movie includes `user_data`. It is `null` for untracked movies.
