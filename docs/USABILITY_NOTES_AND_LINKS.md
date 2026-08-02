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

Movie and notebook lists use pages with at most 20 results per page. Title search, local keyword search, status lists, favourites, Movie Notes, and Notes & Links use exact totals. Advanced and Super Advanced searches calculate final page totals after manageable TMDB result sets have passed local director, country, language, status, notes, and favourite filters. For unusually broad searches that cannot be counted safely in one request, the UI shows only Previous, the current page, and Next instead of presenting raw TMDB page numbers as final matches.

## Movie details

- The full page keeps the poster on the left and the primary information on the right.
- Year, language, and TMDB rating share a metadata line; genre chips follow with a comfortable visual gap.
- Description, director, and the top five credited actors follow in that order.
- Up to 10 official TMDB keywords and all personal keywords appear under the poster. Personal keywords use a coloured border and can be removed from the current movie with `×`.
- Official keywords are informational. Clicking a personal keyword searches the local database for other movies carrying that personal tag.
- Director and actor names open an Advanced Search for that person.
- Person searches keep a visible link back to the movie that started the exploration.
- Related Movies appear after Personal Memory. Opening one adds it to a compact movie trail, so Back moves through the exploration one movie at a time.
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
- one or more URLs for Link entries, entered one per line;
- reusable tags that can be clicked to find related entries;
- created and updated timestamps.

Entries are ordered by their latest edit and support text/tag search, Note/Link filtering, year/month filtering, editing, deletion, and pagination. Year/month filters follow the latest edit date, so an older journal entry becomes current and visible after it is revised. The journal opens on the current Kolkata month and starts from August 2026. Dates are displayed and filtered using `Asia/Kolkata` time.

The index uses three equal compact cards per row on the 1280px effective desktop layout. Selecting a card opens a dedicated, centered reader rather than expanding text beside unrelated cards. Article text is capped at `68ch` for a comfortable reading line instead of stretching across the full reader shell. The reader provides contextual **Notes** or **Links** return navigation, Edit, Previous, Next, and Delete. Its latest edit time is prominent; when an entry has changed, the original creation date appears subtly at the bottom. Returning restores the index page and scroll position.

Deletion is initially a soft delete. The Storage page can permanently purge deleted entries. Body lines beginning with `-` or `*` render as safe lists; raw HTML is never injected.

## Related Movies

Related results hide Watched, Rewatch, and Nope titles by default. Nope is never offered as a related recommendation. When familiar titles exist, a small control can reveal the Watched/Rewatch movies. Poster images use a complete 2:3 frame with `object-fit: contain`, so artwork is not cropped.

## Looking Out For and storage

See [LOOKING_OUT_FOR_AND_STORAGE.md](LOOKING_OUT_FOR_AND_STORAGE.md) for the time-aware future-release list, in-app release badges, demo bootstrap, and safe cache cleanup rules.
