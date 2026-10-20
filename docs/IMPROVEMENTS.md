# Movie Excluder — Improvements & Polish Tracker

A central record of recent fixes, active improvements, and future backlog items for Movie Excluder.

---

## 1. Done (Recently Completed Fixes & Polish)

### A. Watch Later & Rewatch Full Collection Restore
* **Root Cause**: The library filter drawer had a lingering default setting that silently enforced English-only matching on load and reset, hiding all non-English or re-tagged movies (e.g., only 12 of 32 Watch Later movies showed).
* **Fix Applied**: Removed the hardcoded language filter so the drawer starts completely unconstrained. Switching shelves now automatically resets drawer filters to clean state, showing 100% of all saved movies by default.

### B. Global Personal Library Search Engine
* **Capability**: Upgraded the drawer search box from a single-page screen filter into a full database search.
* **Scope Switch**:
  * **All Shelves (Default)**: Searches your entire private collection across all shelves (Watched, Watch Later, Rewatch, Favorites, and NOPE) across all pages.
  * **Current Shelf**: Restricts the search specifically to the shelf currently being viewed.
* **Status Badges**: Each movie card in search results displays its personal shelf status (*Watched*, *Watch Later*, *Rewatch*, *Nope*).
* **Instant Reset**: Clearing the query or clicking "Reset" restores the normal shelf view.

### C. Genre Matching Bug Resolution
* **Root Cause**: Local database movies stored genre identifiers under `tmdb_genre_id`, while the filter buttons checked only `id`, resulting in 0 matches and false empty screens (e.g., Science Fiction notes).
* **Fix Applied**: Normalized genre identifiers across both backend and frontend to check both `id` and `tmdb_genre_id`. Science Fiction and other genres now accurately display all matching movies.

### D. Context-Aware Empty & Zero States
* **Filter Zero Results**: Replaced generic placeholder text with *"No movies match your filters — Try adjusting or clearing your filters"* and an actionable **"Reset filters"** button.
* **Movie Notes**: Specific messages for empty notes and notes search.
* **Shelf Specific**: Relevant empty states per shelf (*Watched*, *Watch Later*, *Rewatch*, *Favorites*, *Nope*).

### E. Grid-Anchored Centered Pagination
* **Centering**: Anchored the movie results pagination bar directly to the 670px width of the compact movie grid rather than stretching across the entire monitor.
* **Spacing**: Increased vertical breathing room to `3.5rem` above the pagination buttons.

### F. Search Header & Ghost Pagination (done — Oct 4)
* All-shelves search now retitles the page **"Personal Library"** (kicker: *Personal library search*). Current-shelf search keeps the shelf name. Clearing the query restores the shelf title.
* Ghost pagination fixed: added `#pagination.is-hidden { display: none !important; }` (the ID rule was overriding `.is-hidden`). This also fixes pagination leaking into other views that hide it.
* Pagination is now rendered *before* drawer filters are applied, so active filters/search reliably hide it.
* **Reset** while searching now reloads the real shelf (previously it would re-show the search results unfiltered). Clicking a shelf in the sidebar always exits search mode.

### G. Compact Language & Country Filters with `+` Adder (done — Oct 4)
* **Always visible**: Languages — English, French, Spanish, German, Japanese, Korean. Countries — United States, United Kingdom, France, Germany, Japan, South Korea.
* **Also visible automatically**: any language/country you've actively set (include/exclude), so an active filter is never hidden.
* **Hidden, still applied**: default-excluded languages (Hindi, Telugu, Tamil, Malayalam, Kannada, Bengali, Marathi, Punjabi, Urdu, Arabic) no longer appear as red chips. They keep excluding in the background. The Languages badge no longer counts them.
* **`+` chip** at the end of each cloud (Discover Languages, Discover Countries, Library Languages) opens a small search box. Type, then click or press Enter to add. Esc or clicking outside closes it. Options that are excluded by default carry an *excluded by default* hint. If you add one, it shows its current (excluded) state and you can toggle it.
* **Remove an added chip**: hover it and click the small `×`. Primary chips can't be removed.
* Added chips are remembered per browser (`localStorage`: `nope_pinned_languages`, `nope_pinned_countries`). Languages added in Discover also show in the Library drawer, and vice versa.
* The language and country lists you can pick from are bigger now: 41 languages and 35 countries.

