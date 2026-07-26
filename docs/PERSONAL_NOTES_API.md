# Personal Notes API

## Set, update, or clear notes

```http
PUT /movies/{tmdb_id}/notes
```

Save or update:

```json
{
  "notes": "Beautiful cold ambience and quiet pacing."
}
```

Clear the note:

```json
{
  "notes": null
}
```

Blank text also clears the note. If the movie is not cached yet, its TMDB
details are fetched before the personal record is created.

## Search all personal notes

```http
GET /movies/notes/search?query=cold%20ambience
```

This is a local SQLite search. It is case-insensitive, supports partial text,
and makes no TMDB request.

Super Advanced Search also accepts an optional `notes_query` so note text can
be combined with the saved Advanced Search preference and selectable personal
statuses.
