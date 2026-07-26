# People and Production-Company Filters

Advanced Search can now include actors, exact directors, and production
companies. It can also exclude production companies.

## Lookup endpoints

Names are converted to official TMDB IDs before they are stored in a search
preference.

- `GET /people/search?query=Nolan`
- `GET /companies/search?query=Syncopy`

The desktop UI can call these endpoints after the user types a few letters,
show the returned choices, and save the selected TMDB ID.

## Search-preference fields

```json
{
  "include_actor_ids": [31],
  "actor_logic": "or",
  "include_director_ids": [525],
  "director_logic": "or",
  "include_company_ids": [9993],
  "exclude_company_ids": [],
  "company_logic": "or"
}
```

All the remaining Advanced Search fields can stay empty or `null`.

## How the filters work

- Actors use TMDB's `with_cast` filter.
- Production companies use `with_companies`.
- Excluded production companies use `without_companies`.
- Directors use `with_crew` to narrow the TMDB results, followed by an exact
  check of the person's movie credits. Only credits whose job is `Director`
  are accepted.
- Comma-style `and` logic requires every selected ID.
- Pipe-style `or` logic accepts any selected ID.

The exact director check is inherited by Super Advanced Search.

## Swagger example: Christopher Nolan

1. Open `GET /people/search`.
2. Enter `Nolan` and run it.
3. Find Christopher Nolan and copy his returned `id`.
4. Create or update a search preference.
5. Put that ID in `include_director_ids`.
6. Leave unrelated filters empty or `null`.
7. Run `GET /movies/discover/advanced` with that preference.

The response excludes movies where the selected person was only a writer or
producer.