### H. UTF-8 Encoding & Mojibake Resolution (done — Oct 4)
* **Root Cause**: `app/web/index.html` contained double-encoded characters (UTF-8 bytes misinterpreted as Windows-1252/CP1252), causing the browser to render `â–¾` for dropdown carets (`▾`), `â€¦` for search placeholder ellipsis (`…`), and garbled icons (`â† `, `â™¥`, etc.).
* **Fix Applied**: Sanitized and restored all 14 corrupted byte sequences across `app/web/index.html` to clean UTF-8 (`▾`, `…`, `–`, `—`, `♥`, `✎`, `✕`, `↻`, `→`, `←`, `•`, `＋`, `🏷️`, `🔍`). Bumped static cache buster to `v=20261004b`.

### I. Multi-Language & Multi-Country TMDB Discover Search (done — Oct 5)
* **Root Cause**: In `app/advanced_filters.py`, multiple included languages/countries were previously stripped from TMDB query parameters, triggering fallback English defaults that dropped results to 1 movie.
* **Fix Applied**: Updated `to_tmdb_params()` to send pipe-delimited values (`ko|es`, `KR|ES`), leveraging TMDB's native OR querying across the entire worldwide catalog.

### J. Full-Database Standalone Library Filtering (done — Oct 5)
* **Capability**: Selecting library filters (languages, genres, year ranges, keywords, cast & crew) now queries the entire collection directly without requiring any keyword in the search box.
* **Scope Aware**: Respects the All Shelves vs. Current Shelf scope toggle.
* **Dynamic Recovery**: Clearing the filters automatically restores standard shelf pagination.

### K. Library Cast & Crew Credits Matching & Scoped Autocomplete (done — Oct 5)
* **Database Credits Matching**: Replaced the plot overview text search with exact joins on `movie_credits`, accurately matching actor and director collections.
* **Collection-Scoped Autocomplete**: Directed drawer autocomplete to `/movies/library/people`, showing only people present in your local collection (optionally scoped to active shelf).
* **Disabled Filmography Hijack**: Removed filmography click hijacking on library people chips so they function strictly as collection filters without triggering TMDB lifetime filmography requests.

### L. Persistent Library Filter State Across Shelf Navigation (done — Oct 5)
* **Behavior**: Removed the aggressive auto-reset on shelf navigation. Selected filters (e.g. Swedish, 1990s, or Christopher Nolan) now persist seamlessly as you move between *Favorites*, *Watched*, *Watch Later*, *Rewatch*, and *Nope*.
* **Explicit Reset**: Filters are cleanly reset whenever the user taps the prominent "Reset" button or "Reset filters" on empty states.

### M. Clean 30-Poster Shelf Pagination (6 × 5 Complete Rows) (done — Oct 5)
* **Design & Geometry**: Standardized shelf presentation across all shelves (*Favorites*, *Watched*, *Watch Later*, *Rewatch*, *Nope*, and *Movie Notes*) to exactly 30 posters per page (6 columns × 5 rows).
* **Eliminated Sprawl**: Replaced overwhelming 60–80+ poster loads with clean, centered pagination (e.g., 83 Favorites cleanly paginated as 30, 30, 23).

### N. Display TMDB Vote Count in Movie Detail Modal (done — Oct 5)
* **Display**: Formatted and displayed TMDB vote count next to the rating in the movie detail popup (e.g. `★ 8.2 TMDB (14.5k votes)`).
* **Database Persistence**: Added `vote_count` column to the `movies` table with automatic database migration.

