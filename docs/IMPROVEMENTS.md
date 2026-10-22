> **AI INSTRUCTION**: Only read and process items listed under **🟢 Pending Tasks (Active Focus)**. Treat **✅ Completed Tasks** as historical archive data only—do not re-implement, modify, or discuss them unless explicitly requested by the user.

# Project Improvements & Backlog

## 🟢 Pending Tasks (Active Focus)

- [ ] **Native Markdown Table Support in Notes & Grey Table Formatting**
  * **Goal**: Support standard Markdown tables (`| Col 1 | Col 2 |`) in notes and journal posts with dark-theme styling, and teach Grey to format and update movie comparison tables.
  * **Scope**:
    * **Frontend Markdown Parser ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: In `appendEntryBody`, detect pipe-delimited table rows (`| ... |`), parse header rows, separator rows, and data rows into structured `<table>`, `<thead>`, `<tbody>` elements with support for inline links, bold text, and formatting.
    * **Modern Dark CSS ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Add responsive, clean dark styling with subtle borders, muted headers, comfortable cell padding, and horizontal scroll wrapper for narrow screens.
    * **Grey Skill Integration ([`notes_editor.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/notes_editor.md))**: Teach Grey to output clean Markdown tables when asked for film comparisons, rankings, or side-by-side lists, and to mimic existing table structures when adding rows to notes that use tables.


---

## ✅ Completed Tasks

- [x] **Modular Skill-Based Prompt Architecture for Grey**
  * **Goal**: Decompose Grey's monolithic 224-line prompt into a lean core persona and dedicated on-demand skill modules, preventing instruction conflicts, context dilution, and token bloat.
  * **Architecture**:
    * **Core Persona ([`grey_core.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/grey_core.md))**: Houses Grey's cinephile voice, craft philosophy, behavioral rules, and JSON action output envelope (~75 lines).
    * **Dynamic Skill Modules ([`app/prompts/skills/`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/))**:
      - [`notes_editor.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/notes_editor.md): Format mimicry, in-place upsert, `>>` Notion toggles with double blank line exit, zero redundancy.
      - [`related_curator.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/related_curator.md): Script craft, pacing, tension, YES/NOPE verdicts on related movies.
      - [`filmography_explorer.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/filmography_explorer.md): Career context, department filter awareness (acting vs directing).
      - [`watchlist_builder.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/watchlist_builder.md): 8-12 tranche synthesis, Notion toggles with Cast/Synopsis/Why YES.
      - [`library_ops.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/library_ops.md): Shelf moves, ratings, verdicts, batch actions, and library awareness.
    * **Dynamic Context Router ([`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py))**: Inspects current view, open note, active person, or slash command to dynamically inject only the active skill directive into `{{ACTIVE_SKILL_DIRECTIVE}}`.
    * **Unit Tests ([`test_grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_grey_service.py))**: Added tests verifying that screen states route exclusively to their intended skill module without loading unrelated instructions.


- [x] **Grey In-Note Deduplication & Human-Readable Notion Toggle Formatting**
  * **Goal**: Prevent Grey from creating duplicate movie entries in existing notes when adding critiques/details, and guarantee that toggles use clean, human-readable Notion-style `>> Title` syntax followed by two consecutive blank lines to exit toggle mode.
  * **Fix**:
    * **In-Place Entity Upsert**: In [`grey_system_prompt.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/grey_system_prompt.md), instructed Grey to inspect existing notes and always update/expand existing movie lines in-place instead of appending duplicate bullets at the bottom.
    * **Notion `>>` Toggle & Double Blank Lines**: Taught Grey that raw HTML tags like `<details><summary>` are forbidden in plaintext notes; Grey must format toggles using clean `>> Title (Year)` syntax followed by two consecutive empty lines to cleanly exit back to root level.
    * **Deterministic Python Safeguard**: In [`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py), `_deduplicate_and_format_note_body` normalizes toggles into clean `>> Title` format, appends double newlines to guarantee toggle exit, replaces bare bullets in-place, and strips any duplicate appended mentions.
    * **Frontend Toggle Boundaries**: Updated [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js) markdown parser so top-level bullets (`• `, `- `, `* `) immediately close active Notion toggles.
    * **Unit Tests**: Added test coverage in [`test_grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_grey_service.py) verifying in-place upsert, toggle exit boundaries, and deduplication.


- [x] **Offline Saved Profile & Poster Speed Optimizations**
  * **Goal**: Eliminate network timeout delays when viewing saved profiles and posters while offline, making offline browsing instant (<10ms).
  * **Fix**:
    * **Local-First Poster Fast-Path**: Updated `createPoster()` in [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js) to load `/images/posters/...` from local disk cache first, completely bypassing external CDN network roundtrips and avoiding 15–30s browser connection timeouts.
    * **Backend Poster Circuit Breaker**: Added `_offline_until` circuit breaker and reduced download timeout to 1.5s in [`poster_cache_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/poster_cache_service.py). When offline, uncached poster requests abort immediately in <1ms without blocking FastAPI worker threads.
    * **Fail-Fast TMDB Client Circuit Breaker**: Added connection error circuit breaker to [`tmdb_client.py`](file:///f:/Movie_Excluder/movie-excluder/app/tmdb_client.py). When offline, uncached queries fail fast (0ms) instead of retrying for 30s.
    * **Discovery Prefetch Timeout Race**: Wrapped speculative buffer pages (pages 2 & 3) in [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js) with a 1.5s timeout race so uncached speculative pages never delay cached primary results.


- [x] **Grey Note Editing Format & Style Mimicry**
  * **Goal**: Teach Grey to inspect and strictly mimic the existing format of a note when editing or appending entries, rather than imposing a generic multi-line Notion-style toggle.
  * **Fix**:
    * Updated [`grey_system_prompt.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/grey_system_prompt.md) with explicit Format Mimicry Rules: when updating existing notes, Grey must inspect the existing entries and seamlessly match single-line bullets (e.g. `• Title (Year) (Cast/Director) - [IMDb](url)`), numbered items, or tables.
    * In [`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py), auto-resolve existing note content into `inspected_note_info` whenever a note is referenced by title or keywords, and added pattern-detection to the fallback action converter to match bullet characters (`•`, `-`, `*`) and IMDb link style.

- [x] **Discover Simple Title Search Stability & Persistent UI**
  * **Goal**: Prevent the left sidebar, toolbar search bar, and top navigation highlight from disappearing when executing a simple title search in Discover.
  * **Fix**:
    * Simple title searches now anchor stably inside the `discover` view (`setActiveView("discover")`).
    * The left sidebar (`#discovery-workspace` and `#advanced-controls`) remains fully mounted and visible with all filters intact instead of collapsing into a blank black void.
    * The canvas search toolbar (with query input, Nope Mode toggle, profile ribbon, and formatted live match count) remains on screen for instant query refinement or clearing.
    * Added native search clear listener so clearing the search input seamlessly reloads default discovery.
    * Automatically de-selects active ribbon profile chips during simple global title searches to avoid misleading active states.

- [x] **Movie Notes Lens Visual Distinction (Wide Full-Width Pill)**
  * **Goal**: Visually distinguish **Movie Notes** from the 6 storage shelves to clearly reflect its role as a modifier/lens.
  * **Design**:
    * **Full-Width Lens Pill**: Spans Movie Notes as a sleek full-width pill below the 2×3 shelf grid (`grid-column: 1 / -1; width: 100%`).
    * **Engaged Lens State**: When active, illuminates with a warm gold frame and subtle lens glow (`#f2c94c`), making it immediately clear that the notes filter lens is engaged.
    * **Divider**: Kept clean without redundant horizontal lines as requested.

- [x] **Context-Aware Notes Search in Movie Notes Mode**
  * **Goal**: When viewing **Movie Notes**, sidebar search automatically searches strictly inside personal movie notes without requiring the user to type `notes: <query>`.
  * **Behavior**:
    * Dynamic search placeholder: switches to `"Search your movie notes…"` in Movie Notes view, and `"Search library (or title:, plot:)…"` on general shelves (`notes:` prefix hint removed).
    * Prefix bypass: Any query without a prefix searches notes; explicit `title:` and `plot:` prefixes are still respected.
    * Shelf scoping: Paired shelves filter notes to that specific shelf (e.g. Watched + Notes).

- [x] **Filmography Header Stacked Arrangement (Two-Tier Layout)**
  * **Goal**: Implement the two-tier stacked layout for the career filmography toolbar based on user mockup.
  * **Layout**:
    * **Top Row**: Circular avatar + gold kicker (`ACTING · COMPLETE FILMOGRAPHY`) + bold name (`Daniel Kaluuya`) on single horizontal lines with zero text-wrapping.
    * **Bottom Row**: Full horizontal width for department filter tabs (`All (38)`, `Directed (1)`, `Acted (37)`).
  * **Badge Cutoff Fix**: Fixed status badges on filmography posters and mobile cards getting truncated (`max-width: calc(100% - 8px)`).

- [x] **Grey Situational Awareness & Live Grid Vision**
  * **Goal**: Provide Grey with full real-time awareness of the screen, active person filmography, and visible movies.
  * **Accurate Screen State**:
    * When viewing Filmography: passes `current_view: "filmography"`, person name, department, and total count.
    * When viewing Movie Notes with a paired shelf: passes `current_view: "movie-notes"`, `notes_shelf_filter: "watched"`.
  * **Live Grid Vision**:
    * Sends a compact summary of the top 20 movies currently rendered on the user's screen (titles, years, personal shelf statuses).
    * Allows Grey to answer questions directly referencing visible titles on screen.

- [ ] **Personal Library Export, Backup & Google Sheets Sync**
  * **Placement**: Located on the **Storage** page (`Local data → Storage`).
  * **Offline Backup (JSON / CSV)**: 1-click download of all user data as timestamped JSON (full fidelity) or CSV.
  * **Google Sheets Webhook Sync (Optional Cloud)**: Connect a Google Apps Script Web App URL to push personal library snapshots directly into a private Google Sheet for mobile access and sharing, without Google Cloud Console overhead.

---

## ✅ Completed Tasks

- [x] **Modular Skill-Based Prompt Architecture for Grey**
  * **Goal**: Decompose Grey's monolithic 224-line prompt into a lean core persona and dedicated on-demand skill modules, preventing instruction conflicts, context dilution, and token bloat.
  * **Architecture**:
    * **Core Persona ([`grey_core.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/grey_core.md))**: Houses Grey's cinephile voice, craft philosophy, behavioral rules, and JSON action output envelope (~75 lines).
    * **Dynamic Skill Modules ([`app/prompts/skills/`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/))**:
      - [`notes_editor.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/notes_editor.md): Format mimicry, in-place upsert, `>>` Notion toggles with double blank line exit, zero redundancy.
      - [`related_curator.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/related_curator.md): Script craft, pacing, tension, YES/NOPE verdicts on related movies.
      - [`filmography_explorer.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/filmography_explorer.md): Career context, department filter awareness (acting vs directing).
      - [`watchlist_builder.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/watchlist_builder.md): 8-12 tranche synthesis, Notion toggles with Cast/Synopsis/Why YES.
      - [`library_ops.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/library_ops.md): Shelf moves, ratings, verdicts, batch actions, and library awareness.
    * **Dynamic Context Router ([`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py))**: Inspects current view, open note, active person, or slash command to dynamically inject only the active skill directive into `{{ACTIVE_SKILL_DIRECTIVE}}`.
    * **Unit Tests ([`test_grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_grey_service.py))**: Added tests verifying that screen states route exclusively to their intended skill module without loading unrelated instructions.
 (Reference Only — Do Not Modify or Re-implement)

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

### V. Tiered Search Relevance Hierarchy & Multi-Word Tag Autocomplete (done — Oct 20)
* **Tiered Search Relevance Hierarchy**: Replaced flat alphabetical search sorting with an intelligent relevance ranking hierarchy:
  1. **Exact Title Match** (Tier 1, top priority)
  2. **Title Starts With Query** (Tier 2)
  3. **Title Contains Query** (Tier 3)
  4. **Original Title Match** (Tier 4)
  5. **Personal Memory Notes Match** (Tier 5)
  6. **Overview / Plot Premise Match** (Tier 6)
  Ensures that exact or direct title searches never get buried underneath dozens of movies that merely mention the word in their overview blurb.
* **Multi-Word Tag Autocomplete**: Tag input now respects multi-word concepts (e.g. *"movie philosophy"*, *"site links"*), splitting strictly on commas rather than spaces, with an interactive suggestions dropdown and badge counts.

### W. Notion Toggle Clean Breakouts & Note Navigation (done — Oct 20)
* **Empty Line Toggle Exit**: Pressing Enter on an empty line within a Notion toggle block cleanly escapes the toggle and returns cursor to normal top-level body text.
* **Modal Navigation Fixes**: Resolved note chip interactions from the single movie inspection modal so personal notes open reliably in the reader.

### X. Single 1-Click Launcher (`run.bat`) & Grey Opinion Title Anchor (done — Oct 21)
* **Consolidated Launcher**: Merged `run_app.bat` into `run.bat`. A single double-click launches the Uvicorn server and automatically opens the browser to `http://127.0.0.1:8000` while preserving CLI subcommands (`test`, `init`, `install`).
* **Grey Opinion Header Anchor**: Injected Rule 0 into Grey's system prompt enforcing bold **Movie Title (Year)** on line 1 for any movie opinion, critique, or verdict.

### Y. Journal Reader Rich Markdown, Cinematic Banner Headers & Keyword-Driven Discovery (done — Oct 21)
* **Full Markdown Styling in Journal Reader**: Expanded `formatRichText` and `appendEntryBody` to support bold (`**strong**`), italics (`*film title*`), section headings (`## Heading 2`, `### Heading 3`), blockquotes (`> quote`), and inline tags/code (`` `keyword` ``).
* **Cinematic Banner Images for Journal Entries**: Added optional backdrop / banner image support (`image_url`) for journal articles and film essays, rendering a hero header at the top of the entry reader.
* **Keyword-Driven Discovery Filter Generator**: Enabled generating intelligent TMDB discovery filters from selected journal articles, themes, or keyword clusters.

### Z. Prune Redundant Skill Chips (`/nope` and `/tonight`) (done — Oct 21)
* **Decluttered Interface**: Removed `🎬 /tonight` and `🚫 /nope` from Grey's quick-action pill tray and slash autocomplete menu.
* **Streamlined Skill Registry**: Focused Grey's quick action bar exclusively on high-leverage tools (`⚡ /related` for reality checks and `📝 /watchlist` for rich toggle notes).

### AA. `/watchlist` Skill Overhaul & Zero Shelf/Note Confusion (done — Oct 21)
* **Exact Post Title Resolution & Smart Appending**: When saying *"add this to my [Post Title] post"* (e.g. *"Watchlist 1"*, *"Watchlist 2"*, *"Spoof Movies"*), Grey accurately resolves the targeted post by title (ranking specific multi-word titles first) and appends the new movie toggle (`>> Title (Year)`) directly to that note's body, preserving existing contents.
* **Substantial Depth & Coverage**: Eliminated lazy 3-movie cutoff. When drafting a watchlist note from the queue, Grey curates a comprehensive tranche (8–12 titles) with clean Notion-style `>> Title (Year)` toggles, cast, synopsis hook, and cinephile reasons.
* **Zero Shelf/Note Confusion Guardrail**: Added strict prompt rule and backend interception: if the prompt mentions *"post"*, *"note"*, *"journal"*, or *"entry"*, `set_movie_status` is strictly forbidden and automatically redirected to `update_entry`.

### AB. Offline Mode Resilience & Local Poster Cache Pipeline (done — Oct 21)
* **Graceful Single Movie Page Offline Fallback**: When viewing movies while offline (from saved filters or shelves), deep TMDB metadata fetch failures are caught gracefully. The modal renders the lightweight cached data (title, year, overview, rating, genres) with a subtle gold `Offline Preview` pill. Core user actions (Watch Later, Watched, Nope, Rewatch, personal notes) remain 100% functional offline in local SQLite.
* **Frontend Memory Fallback**: If the network is entirely offline, `openMovieDetails` catches fetch errors and renders an immediate offline preview from in-memory collection cache (`state.movies` / `state.allFilteredMovies`).
* **Local Poster Caching Pipeline**: Created `PosterCacheService` storing downloaded posters locally on disk in `data/posters/`. Automatically queues posters in the background whenever shelves or saved filters are browsed.
* **Local Poster Proxy Route & CDN Fallback**: Added `/images/posters/{file_path}` serving cached poster images from disk with immutable caching headers. Equipped `createPoster` with a smart two-stage loader (fast direct TMDB CDN when online, local disk fallback when offline) to eliminate initial letter-box fallbacks.
* **Storage Optimization Invariant Enforced**: Movies marked as excluded (`NOPE`) are strictly prevented from caching posters, and any existing poster file is immediately purged on rejection.

### AC. Grey Docked Mode Layout & Scroll Isolation Fix (done — Oct 21)
* **Root Cause Resolved**: Fixed layout clipping where opening the Grey companion alongside a movie detail page pushed the header/title off-screen and left a black void at the bottom.
* **Viewport Pinning**: Fixed `.movie-detail-page` to `position: fixed; top: 0; left: 0; bottom: 0;` when Grey is docked, guaranteeing immune alignment regardless of window scroll offsets.
* **Seamless Scroll Transfer**: Synchronized window scroll offsets into the internal detail scrollbar upon drawer toggle and back to the window upon closing.
* **Focus Scroll Protection**: Guarded all Grey input `.focus()` calls with `{ preventScroll: true }` to prevent browser auto-scroll shifts.

### AD. Related Movies: 20-Title Expansion, Status Badges by Default & Vote-Count Tooltips (done — Oct 21)
* **20-Movie Full Tranche**: Expanded recommendation limit from 12 to 20 to fetch TMDb's complete recommendation page.
* **Compact Mini-Poster Geometry**: Reduced card size to ~82px–92px (5–6 per row) so 20 recommendations fit in a tight, elegant 3–4 row grid without vertical sprawl. Excluded titles are subtly dimmed (`opacity: 0.52`).
* **Show Tracked Titles by Default**: All related titles display their library badges (**Watched**, **Nope**, **Watch Later**, **Rewatch**) upfront. The toggle now acts as an opt-in filter (*"Hide tracked movies (N)"* / *"Show N tracked movies"*).
* **Vote-Count Reality Check Tooltips**: Upgraded hover tooltips to show Title, Year, and Vote Count sample size (e.g. `Dark Star (1974) • (24.3k votes)` + private note snippet if present) with no redundant rating.

### AE. Library Search Overhaul: Word Boundaries, 5-Tier Relevance Ranking & Prefix Syntax (done — Oct 22)
* **Word-Boundary & Acronym Normalization**: Replaced raw substring matching (`LIKE '%ai%'` / `.includes("ai")`) with regex word-boundary token matching (`(?<![a-z0-9])...(?![a-z0-9])`) and acronym dot normalization (`A.I.` → `AI`). Searching `ai` now matches only standalone AI movies and tags without false-positive matches on words like `straight`, `against`, or `aircraft`.
* **5-Tier Relevance Ranking**: Both backend (`search_user_library`) and frontend (`applyLibraryFilters`) rank search results in strict priority order:
  1. **Tier 1**: Exact title match
  2. **Tier 2**: Title contains word/phrase (starts-with prioritized first)
  3. **Tier 3**: Word found in TMDB plot blurb
  4. **Tier 4**: Word found in personal movie notes
  5. **Tier 5**: TMDB keyword tag match
* **Exact Field Prefixes**: Added `title:`, `plot:`, and `notes:` prefix support in the sidebar search bar for targeted field searches.

### AF. Movie Notes UX: Unified Sidebar Search, Shelf Double-Select Lens & Instant Hover Preview (done — Oct 22)
* **Removed Redundant In-Page Search Bar**: Removed `#notes-search-container` from the Movie Notes canvas so all searching and `notes:` queries happen cleanly from the unified left sidebar.
* **Movie Notes + Shelf Double-Select Lens (Option 1)**: Clicking **Movie Notes** activates the notes lens; clicking any shelf button (*Watched*, *Nope*, *Favourites*, *Watch Later*, *Rewatch*, *New Discovery*) highlights both buttons and filters strictly to notes on that shelf. Clicking the active shelf again clears the shelf filter; clicking **Movie Notes** again exits the lens back to the full shelf.
* **Instant Poster Hover Preview Card**: Hovering over any poster with a personal note triggers a snappy (150ms) dark glassmorphism popover card (`#poster-note-popover`) displaying the gold `📝 Note` badge, title/year, and formatted note text without opening the modal.

---

*Last Updated: October 22, 2026*
