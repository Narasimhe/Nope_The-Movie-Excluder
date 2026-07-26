# Custom Keyword API

Custom movie tags can now be managed through the API.

## Add a custom keyword

`POST /movies/{tmdb_id}/keywords/custom`

Request body:

```json
{
  "name": "cold ambience"
}
```

The movie is fetched and saved first if it is not already available locally.
The returned keyword uses `is_custom = true`.

## Remove a custom keyword from one movie

`DELETE /movies/{tmdb_id}/keywords/custom/{keyword_id}`

Only a custom keyword link can be removed through this endpoint. Official TMDB
keywords are not affected.

## Delete a custom keyword everywhere

`DELETE /keywords/custom/{keyword_id}`

This permanently deletes the custom tag and removes it from every linked
movie. The response includes `affected_movie_count`. Official TMDB keywords
cannot be deleted through this endpoint.

## Rename or merge a custom keyword everywhere

`PUT /keywords/custom/{keyword_id}`

Request body:

```json
{
  "name": "wintry atmosphere"
}
```

If the new name is unused, the shared custom tag is renamed and every linked
movie immediately shows the new name.

If another custom tag already uses that name, the two tags are merged. All
movie links are moved to the existing tag, duplicate links are avoided, and
the old tag is deleted. Official TMDB keywords cannot be renamed or merged
through this endpoint.

`GET /movies/{tmdb_id}` returns the remaining official and custom keywords
together.
