# Discovery Search UI

The homepage is now a movie-discovery workspace. `New discovery` remains a
personal movie status in the left library menu.

## Search modes

- **Simple Discovery** runs a broad TMDB discovery without checking local user
  statuses.
- **Advanced Search** applies TMDB filters without checking local user statuses.
- **Super Advanced** uses the same filters and then applies the selected local
  status, notes, untracked, and favourite rules.

## Profiles

Search profiles are reusable filter presets. A profile can be created, loaded,
updated, marked as default, or deleted from the UI. Super Advanced personal
filters are stored with the profile as well.

Filters can also be run without saving a profile. The API accepts direct filter
objects through `POST /movies/discover/advanced` and
`POST /movies/discover/super-advanced`.
