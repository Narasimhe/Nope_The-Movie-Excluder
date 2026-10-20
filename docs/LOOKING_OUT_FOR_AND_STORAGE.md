# Looking Out For, release time, and local storage

## Looking Out For

**Looking Out For** is secondary tracking for a movie with a confirmed future TMDB release date. It is deliberately separate from the main statuses, so tracking an unreleased title does not incorrectly mark it New Discovery, Watch Later, Watched, Rewatch, or Nope.

- A title can be added from its movie detail page only when its exact release date is later than today.
- The list appears in the footer and is paginated.
- Release state is calculated using `Asia/Kolkata`: upcoming, within seven days, today, or released.
- The optional in-app badge counts qualifying titles across the complete list, not merely the currently visible page.
- When a tracked title reaches its release date, it can be moved deliberately to Watch Later.
- Release dates older than the refresh interval are checked against TMDB. A TMDB outage does not prevent the locally saved page from opening.

The notification toggle controls only the in-app badge and summary. It never creates Windows or browser notifications.

## Database bootstrap

The public package includes `data/demo.db`, a clean sample template. `data/movie_excluder.db` remains the only writable user database.

At first launch, when the working database is absent, `ensure_database_exists()` copies the template once with `shutil.copyfile`. The FastAPI lifespan then runs `initialize_database()` so all current migrations are present before requests are served. If the working database already exists, the template is ignored and the existing data is migrated in place.

The demo can be rebuilt reproducibly with `python scripts/build_demo_database.py`. The builder writes a temporary file, validates it with SQLite's integrity check, and atomically replaces only `demo.db`.

## Storage page and cleanup

The Storage page reports the SQLite file size and useful record counts. Its cache cleanup removes only old TMDB-only movie rows that have not been accessed within the chosen retention period.

A movie is protected from cache cleanup when it has any personal significance, including:

- personal status, verdict, notes, or favourite data;
- a personal/custom movie keyword;
- Looking Out For tracking.

Genres, official TMDB keywords, and cached credits attached only to a disposable movie are removed by SQLite cascade rules. Orphan metadata is cleaned afterward. Deleted general notebook entries remain recoverable until the separate permanent purge action is confirmed.

For complete architectural details on automated pre-cleanup backups, SQLite vacuum compaction, dry-run previews, active shelf background refresh, and data export, see `docs/DATABASE_HEALTH_AND_SMART_CLEANUP.md`.

