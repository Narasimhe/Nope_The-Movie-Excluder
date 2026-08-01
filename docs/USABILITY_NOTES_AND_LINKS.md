# Search, details, pagination, and Notes & Links

## Search workspace

- Simple, Advanced, and Super Advanced searches share one discovery workspace.
- The complete workspace can be hidden with one button. Its last open/closed state and the active unsaved filters are stored in SQLite.
- Filter cards begin collapsed and open individually.
- Multi-select trays close with **Done**, `Escape`, or a click outside. They do not close on a timer, so several values can be selected safely.
- Selected genres, languages, countries, people, keywords, and companies have clear actions.
- Saved profiles remain optional reusable presets. The current unsaved filter state is the normal active state; the UI no longer requires a default profile.
- Advanced results display local status and favourite badges but do not filter them. Super Advanced applies the personal status, notes, and favourite filters.

## Pagination

Movie and notebook lists use numbered pages with at most 20 results per page. This applies to title search, local keyword search, discovery searches, exact status lists, favourites, and Notes & Links. Status and favourite pages use SQLite `LIMIT` and `OFFSET` queries.

## Movie details

- The full page keeps the poster on the left and the primary information on the right.
- Year, language, and TMDB rating share a metadata line; genre chips sit at the far end of that line.
- Description, director, and the top five credited actors follow in that order.
- Up to 10 official TMDB keywords and all personal keywords appear under the poster. Personal keywords use a coloured border and can be removed from the current movie with `×`.
- Clicking a keyword searches the local database for other linked movies.
- Status saves use a visible `Saving…` then `✓ Saved` sequence without reloading the movie list behind the detail page.
- The heart is the only favourite control. It is available for Watched and Rewatch movies.
- **My Verdict** stores a whole-star score from 1 to 10 and can be cleared.
- Personal Memory opens by default and can be minimized.

Older cached movies are refreshed once when opened so their language, director, cast, and expanded keyword set can be stored locally.

## Notes & Links

The sidebar page is a separate general notebook; it does not replace notes attached to an individual movie.

Each entry has:

- type: Note or Link;
- title;
- optional body;
- URL for Link entries;
- created and updated timestamps.

Entries appear newest first and support text search, Note/Link filtering, year/month filtering, editing, deletion, and pagination. Deletion is a soft delete, so the database retains the row internally. Body lines beginning with `-` or `*` render as safe lists; raw HTML is never injected.