### O. Full-Collection Library Sorting (Database-Wide) (done — Oct 9)
* **Design & Capability**: Fixed shelf and library sorting across all 4 modes (*Newest first*, *Oldest first*, *Title A–Z*, and *Recently updated*).
* **Root Cause Fixed**: Previously, backend shelf pagination returned only titles A–F on Page 1, and frontend sort chips only sorted those 30 in-memory titles.
* **Resolution**: Shelves now load the full collection from SQLite, sort the entire collection database-wide before slicing, and render clean 30-poster pages. Selecting "Newest first" on any shelf (e.g., New Discoveries) now reliably displays the newest 2026 releases first across the entire alphabet.

### P. Notes Reader View Isolation & Refresh Collision Fix (done — Oct 9)
* **Root Cause Fixed**: Refreshing (`F5`) an opened note previously booted Discover and bled Discover controls (search input, preset pills, and pagination) into the top of the Notes page.
* **Resolution**: Added URL hash routing (`#entry-reader:<id>`) and session persistence for opened notes. On refresh, the application stays locked to the active note, loads the note content seamlessly, and strictly suppresses Discover controls, search workspace, and pagination.

### Q. First-Class Personal Keyword Search & Drawer Autocomplete (done — Oct 9)
* **Capability**: Searching your personal library in the search box now matches custom tags and movie keywords directly via database join on `movie_keywords` and `keywords`.
* **Drawer Autocomplete**: Upgraded the Library drawer "Keywords & Themes" autocomplete to query `/movies/library/keywords`, prioritizing personal custom tags (`is_custom = 1`, badge `🏷️`, labeled *Personal tag*) above general library keywords.

### R. Grey: In-App AI Cinema Companion (done — Oct 17)
* **Docked Right Column Architecture**: Google Chrome Side Panel style full-height companion panel (`#grey-drawer`) sliding out seamlessly beside the movie grid without locking document scrolling.
* **Integrated Input Card**: Ergonomic 75px card with auto-routing model indicator (`✦ Auto` / `Flash` / `Pro`) and bottom-right send trigger with keyboard shortcuts (`Enter` to send, `Shift+Enter` for newline, `Esc` to collapse).
* **Taste Dossier Grounding**: Automatic SQLite extraction of the user's top-rated favorites, personal notes, active watchlist, and discards to provide deeply personalized recommendations with zero conversational fluff.
* **Intelligent Auto-Routing**: Dynamically routes research queries (Rotten Tomatoes, IMDb, awards, box office, deep thematic breakdowns) to enhanced reasoning while executing fast library filters with lightweight speed.
* **Interactive Action Pills**: Dynamic shortcut pills (`[ ⚡ Ephemeral Shelf ]`, `[ 🎬 Movie Card ]`, `[ ⏱️ Prompt ]`) for instant library exploration.

---

### S. Journal Drafts System & Staging Workflow (done — Oct 17)
* **Scope**: Strictly for **Journal Entries / Blogs** (`general_entries`). Personal movie memory notes remain immediate and unchanged.
* **Database Migration**: Added `status` column (`'published' | 'draft'`) to `general_entries` with an optimized index on `(is_deleted, status, is_archived, updated_at DESC)`. All existing entries are preserved and defaulted to `'published'`.
* **Drafts Sidebar Tray**: Added `📝 Drafts (<count>)` navigation link in the Notes sidebar with real-time draft badge counts. Selecting Drafts filters the notebook strictly to draft entries.
* **Dual Action Composer**: Integrated dual `Save draft` (secondary action) and `Publish to Journal` (primary action) buttons into the journal editor modal.
* **Reader Promotion**: Draft entries in reader mode feature a prominent `Publish to Journal` button that promotes the entry and refreshes sidebar counts with one click.
* **Draft Badge on Cards**: Draft cards in the notebook display a subtle gold `📝 Draft` badge.

