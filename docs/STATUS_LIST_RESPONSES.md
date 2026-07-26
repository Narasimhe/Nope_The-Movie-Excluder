# Status List Responses

Movie status lists return lightweight movie summaries with:

- the saved movie fields;
- `genres`; and
- `user_data`, including the current personal status.

Official and custom keywords remain in `GET /movies/{tmdb_id}` rather than
being repeated across every list item.

Genre and user-data lookups are performed in batches for the complete list,
instead of running separate database queries for every movie.