### T. Dedicated Plain-Text System Prompt File & Hot-Reloading (`app/prompts/grey_system_prompt.md`) (done — Oct 17)
* **Decoupled Architecture**: Extracted Grey's system prompt from Python code into a dedicated Markdown file (`app/prompts/grey_system_prompt.md`).
* **Plain English Customization**: Allows reading and editing Grey's personality, rules, tone, and cinema taste philosophy in plain English without modifying application code.
* **Hot-Reloading**: Automatically loads and populates template placeholders (`{{INSPECTED_INFO}}`, `{{INSPECTED_TITLE}}`, `{{FAVORITES_JSON}}`, `{{WATCHLIST_JSON}}`, `{{CURRENT_VIEW}}`, `{{ACTIVE_FILTERS_JSON}}`) dynamically on every chat turn.
* **Grey Auto-Drafting Action**: Enabled the `create_draft` action so natural language requests (e.g. *"draft an essay on..."*, *"write a comparison between X and Y"*) automatically compile and persist a draft into SQLite and return a `[ 📖 Open Draft ]` pill.
* **Active Screen & Modal Synchronization**: Active movie focus override ensures that whenever a movie is open on screen, pronouns ("it", "this movie", "its rating") anchor directly to that movie, superseding past chat turns.
* **Multi-Model Quota Fallback**: Automatic cascade through Gemini models (`gemini-3.8-flash` → `gemini-3.7-flash` → `gemini-3.6-flash` → `gemini-3.5-flash` → `gemini-flash-lite-latest`) prevents quota failures.

### U. Grey Daily Session Persistence & Frugal Journal Taste Memory (done — Oct 17)
* **Daily Session Continuity**: Today's active chat session in Grey automatically persists in browser storage across page refreshes (`F5`), tab reloads, and drawer toggles. Rolls over cleanly to a fresh slate each day, or resets instantly whenever the user clicks the `⟲` button.
* **One-Click "Save to Draft" Action**: Every response bubble from Grey now features an ergonomic `📝 Save to Draft` action button. Clicking it immediately saves the response into your Journal Drafts as a draft note, updates sidebar draft counts, and marks the bubble as `✓ In Drafts`.
* **Frugal Journal Taste Dossier**: Grey's taste dossier now includes a compact index of your published articles (titles and core themes/tags). When you ask about your essays (e.g. *"Based on my essay on Settlers, what should I watch?"*) or discuss a movie you've written an essay about, Grey dynamically pulls the relevant excerpt into context, ensuring Grey learns from your curated thoughts without prompt bloat.

---

## 2. Next (Active & Queued Features)

### Item 1: Full Markdown Styling in Journal Reader
* Expand `formatRichText` and `appendEntryBody` to support:
  * Bold (`**strong**`)
  * Italics (`*film title*`)
  * Section headings (`## Heading 2`, `### Heading 3`)
  * Blockquotes (`> Dialogue or review quotes`)
  * Inline tags / code (`` `keyword` ``)

### Item 2: Cinematic Banner Images for Journal Entries
* Optional backdrop / banner image field for journal articles and film essays (e.g., pasting an image URL or auto-attaching a TMDB backdrop from an inspected movie).
* Renders a cinematic hero header at the top of the entry reader.

### Item 3: Keyword-Driven Discovery Filter Generator
* Generate intelligent TMDB discovery filters based on selected journal articles, themes, or keyword clusters.

---

## 3. Much Later (Future Backlog)

### Item A: Personal Library Export, Backup & Google Sheets Sync
* **The Goal**: Offline ownership and optional cloud accessibility for your personal library data (shelves, ratings, notes, and favorites).
* **Placement**: Located on the **Storage** page (`Local data → Storage`).
* **Components**:
  * **Offline Backup (JSON / CSV)**: 1-click download of all user data as timestamped JSON (full fidelity) or CSV (spreadsheet-friendly).
  * **Google Sheets Webhook Sync (Optional Cloud)**: Connect a Google Apps Script Web App URL to push personal library snapshots directly into a private Google Sheet for mobile access and sharing, without Google Cloud Console overhead.

---

*Last Updated: October 17, 2026*

