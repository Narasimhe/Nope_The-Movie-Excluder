> **AI INSTRUCTION**: Only read and process items listed under **🟢 Pending Tasks (Active Focus)**. Treat **✅ Completed Tasks** as historical archive data only—do not re-implement, modify, or discuss them unless explicitly requested by the user.

# Project Improvements & Backlog

## 🟢 Pending Tasks (Active Focus)

- [ ] **Storage Telemetry Labels**
  * **Storage Page "Personal Library" Label Cutoff**: Fix card width, padding, or label sizing on the Footer > Storage page so the *"Personal Library"* metric labels and sublabels never clip or truncate.

- [ ] **Grey Intelligence, Contextual Help & Google Sheets Export**
  * **Strip Redundant Movie Header Metadata from Grey's Movie Notes**: When Grey writes or updates a personal movie note (`set_movie_status` / movie note field), ensure it never prepends redundant Movie Title, Release Year, or Genre headers inside the note body—keep only the actual note/reflection.
  * **Screen-Relevant Help Docs in Grey**: Give Grey access to a concise internal UI/formatting help guide (especially when on the Notes editor screen) so questions like *"Hey Grey, how do I use formatted titles in notes?"* return the exact syntax and examples from the app docs.
  * **Export Library / NOPE Database to Google Sheets**: Add an export workflow from the SQLite database (Personal Library / NOPE shelves) into a structured Google Sheet.

- [ ] **Dedicated API & Network Telemetry Space (Footer / System View)**
  * **Goal**: Provide a clean, dedicated space (similar to the Storage page, accessible via footer or system navigation) that visualizes outbound TMDB API consumption, cache efficiency, and network health without cluttering the main footer or UI.
  * **Key Components**:
    * **Outbound TMDB Metering**: Track total requests made during the session and across historical runs (today/cumulative).
    * **Cache Savings Ratio**: Quantify bandwidth and network savings achieved by local SQLite caching (e.g. `X live requests vs. Y queries served from local cache`).
    * **Rate Limit & Health Telemetry**: Display circuit-breaker status, response latencies, and TMDB throttle/health state.
    * **Dedicated Zen Surface**: Kept cleanly out of the primary footer surface into its own harmonious memory page/modal.

- [ ] **Pluggable Critic Personalities & Roger Ebert Lens for Grey**
  * **Goal**: Replace rigid, repetitive buzzword lexicons with deep, authentic critical perspectives. Allow Grey to channel legendary film critics—starting with Roger Ebert—to provide nuanced, humane, and varied critiques.
  * **Key Components**:
    * **Personality Profile Architecture (`app/grey/personalities/`)**: Dedicated markdown/config profiles defining voice, critical philosophy, and review guidelines (starting with `ebert.md`).
    * **Dual-Era Ebert Intelligence**:
      * *Pre-2013 films*: Gemini surfaces his actual historical reviews, four-star ratings, and memorable quotes or pans.
      * *Post-2013 films*: Gemini channels his distinctive humanistic philosophy (*"A movie is not about what it is about, but how it is about it"*) to evaluate modern films through his eyes.
    * **Activation & Interaction**: Support natural conversational triggers (e.g. *"What would Ebert say?"*, `/ebert`), contextual suggestion pills on the movie detail page, or a discreet critic lens selector in the Grey drawer.

---

## ✅ Completed Tasks
- [x] **Restored All Blog / Journal Banners & Storage Test Sandbox Isolation (`app/storage_repository.py`)**
  * **Root Cause & Prevention**: Fixed a bug where `StorageRepository.purge_deleted_entries()` hardcoded `banners_dir` to production `data/banners`. When running unit tests with a temporary in-memory/isolated SQLite database containing no banner entries, orphaned cleanup was deleting production banner image files. Fixed `banners_dir` to derive dynamically from `Path(database.DATABASE_PATH).parent / "banners"`, fully isolating test databases.
  * **Full Banner Recovery**: Recovered all 20 historical user banner images (`f0e73afcd2434919.png`, `05cc6b66e77d4396.png`, `af8bb366267b4305.png`, `fa28b3d3dfed407a.jpg`, `c94489fd02d5466d.png`, etc.) directly from Git commit history into `data/banners/`.
- [x] **Back-to-Top Floating Scroll Button Spacing in Grey Mode (`app/static/styles.css`, `app/web/index.html`)**
  * **Breathing Space from Grey Chat Drawer**: Shifted `.back-to-top-pill` position when Grey is docked open from `calc(420px + 24px)` to `calc(420px + 40px)`, shifting the button 16px to the left to give comfortable breathing room away from the Grey chat box border.
- [x] **Actor & Director Filmography Zen Restyle (`app/static/styles.css`, `app/web/index.html`)**
  * **Stripped Excessive Weight & Chunky Styling**: Replaced heavy font weights (`850` name, `800` kicker, `750` return button, `700` tabs) with refined, calm Zen weights (`650` title, `550` kicker, `500` return button and tabs).
  * **Streamlined Header & Palette**: Eliminated the bulky, opaque dark box container and loud canary yellow borders. Replaced with an open, airy horizontal layout featuring subtle hairline borders (`rgba(255, 255, 255, 0.06)`), a compact 48px avatar with refined champagne border, warm champagne kicker (`#DEC68B`), and a compact segmented pill tab group (`height: 28px; width: fit-content`).
  * **Zen Pill Return Button**: Converted `.return-to-origin` into a compact, 30px hairline pill button with subtle warm hover interaction.
- [x] **Poster Hover Preview Card Year & Metadata Alignment (`app/static/app.js`, `app/static/styles.css`, `app/web/index.html`)**
  * **Bare Release Year**: Stripped parentheses from the release year in `.poster-note-popover` so it sits bare right after the title with a clean single space gap (e.g. `Inception 2010`).
  * **Unified Metadata Placement & Proximity**: Switched `.poster-note-popover-header` alignment from `space-between` to `flex-start` with a consistent `16px` gap, ensuring rating and vote count metadata sit directly next to the title/year across both title-only previews and previews with personal notes.
- [x] **Sidebar Library Status Placement & Preset Decoupling (`app/web/index.html`, `app/static/app.js`)**
  * **Sidebar Hierarchy Repositioning**: Moved *Library Status* directly beneath *Sort Results* at the top of the Discover sidebar accordion, keeping both global presentation/lens controls grouped together before movie criteria filters.
  * **Full Decoupling of Library Status from Presets (Option 1)**: Removed personal library status from preset divergence checks and preset application (`applySelectedProfile`), ensuring search presets focus purely on TMDB discovery criteria without overwriting or dirtying active personal library status toggles.
- [x] **Search Preset Divergence & Instant Chip Feedback Refinement (`app/static/app.js`, `app/web/index.html`)**
  * **Minimum Vote Count Key Parity**: Fixed key mismatch in `isProfileFiltersDiverged` where the filter key was checked as `vote_count_minimum` instead of `minimum_vote_count`, ensuring changes to the minimum votes input immediately trigger the preset divergence check and update icon. Also added coverage for `maximum_rating`, `runtime_min`, `runtime_max`, `include_actor_ids`, and company/keyword exclusion keys.
  * **Update Icon Scoped Exclusively to Ribbon Presets**: Removed the update icon button from the Search Profiles accordion workshop chips so the update icon appears exclusively on the top ribbon presets as requested.
  * **Sort Order Excluded from Preset Divergence**: Removed `sort_by` from `isProfileFiltersDiverged` so modifying result ordering (e.g. Highest rated, Most popular, Newest) is treated strictly as view presentation and never marks a preset as modified or triggers the update icon.
  * **Instant Chip Feedback**: Wired genre chips, language/country pickers, keywords, and entity tags (cast, directors) directly into `syncRibbonActiveState()` and `renderProfileWorkshop()` so toggling or removing any filter chip immediately surfaces or clears the preset update icon in real time without needing a form event or search submission.
- [x] **Reader & Blog Notes Typography Scale Refinement (`app/static/styles.css`, `app/web/index.html`)**
  * **Balanced Editorial Font Sizing**: Scaled down body text and headings in `.entry-reader` and `.reader-body-textarea` to harmonize with the compact Zen UI aesthetic.
  * **Body & Textarea**: Scaled from `1.06rem` (~17px) / `1.76` line-height down to `0.94rem` (~15px) / `1.62` line-height (and `0.90rem` / `1.58` in docked Grey mode) with paragraph margins reduced from `1.25rem` to `1.05rem`.
  * **Note Titles**: Scaled down note title input and display from `clamp(2rem, 4vw, 2.55rem)` down to `clamp(1.5rem, 2.8vw, 1.75rem)` in full view (and `clamp(1.35rem, 2.2vw, 1.55rem)` in Grey docked mode) with tightened margins (`margin-bottom: 0.75rem`).
  * **Section Headings**: Scaled `h2` down from `1.6rem` to `1.22rem` (margin: `1.6rem 0 0.65rem`) and `h3` down from `1.28rem` to `1.05rem` (margin: `1.3rem 0 0.55rem`) for cohesive visual hierarchy.
- [x] **Notes UI Restyle, Editor Status & Movie Hover Card Polish (`app/static/styles.css`, `app/static/app.js`, `app/web/index.html`)**
  * **Movie Grid Creeping into Notes Fix (Grey Mode)**: Resolved an issue where library posters bled into the top of the Notes workspace when Grey was docked open. The root cause was that Grey mode grid overrides checked `:not(.is-hidden)` while auxiliary views only set `.force-hidden` and left the `#movie-grid-viewport` untoggled. Unified both classes on grid and viewport, guarded with `:not(.force-hidden)`, and established a CSS firewall ensuring the movie grid and viewport are never rendered whenever `#entries-page` or `#entry-reader` is active.
  * **Notes Toolbar Zen Dimensions & Palette Alignment**: Compacted the toolbar from chunky 44px blocks down to a refined 32px height matching the Library/Discover toolbars. Replaced the loud solid canary yellow `+ New note` button with a subtle, warm champagne-accented Zen pill (`rgba(222, 198, 139, 0.10)`), toned down the List/Cards switcher active state to soft champagne (`#DEC68B`), eliminated the yellow neon box shadow, and aligned search input padding, typography, and focus ring with the Zen aesthetic.
  * **Grey Docked Mode Note Toolbar Visibility Fix**: Corrected selector over-matching (`body.grey-docked-open .entry-reader-toolbar:not(.is-hidden)`) that was inadvertently forcing both the reading view toolbar and editing canvas toolbar to render simultaneously in Grey mode. Explicitly scoped `display: none !important` and `display: flex !important` based on `.is-editing` state.
  * **Clean Segmented Switcher & Subpixel Antialiasing**: Eliminated the concentric double-box border by setting the active switcher button border to transparent within its outer container, removed the colliding vertical separator line, and enforced grayscale font antialiasing (`-webkit-font-smoothing: antialiased`, `-moz-osx-font-smoothing: grayscale`) across the body and UI buttons to completely eliminate Windows ClearType chromatic (red/cyan) text fringing.
  * **Unified Tag Chip Shape (List Mode & Single Note Mode Parity)**: Aligned single note reader/editor tag chips (`.reader-tag-chip`, `.entry-reader-tags .entry-tag`, and `.reader-tag-input`) from squarish `border-radius: 6px` to the exact rounded `999px` pill style and muted champagne border used in list mode.
  * **List Mode Row Actions Proximity**: Removed `margin-left: auto` from `.ledger-right`, docking the pin, archive, and delete action buttons directly adjacent to the note title and tag pills with a comfortable 12px gap instead of stranding them at the far right edge of the monitor.
  * **Calm Editorial Hierarchy in List Mode**: Toned down overly bright/thick note titles (`font-weight: 500; color: #d8d5cf;`), highlighting warmly on hover and maintaining clear balance on pinned rows.
  * **Soft Champagne Zen Active State & Outline Drafts Icon**: Softened `.notes-tag-link.is-active` from saturated yellow to warm champagne-gold (`#DEC68B` / `rgba(222, 198, 139, 0.10)`), and replaced the solid emoji with a clean outline SVG icon for Drafts, All Notes, and Archive in the sidebar.
  * **Direct Note Title & Tag Proximity**: Positioned category/tag pills directly inside `.ledger-title-wrap` immediately adjacent to note titles with a comfortable 9px gap, preventing tags from floating far to the right on wide displays while keeping row actions cleanly docked on the far right.
  * **Timeline Month Note Count Proximity**: Repositioned `(n notes)` directly following `YYYY · MONTH` with a clean spacing gap, allowing the decorative horizontal rule to span the remainder of the row instead of pushing the count to the far right edge.
  * **Single Movie Detail Vote Icon Parity**: Replaced the Material icon on the movie detail page with the exact yellow SVG vote icon (`stroke: #F2C94C`, stroke-width: 2.2) used in the hover preview card.
  * **Muted Stone/Champagne Save Indicators**: Replaced neon green indicators in the notes editor and movie detail notes with warm muted stone/champagne typography (`#d1cdb8`), removing visual clutter while preserving reassuring status clarity.
  * **Movie Hover Card Layout & Metadata Styling**: Release year now matches the exact font weight of the movie title (`550`); preserved generous 14px header spacing; formatted metadata with crisp yellow SVG icons and bold white numbers for both ratings (`[Star Icon] Rating`) and votes (`[Vote Icon] Vote Count`).
- [x] **Detail View Header Edge Alignment & Related Movies Baseline & Poster Locking (`app/static/styles.css`, `app/static/app.js`, `app/web/index.html`)**
  * **Back to Discover Left Edge Alignment**: Removed legacy overriding header padding/margins from lines 6379-6461 so `← Back to Discover` and the main poster left edge align at the exact same pixel offset across both non-Grey and Grey docked modes.
  * **Metadata Card & Stepper/Sync Right Edge Alignment**: Synchronized `.detail-header-inner` and `.detail-hero` width to `min(970px, 100%)` so the navigation stepper and sync button (`[ ‹ Prev | Next › ] [ ↻ Sync ]`) align with the right edge of the movie metadata card.
  * **Related Movies Baseline & Last Poster Lock**: Cleared legacy `margin-bottom: 1rem` from `#related-familiar-toggle` to align it on the exact vertical baseline of `Related Movies`. Added `alignRelatedHeading()` in `app.js` to dynamically lock the right boundary of the heading to the right edge of the last poster in the top row across all screen sizes and Grey mode toggles.
  * **Fixed Ghost Circle When Zero Tracked Movies**: Scoped toggle display to `:not(.is-hidden)` and reinforced `#related-familiar-toggle.is-hidden { display: none !important; }` so movies with zero tracked related titles remain hidden without rendering an empty circular border.
- [x] **Grey Docked Mode Responsive Layout & Overflow Polish (`app/static/styles.css`, `app/web/index.html`)**
  * **Strict Visibility Guard**: Added `.movie-grid-viewport.is-hidden` and `body.grey-docked-open .movie-grid-viewport.is-hidden` to prevent the poster grid from ever rendering inside the Notes workspace in Grey mode.
  * **Sidebar Sort Results Constraint**: Updated `.sort-chip-cloud` to `grid-template-columns: repeat(2, minmax(0, 1fr))` with `box-sizing: border-box` and `.sort-chip` text truncation (`min-width: 0`, `text-overflow: ellipsis`) so sort buttons never overflow past the sidebar container border.
  * **Center Header & Shelf Ribbon Clipping**: Replaced rigid `overflow: hidden` on `.library-shelf-ribbon` with clean `overflow-x: auto` (hidden scrollbars) and allowed `.discover-toolbar-row` / `.library-toolbar-row` to flex and wrap gracefully in docked Grey mode so the `Nope` shelf button and movie count are never clipped.
  * **Single Movie Page Responsiveness & Aligned Header**: Repaired malformed comma before `@media` rule in `.cockpit-shelf-pill`, enabled `flex-wrap: wrap` on `.cockpit-shelf-row`, and aligned header padding (`padding: 0 24px`) with content in Grey mode so the `Nope` cockpit button and `[ ‹ Prev | Next › ] [ ↻ Sync ]` controls maintain exact spacing and never overflow.
- [x] **Top-Right Main Poster Status Badge, High-Contrast Thickened Badges & Notes Keyboard Escape (`app/static/styles.css`, `app/static/app.js`, `app/web/index.html`)**
  * **Top-Right Main Poster Badge**: Repositioned `.detail-poster-status-badge` from top-left (`left: 12px`) to top-right (`top: 10px; right: 10px; left: auto;`), placing it immediately adjacent to the film title and overview column.
  * **Thickened High-Contrast Poster Badges**: Enhanced status glyphs across main, discover, and related movie poster cards with `font-weight: 800` and filled circular backplates (`background: rgba(15, 15, 18, 0.85); border: 1px solid rgba(255, 255, 255, 0.2);`), ensuring high visibility across dark and light movie artwork alike.
  * **Escape Key Unfocus from Notes**: Added an `Escape` keydown handler on the personal movie notes textarea that flushes any pending debounced save, blurs the textarea, and returns focus to the detail page container, allowing effortless subsequent `←` / `→` arrow key navigation between movies.
- [x] **Direct Single-Movie TMDB Sync, Prev/Next Preservation & 24px Header Lift (`app/main.py`, `app/movie_service.py`, `app/static/app.js`, `app/static/styles.css`, `app/web/index.html`)**
  * **Header A [ ‹ Prev | Next › ] [ ↻ Sync ] Order & Spacing**: Placed `[ ‹ Prev | Next › ]` and `[ ↻ Sync ]` in exact requested order in the detail header with a clean 28px gap, using the Discover sync icon and 12px keyword typography that turns brand champagne gold while spinning.
  * **Direct TMDB Force-Sync**: Connected `GET /movies/{tmdb_id}?force_refresh=true` to freshly fetch, cache in SQLite, and update credits, directors, cast, and metadata on screen in-place.
  * **Fixed Stepper Disappearing on Refresh**: Persisted navigation queue IDs in `sessionStorage` and restored them on boot/shelf loads so `‹ Prev | Next ›` remains active and visible on single movie refreshes.
  * **24px Viewport Lift**: Reduced header height to 54px and content padding-top to 10px, lifting the single movie page content by 24px without altering Prev/Next positioning.
- [x] **Eliminate Initial View Flash on Page Refresh Across All Screens (`app/static/app.js`, `app/static/styles.css`, `app/web/index.html`)**
  * **Head Pre-Resolution Script**: Added an early synchronous snippet in `<head>` that immediately attaches `html.is-route-movie` if `#movie:<id>` is detected, instantly suppressing `#app-shell` and showing `#movie-detail-page` with zero frame flashing.
  * **HTML Hardcoded State Cleared**: Removed `data-active-view="discover"` from `<body>` and marked `#discover-canvas-header` with `is-hidden` by default so discovery headers never flash when booting directly into Library or Notes.
  * **Eager Route Handshake & Non-Blocking Shelf Loading**: In `initializeApp()`, immediately invoked `openMovieDetails(id)` without blocking on background shelf API calls; background shelf hydration runs silently in parallel so the Single Movie page appears without delay.
- [x] **Direct Numbered Page Links & Jump-to-Page in Zen Pagination (`app/static/app.js`, `app/static/styles.css`, `app/web/index.html`)**
  * **Interactive Numbered Folio Sequence**: Replaced the static center `1 / 149` counter with a responsive, clickable numbered sequence (e.g. `1  2  3  4  5 … 149` or `1 … 14  15  16 … 149`) that jumps directly to any clicked page.
  * **Zen Minimalist Typography**: Maintained seamless alignment between `< Prev` and `Next >`. Styled the active page in soft champagne gold (`#DEC68B`, font-weight 600) without heavy box borders or buttons, with muted gray links for inactive pages and subtle hover transitions.
  * **Smart Jump-to-Page Input Preserved**: Kept inline jump input on clicking the active page number or ellipsis (`…`), allowing direct keyboard entry and Enter-to-jump.
- [x] **Zero-Plot-Synopsis Movie Context, `gemini-3-flash-preview` Promotion & 429 Cooldown Cache (`app/grey/service.py`, `app/config.py`, `app/grey/prompts/grey_core.md`)**
  * **Zero Plot Synopsis + Director & Cast in `{{INSPECTED_INFO}}` (`_resolve_screen_and_mentioned_context()` in `app/grey/service.py`)**: Removed `Overview: ...` completely from `{{INSPECTED_INFO}}` and replaced it with **Director + Top 4 Cast** queried from local SQLite (`movie_credits`), preventing Grey from ever regurgitating the plot premise on screen.
  * **Promoted Full `gemini-3-flash-preview` & Added 5-Minute `429` Cooldown Cache (`app/config.py` & `_call_gemini_cascade()`)**: Promoted `gemini-3-flash-preview` (full Flash model with active Free Tier quota) to #1 in `GEMINI_FLASH_CANDIDATE_MODELS` and added `_model_cooldowns` in `GreyService` so models returning `429`/`404` are skipped for 5 minutes—eliminating 3 wasted `429` roundtrips per turn and upgrading Grey from `flash-lite` to full `gemini-3-flash-preview`.
  * **Observant Film-Lover Review Framing (`grey_core.md` & `related_curator.md`)**: Shifted Grey from binary verdict posturing to grounded synthesis of what actually works or fails on screen—highlighting standout performances (*"De Niro nailed this"*), pacing, atmosphere, and act-by-act strengths/flaws while reserving the "CGI/AI slop" hammer for genuine slop.
  * **Discarded Approaches (Do NOT Implement)**:
    * *Custom Python scraping of Letterboxd / TMDB `/reviews` into prompt strings* — discarded as impractical, brittle, and the wrong way to use AI.
    * *`tools: [{"google_search": {}}]` on Free Tier API Key* — verified that Google's Free Tier locks `google_search` grounding quota to `0` (`429 RESOURCE_EXHAUSTED` across all models unless a paid billing plan is attached).
- [x] **Soul vs. Soulless Cinema Rubric, CGI/AI Slop Diagnosis & Blunt Human Vocabulary (`app/grey/prompts/grey_core.md`, `app/grey/prompts/skills/related_curator.md`, `app/grey/service.py`)**
  * **Synthesized 7-Axis "Soul vs. Soulless" Rubric (The Ten-Minute Rule)**: Replaced the generic rubric in `grey_core.md` with the user's 7-axis framework (*Observed Humans vs. Director Ego-Extensions*, *Lived History in Behaviour vs. Expositional Slop*, *Genuine Exploration vs. Predetermined Thesis*, *Trusting the Audience vs. Reaction Engineering*, *Long-Term Conviction vs. Cash Grabs*, *Singular Voice vs. Committee AI Slop*, and *Tactile Craft vs. Weightless CGI Slop*).
  * **Explicit CGI Slop & AI Slop Diagnosis in `YES / NOPE` Verdicts**: Updated `related_curator.md` and `grey_core.md` so every `YES` or `NOPE` verdict diagnoses whether a film has real life and conviction or is weightless CGI spectacle/synthetic slop.
  * **Blunt Human Vocabulary & `BLOCK_NONE` Safety Thresholds**: Authorized unfiltered human language in `grey_core.md` and added `BLOCK_NONE` safety settings to `chat()` in `app/grey/service.py` so Gemini never self-censors blunt roasts.
- [x] **Grey Service Phase 2 Micro-Optimizations & Skill Hygiene (`app/grey/service.py` & `app/grey/prompts/skills/`)**
  * **Zero-SQL Mention Resolution (`_resolve_screen_and_mentioned_context()` in `app/grey/service.py`)**: Removed the dead `relevant_journal_excerpt` SQL query (`LIMIT 15`) and replaced the per-turn `LIMIT 200` movies scan and `LIMIT 50` `general_entries` body scan with fast in-memory matching against `_dossier_cache` (`tracked_movies_index` and `all_active_notes`), querying SQLite for the single row only when a title actually matches.
  * **Persistent HTTP Connection Pooling (`_call_gemini_cascade()` in `app/grey/service.py`)**: Routed Gemini API calls through `self.http_session.post` (while preserving unit test compatibility when `requests.post` is monkeypatched) to eliminate repeated DNS + TCP/TLS handshakes (~150–250ms saved per call).
  * **Removed Orphaned `watchlist_builder.md` & Dead `{{WATCHLIST_JSON}}` Serialization**: Deleted `app/grey/prompts/skills/watchlist_builder.md` and removed redundant `{{WATCHLIST_JSON}}` replacement in `chat()`.
  * **Documented `apply_filter` Parameter Schema (`app/grey/prompts/skills/library_ops.md`)**: Specified the exact filter keys expected by `handleGreyFilterAction` in `app/static/app.js` (`genres`, `languages`, `min_year`, `max_year`) so Grey can reliably filter the grid on command.
  * **Bounded Conversation History Window (`chat()` in `app/grey/service.py`)**: Kept the most recent 4 history turns intact while capping older turns in `history[-16:]` to ~600 characters so earlier 30-movie lists or tables don't re-bloat token payloads on subsequent turns.
- [x] **Grey Service Intelligence & Architecture Overhaul (`app/grey/service.py` & `app/grey/note_formatter.py`)**
  * **Eradicated Per-Turn Megaprompt Bloat & 17-Query SQLite Loop**: Consolidated `get_taste_dossier()` from 17 sequential SQL queries (including an 8-query `N+1` tag loop) into 2 fast consolidated queries backed by signature-verified RAM caching (`_dossier_cache`), and replaced the 15,000-character research file dump on normal turns with a 1-line filenames summary (`get_research_files_summary()`).
  * **Hybrid 1-Line RAM Title Map + On-Demand Gemini Tool Fetching (`_execute_tool_call()`)**: Replaced the 50-object JSON note dump with a compact `ID="Title"` map and implemented native on-demand tool execution (`get_shelf_movies`, `get_note`, `search_library_movie`, `read_research_file`) so Gemini can resolve synonyms and fetch shelves, notes, or research files in ~1ms when a query reaches outside the current screen.
  * **Eliminated False-Positive Movie, Note & Model Hijacking**: Replaced the naive 4-letter substring movie matcher (`len(w) >= 4`) with strict word-boundary title matching (`_resolve_screen_and_mentioned_context()`), prevented background `get_related_movies()` calls unless a movie is open in the UI, removed generic single-word Pro triggers (`"rating"`, `"review"`), and restricted `set_movie_status` $\rightarrow$ `update_entry` interception strictly to explicit post/note target phrasing.
  * **Zero Hardcoded Python Prompts & Mtime-Aware RAM Cache**: Removed all hardcoded `"directive"` strings from `SKILLS_REGISTRY` and inline fallback prompts, preloaded `grey_core.md`, skill `.md` files, and `reactions.json` into memory (`_read_cached_file()`), and documented `##`/`###` headings, `@Movie Title (YYYY)` pills, `>` blockquotes, and Read vs. Write separation in `notes_editor.md`.
  * **Decomposed `chat()` & Extracted `note_formatter.py`**: Moved the 250-line `_deduplicate_and_format_note_body()` helper into `app/grey/note_formatter.py` and extracted `_handle_create_draft`, `_handle_batch_set_movie_status`, `_handle_set_movie_status`, `_handle_update_entry`, and `_handle_research_file_action` into dedicated private methods with top-level imports.
- [x] **Per-Shelf Notes Lens in Library Ribbon (Status + Notes)**
  * **Eliminated Generic "All Statuses Notes" Bucket**: Transformed the ribbon's `📝` button into a dedicated, status-paired lens (*Shelf + Notes*). It never mixes notes from unrelated statuses into an untamed bucket.
  * **Status-Aware Memory Reading**: Clicking `📝` on **Nope** shows only rejected films with notes (*"Why did I drop this?"*); on **Watched** it shows watched reflections; on **New discovery** or **Rewatch** it filters to those respective notes.
  * **Fluid Shelf Switching**: Clicking between shelves while the `📝` lens is active smoothly transitions to the new shelf's notes (e.g. *Watched Notes* $\rightarrow$ *Nope Notes*) with both the shelf chip and the note icon highlighted.
  * **1-Click Lens Dismissal**: Clicking `📝` again (or clicking the currently paired shelf chip) deactivates the lens and instantly restores the full shelf.
  * **Contextual Empty States & Headings**: Displays tailored headers (e.g. *Nope Notes*, *Watched Notes*) and contextual empty states with a direct 1-click *"View all [Shelf]"* fallback.
- [x] **Rock-Solid Library Sort Chips & Tactile "See Results" Button Polish**
  * **Eliminated Sort Re-Click Snap-Back (Mouse Bounce Protection)**: Replaced fragile toggle-off logic on Library sort chips with idempotent radio selection (`if (chip.classList.contains("is-active")) return;`). Micro-double-clicks, switch bounces, or repeated clicks no longer accidentally flip the selection back to "Recently updated".
  * **Search-Aware Sorting Tiebreaker**: Updated `applyLibraryFilters` so that selecting a sort chip (e.g. "Newest first", "Oldest first", "Title A-Z") orders movies within search relevance tiers instead of hardcoding title sort.
  * **Pointer Event Pass-Through**: Added `pointer-events: none` to all inner elements inside `.sort-chip`, ensuring clicks hit the button directly without text-selection or drag hiccups.
  * **Tactile "See Results" Inner Shade & Refined Ivory Typography**: Applied a rich subtle vertical gradient (`linear-gradient(180deg, rgba(212, 175, 55, 0.22) 0%, rgba(180, 140, 40, 0.12) 100%)`) with an inset top highlight (`inset 0 1px 0 rgba(255, 255, 255, 0.12)`) and warm ivory text (`#F3EFE6`), removing hollow blackness and harsh neon yellow.
- [x] **Butter-Smooth Library Scope Toggling & Flicker-Free Transitions**
  * **Eliminated Skeleton Strobing**: Replaced full-grid DOM destruction and aggressive 10-skeleton card flashing on fast local SQLite searches with an in-place opacity crossfade (`opacity: 0.75 -> 1.0`), keeping existing movie cards stable until results load.
  * **Always-Active Scope Switching**: Clicking `[ This shelf ]` / `[ All shelves ]` now reliably executes the transition at all times (including when the search box is empty), cleanly switching between the current shelf and all personal library movies.
  * **Stable Shelf Counter**: Prevented `setSectionCopy` from wiping the top-right movie count (`elements.shelfCount`) during library searches, eliminating layout jumps.
  * **Width-Stabilized Pill**: Added `min-width: 82px` to `#library-scope-toggle` so switching between "This shelf" (10 chars) and "All shelves" (11 chars) does not cause neighbor pill jitter.
- [x] **Dynamic Search Target Reflection & 1-Click Entity Reset in Library**
  * **Dynamic Entity Reflection**: When a sidebar keyword, actor, or director is filtering the shelf (and the text search box is empty), the target pill dynamically reflects it (e.g., `[ 🏷️ whodunit × ]`, `[ 🎬 Nolan × ]`, `[ 👤 Bale × ]`) with contextual placeholder `Search within theme "<name>"…`.
  * **1-Click Pill Reset / Dismiss**: Clicking the active dynamic entity pill (or its `×`) instantly clears the active keyword / cast & crew filters, restores the shelf view, and resets the target pill back to standard `[ 🌐 All ]` without touching the sidebar.
  * **Smooth Text Fallback**: Typing into or focusing the search input immediately shifts the target button back to the 4-way text target (`All`, `Title`, `Plot`, `Notes`).
- [x] **Instant Reactive Library Filtering with Passive Anchor "See Results" Button**
  * **Zero-Latency Reactive Filtering**: Clicking genre chips, language chips, or typing years now filters your library immediately and reactively in real time (<1ms in-memory filtering), removing the artificial staging barrier.
  * **Visual Layout Anchor (Dummy)**: Kept `#run-library-search` in place as a calm, passive visual companion matching Discover mode pixel-for-pixel, preventing header jumping when switching modes. Clicking it acts as a tidy-up shortcut that collapses any open accordions.
- [x] **Library Cast & Crew Autocomplete Fix (`/movies/library/people`)**
  * **Standardized Payload**: Ensured `/movies/library/people` returns `{ "results": [...] }` (and fortified frontend parser to handle both direct arrays and `{ results }` envelopes), restoring seamless autocomplete search for actors and directors in Library mode.
- [x] **Refined "See Results" Visual Styling & Library Multi-Genre Selection**
  * **Warm Champagne Gold Hue**: Replaced the harsh neon yellow (`#FACC15`) on `.see-results-btn.is-dirty` with our refined brand champagne tone (`#DEC68B` / `rgba(222, 198, 139, 0.42)`).
  * **Visible Inner Shade**: Added a soft, warm background tint (`rgba(222, 198, 139, 0.12)`) and inset highlight, eliminating the hollow/flat dark box appearance.
  * **Library Genre Multi-Select Restored**: Restored independent multi-selection across genre chips in the Library sidebar, allowing users to combine multiple genres with staged execution.
- [x] **Smart Shelf Ribbon Highlighting across Library Search Scopes**
  * **All-Shelves Search Neutralization**: When searching across `All shelves` (either via search query or active library filters), individual shelf chips (e.g. `Rewatch`, `Watched`) are no longer highlighted as active, eliminating visual confusion about search boundaries.
  * **Instant Active State Restoration**: Toggling back to `This shelf` immediately restores the glowing active highlight to the currently selected shelf.
- [x] **4-Way Library Search Target Toggle (All → Title → Plot → Notes)**
  * **Added Plot Target**: Integrated `plot` into the library search target toggle with a clean text lines icon and label `Plot`.
  * **Seamless 4-Way Cycle**: Clicking the target pill cycles smoothly through `All` → `Title` → `Plot` → `Notes` → `All`.
  * **Search & Rank Integration**: Connects directly to backend plot matching (`overview` field) and local word-boundary regex ranking, updating search placeholder text accordingly (e.g., `Search plots in Rewatch…` or `Search plots across all shelves…`).
- [x] **Sidebar Search Preset Selection & Direct In-Row Rename Action**
  * **Sidebar Presets Selectable**: Restored clickable row selection for presets inside the sidebar workshop (`#ribbon-profiles-cloud`). Clicking any preset row selects and activates it, lighting it up with gold accent and immediately transforming the action button below into `Rename preset "<name>"`.
  * **Direct In-Row Rename Action**: Added a sleek pencil edit icon (`.chip-rename-btn`) on the preset row (revealed on hover beside the delete `×`), allowing instant 1-click renaming without needing to click down into the action button.
- [x] **Zero-Scroll Zen Storage & Local Data Surface**
  * **Zero-Scroll Viewport**: Redesigned the Storage page to fit entirely into a single viewport (~380px vertical footprint) without requiring any vertical scrolling.
  * **Cohesive Zen Visual Aesthetics**: Replaced outdated large gold headers and clunky cards with restrained editorial typography (`20px` heading, `10.5px` uppercase kicker, faint brand yellow `#DEC68B` tabular metrics, dark frosted glass cards).
  * **Single-Row Telemetry Strip**: Reorganized the 5 SQLite storage statistics into a unified 5-column dashboard strip (`Database Size`, `Cached Movies`, `Personal Library`, `Stale Cache`, and `Trash Bin`) with iconography and clear helper labels.
  * **Structured Action Zones**: Divided actions into three sleek horizontal strips: Data Portability & Backups (Export Notes `.md` and Export Library `.json`), Cache Maintenance (Clear TMDB Cache older than 90 days), and Permanent Purge (Purge Trash Bin). Integrated floating toast notices for instant confirmation.
- [x] **Fix Library Shelf Sort Chip View Leaks & Discovery Hijack**
  * **Root Cause Neutralized**: Discover sort event listeners (`initializeSortChips` / `syncSortChips`) were broadly querying all `.sort-chip` elements across the DOM instead of scoping strictly to `#sort-chip-cloud`. Clicking any sort chip inside the Library shelf (`#lib-sort-cloud`) was triggering Discovery mode's search engine (`runDiscoverySearch()`), which wiped out the shelf and redirected to an empty Discovery view.
  * **Strict Scoping**: Isolated Discover sort controls strictly to `#sort-chip-cloud .sort-chip`. Library sort chips are completely insulated and handled exclusively by `applyLibraryFilters()`.
  * **Toggle / Unselect Support**: Enabled radio-toggle behavior on Library sort chips so clicking an already active non-default sort chip (e.g. `Newest first`) cleanly toggles back to the default `Recently updated` sort and updates the shelf in-place without page hops.
- [x] **Live TMDB Sync Button for Presets & Discovery (Sidebar Header)**
  * **Placed Beside Reset**: Added a dedicated `[↻ Sync]` action link immediately beside `[↺ Reset]` in the sidebar filters header (`FILTERS` row) in the exact order requested (`Reset` first, then `Sync`).
  * **Fresh Live API Execution**: Clicking `Sync` clears the client cache and invokes `runDiscoverySearch({ forceRefresh: true })`, bypassing local cache to pull fresh, live movie results from TMDB for the currently active preset or active filter combination.
  * **Visual Harmony & Loading Spin**: Matches the subtle `11px` typography and muted color of `Reset`, with a smooth spin animation on the refresh icon while the live network request is in flight.
- [x] **Harmonious Footer Spacing: Eradicate 120px Dead Void Below Pagination**
  * **Eliminated Compounding Void**: Removed the compounding 180px gap below bottom pagination by reducing pagination `margin-bottom` from `56px` to `24px`, lowering `.library` `padding-bottom` to `12px`, and reducing `footer` `margin-top` to `20px`. The space from the pagination bar down to the footer hairline divider is now a balanced, cohesive ~56px–60px.
- [x] **Keyboard Navigation for Pagination across Discover, Library & Notes**
  * **Global Left / Right Arrow Keys**: Pressing `ArrowLeft` or `ArrowRight` (when not typing in an input field or viewing the movie detail modal) instantly triggers `‹ Prev` or `Next ›` in the bottom pagination bar across Discover, all Library shelves, and Notes.
  * **Interactive Key Feedback**: Injected `.is-key-active` visual feedback that flashes the targeted chevron button in faint brand yellow (`#DEC68B`, scale 0.95) for 180ms to confirm the shortcut execution.
- [x] **Search Profile Workshop Refinements & Universal Floating Toast Notifications**
  * **Dedicated Preset Rows (No Wrapping)**: Refactored the search profiles workshop into a 100% full-width stacked column (`display: flex; flex-direction: column;`). Sci-Fi and every other preset now occupy their own full dedicated row with star pin/unpin on the left, name in the center, and delete on hover on the right.
  * **Ribbon-Only Profile Selection**: Removed chip-click activation from the sidebar workshop. Search profiles are now selected and made active exclusively via the Discover ribbon chips, with re-clicking an active ribbon chip cleanly toggling off back to default/unsaved search.
  * **Dynamic Rename / Save Preset Chip**: When a search profile is active, `#save-profile` automatically converts to a rename action (`Rename preset "${name}"` with pencil icon) that opens the rename dialog to update the profile name. When no profile is active, it remains `Save current search as preset` with plus icon.
  * **Quiet Neutral Chip Parity & Clean Separation**: Redesigned `#save-profile` to blend seamlessly with the search preset chips (`32px` height, `0 10px` padding, `8px` squircle radius, `12.5px` font, neutral `1px solid rgba(255, 255, 255, 0.08)` border without loud borders), vertically aligned `+` / pencil icon and text, and separated by a clear `14px` breathing gap from the last preset above.
  * **Harmonious Profile Modal Dialog**: Replaced the loud modal styling with a compact Zen card (`width: min(390px, calc(100% - 32px))`, `12px` squircle radius, `#111115` dark background, `8px` blurred backdrop, scaled typography, and refined `32px` brand yellow action button).
  * **Universal Top-Right Floating Toast Notifications**: Shifted app-wide notifications (`.notice` / `#notice`) out of the document flow into a fixed top-right floating toast card (`top: 24px; right: 24px; z-index: 100000; max-width: 440px;`). It never pushes down the poster grid or page content, features dark frosted glass with distinct error/success badges, an instant `×` close button, and smooth auto-dismissal after 4.5 seconds.
- [x] **Zen Folio Bottom Grid Pagination: Minimal, Borderless & Centered Inline Direct Jump**
  * **Minimal Borderless Folio (`‹ Prev     1 / 23     Next ›`)**: Stripped all legacy numbered buttons (`1, 2, 3 ... 23`), borders, and background boxes. Structured as a centered flex row (`font-size: 13.5px; gap: 36px; user-select: none;`).
  * **Enlarged 20px Optical Chevrons**: Isolated `‹` and `›` in dedicated `.folio-chevron` elements sized to `20px` / `350` weight with subtle directional hover nudging (`±2px`), providing prominent, effortless visual recognition without font-size distortion of the `Prev` / `Next` labels.
  * **Precise Control States**: `‹ Prev` and `Next ›` controls render with `#9CA3AF` resting color, `#F3F4F6` on hover, and `#374151` with `pointer-events: none` when disabled (page 1 or last page).
  * **Direct Click-to-Type Page Jumping**: Center counter formats in tabular numbers (`font-variant-numeric: tabular-nums`). Current page illuminates in brand yellow (`#DEC68B`, 600 weight, hover underline). Clicking replaces the number with an inline `<input type="text">`, auto-focusing with text selected. Pressing Enter navigates (clamped `1` to `totalPages`), while Escape or blur reverts without navigation.
  * **Mathematical Grid Centering & Viewport Alignment**: Enclosed the 6-column poster grid and pagination inside `.movie-grid-viewport` (`width: 670px; max-width: 100%; display: flex; flex-direction: column; align-items: center;`), guaranteeing that the middle axis of pagination aligns dead-center directly under the 6 poster columns.
  * **Generous 76px Vertical Breathing Space**: Elevated top margin to `76px` with `56px` bottom padding, creating spacious breathing room beneath the poster rows.
- [x] **Related Movies Editorial Hierarchy & Spacing Harmony**
  * **Brand Faded Yellow Headline**: Stepped up the `Related Movies` section heading from 13px to `15px` / `600` weight, illuminated in the faint brand yellow (`#DEC68B`) matching the main title.
  * **Unified 24px Inter-Zone Spacing**: Eradicated the compounding 54px void above Related Movies by setting `.personal-ledger-panel` margin-bottom to 0 and `.related-panel` margin-top to an exact, disciplined `24px`.
  * **Crisp 12px Grid Separation**: Set `.related-heading` margin-bottom to `12px`, establishing an intentional, cohesive distance from the label to the 6-poster grid.
- [x] **Single Movie Poster Corner Status Badge: Deep Dark Contrast & Sizing Variants**
  * **Top-Left Corner Badge (1:1 Grid Parity)**: Positioned an icon-only status badge in the top-left corner of the 270×405px detail poster, instantly communicating whether a movie is in Discovery, Watch later, Watched, Rewatch, or Nope.
  * **Deep Contrast Glass Shield**: Backed with `rgba(9, 9, 11, 0.92)` dark glass, `backdrop-filter: blur(12px)`, hairline border `rgba(255, 255, 255, 0.16)`, and `box-shadow: 0 4px 14px rgba(0, 0, 0, 0.75)`, guaranteeing high visibility even over bright or white poster artwork.
  * **Vivid Punchy Glyphs**: Discovery (`✦` #F2C94C), Watched (`✓` #4ADE80), Watch later (`⏱` #38BDF8), Rewatch (`⟳` #FB923C), Nope (`⊘` #EF4444).
  * **Multi-Size Readiness**: Pre-configured three selectable scales: Small (24px badge / 13px icon), Active Large (32px badge / 18px icon), and Large (32px badge / 18px icon).
- [x] **Movie Detail Zen Polish: Double-Spaced Pure Genres, Wrapped Actor Dot Shield & Responsive Status Rail**
  * **Double-Spaced Pure Genres (Zero-Pill Architecture)**: Stripped all pill frames and commas from single movie detail genres. Rendered as pure typographic words in calm `#9CA3AF` separated by an elegant `14px` double-space breathing gap (`Thriller  Action  Mystery`).
  * **No-Leading-Dot Wrapped Actors (`white-space: nowrap`)**: Wrapped each actor + floating middle dot inside an atomic `.credit-item` span (`Matt Damon •`). When line wrapping occurs, the dot remains glued to the end of line 1, mathematically guaranteeing line 2 always begins cleanly with a letter.
  * **Grey Docked Mode Status Rail Responsiveness**: Resolved the clipped `Nope X` bug in Grey mode by replacing rigid `14px` pill padding with responsive `clamp(8px, 1.1vw, 14px)` and a compact `padding: 0 8px; gap: 4px;` rule for `body.grey-docked-open`, reducing total track width from 560px to 430px so all 5 options fit comfortably.
  * **Blueprint Order Restoration**: Restored `Title` $\rightarrow$ 8px $\rightarrow$ `Year • Rating • Votes` $\rightarrow$ 8px $\rightarrow$ `Genres` $\rightarrow$ 24px Clean Break $\rightarrow$ `Story Prose`.
- [x] **Movie Detail Blueprint Spacing: Precise 8px/12px/24px Cadence, Aligned 64px Labels & Floating Middle Dots**
  * **Precision Vertical Cadence**: Locked Title `line-height: 1.1`, Title $\rightarrow$ 8px $\rightarrow$ Genres, Genres $\rightarrow$ 12px $\rightarrow$ Metadata, and an intentional 24px clean break before Story Prose.
  * **64px Fixed Credit Labels**: Standardized `.credit-label` to `width: 64px` with baseline flex alignment, ensuring Director and Cast names align flush on the exact same left vertical line rather than staggering.
  * **Floating Middle Dots (`•` at 0.4 Opacity)**: Replaced sunken baseline periods with genuine middle dots (`•`, `\u2022`) at `opacity: 0.4`, bound via non-breaking space (`\u00A0• `) so dots float at exact mid-height (matching metadata) and never wrap as leading bullets.
  * **Pinned Hairline Footer**: Maintained 14px padding and `margin-top: auto` above the subtle hairline divider (`1px solid rgba(255, 255, 255, 0.05)`) with a 6px gap between Director and Cast.
- [x] **Movie Detail Refinements: Framed TMDB Dossier Slab, Pinned Credits Footer & Elevate-on-Scroll Header**
  * **Zero-Border Rest Header (Double-Walling Elimination)**: Removed the static border and shadow from `.detail-page-header` at page rest, allowing the header to merge seamlessly into the `#09090b` canvas with zero border-stacking collision against the top of the dossier. Added dynamic `.is-scrolled` elevation that softly fades in the frosted glass, hairline divider, and shadow on downward scrolling.
  * **Framed TMDB Dossier Card**: Transformed `.detail-top-info` into a matching editorial companion card (`min-height: 405px`, 2% tint, hairline border, 12px squircle radius, 20px 24px padding), perfectly mirroring the 270×405px poster dimensions shoulder-to-shoulder.
  * **Pinned Credits Footer**: Pushed Director and Cast credits to the base of the TMDB Dossier box (`margin-top: auto`) above a subtle hairline divider (`1px solid rgba(255, 255, 255, 0.05)`), turning dead vertical void on short plots into purposeful, structured editorial layout.
  * **Lower Baseline Parity (14px Gap)**: Synchronized `.personal-ledger-panel` margin-top to `14px`, matching the exact margin of the poster keywords for a unified horizontal horizon across columns.
- [x] **Movie Detail Zen Architecture: Inset Personal Ledger Panel, Reading Measure Cap & Poster Baseline Alignment**
  * **Subtle Inset Personal Ledger Panel**: Enclosed personal interaction controls (Segmented Status Rail, 10-Star Verdict + Heart, and Personal Notes) inside an elegant, low-contrast workspace card (`.personal-ledger-panel`, 2% white tint, hairline border `rgba(255, 255, 255, 0.07)`, 12px squircle radius, 18px 20px padding).
  * **Vertical Poster Baseline Alignment**: Applied `min-height: 405px !important;` to `.detail-top-info`, guaranteeing that the personal ledger panel in the right column consistently anchors at or below the 405px base horizon of the movie poster across short and long plots alike.
  * **Constrained Editorial Measure (560px)**: Capped plot synopsis (`.dialog-overview`) and credits (`.credits-lines`) to `max-width: 560px` (~65ch reading measure) for comfortable, book-like typography with a breathing margin against the 670px canvas.
  * **Strict Spacing & Indentation**: Indented rating row by 14px flush under `Discovery`, placed Heart directly below `Watched`, and locked vertical rhythm to 10px between Title $\rightarrow$ Metadata $\rightarrow$ Genre Chips.
- [x] **Movie Detail Refinements: Dedicated Metadata Subline, Harmonious 16px Cadence & Hover Consistency**
  * **Dedicated Metadata Subline (All-Title Stability)**: Standardized factual release metadata (Year • Language • Rating • Votes) onto its own dedicated subline directly beneath the title headline on every movie, eliminating flex-wrap clipping on long titles (like *The Lord of the Rings*).
  * **Unified 16px Personal Vertical Rhythm**: Eradicated the compounding 40px margin gap above the notes panel, establishing an exact, even 16px cadence across all three personal tiers (Status Track $\rightarrow$ 16px $\rightarrow$ 10 Stars + Heart $\rightarrow$ 16px $\rightarrow$ Journal Notes).
  * **Optical Grid Anchoring**: Indented the 10-star rating row by 14px so the first star sits flush beneath the capital D of Discovery, while the Favorite Heart lands directly beneath Watched.
  * **Always-Visible Heart & Seamless Favoriting**: The favorite heart icon is permanently visible in a calm muted outline (#4B5563), never disappearing or popping in/out based on watch status. Favoriting automatically records the movie as watched if unreviewed.
  * **Actor & Director Hover Color Harmony**: Replaced harsh neon yellow (#ffe071) on actor/director hover with the exact faint brand yellow (#DEC68B) of the movie title.
  * **Brand Yellow Vote Icon**: Rendered the how_to_vote icon in matching faint brand yellow (#DEC68B).
- [x] **Movie Detail Zen Flow: Segmented Status Track, Dual Verdict Row & Toned-down Credits**
  * **Unified Segmented Status Track (Zero-Pill Architecture)**: Replaced disjointed floating pill chips with a sleek continuous segmented rail ([ Discovery D | Watch later L | Watched W | Rewatch R | Nope X ]). Structured with centered 14px hairline dividers and balanced 14px padding for mis-click-free hit targets.
  * **Pure Typography Active State (No Fill)**: Eradicated pill background fills. Inactive items stay muted grey (400 weight). The active status illuminates in brand yellow (#DEC68B, 600 bold) with an accented shortcut badge (#EF4444 for Nope).
  * **Dual Verdict Row (Stars + Heart)**: Repositioned the Favorite Heart directly beside the 10-star rating row with 22px breathing room (★ ★ ★ ★ ★ ★ ★ ★ ★ ★    <space>   [ ♥ ]), completely clearing the title row and uniting score and like verdicts.
  * **Star Color Consistency**: Replaced saturated bright yellow with the exact faint brand yellow (#DEC68B) of the movie title for selected and hover stars.
  * **Title Metadata Left-Shift & Clean Votes**: Shifted year/language/rating metadata closer to the title (gap tightened from 16px to 10px, baseline-aligned). Stripped parentheses brackets from votes and integrated the how_to_vote icon (• ★ 6.3 • [how_to_vote] 3,775 votes).
  * **Toned-Down Director & Cast**: Toned down actor/director clickable links from stark white (#E5E7EB) to calm silver grey (#9CA3AF), with muted labels (#8E8B97) and dim separators (#4B5563), preserving gold hover illumination.
  * **Responsive Arrow Navigation**: Pressing Left or Right arrow keys on the keyboard now triggers an immediate active pulse highlight on the #detail-prev-btn and #detail-next-btn header buttons.
- [x] **Movie Detail Page Typography Audit & Discovery/Library Scale Harmonization**
  * **Unified Scale Parity**: Eliminated fractional, arbitrary font steps (11.5px, 12.5px, 13.5px, 15px, 15.2px) and matched Discovery & Library's clean 4-tier semantic hierarchy (11px micro, 12px chips/controls, 13px standard UI, 14px body reading).
  * **Parity on Chips & Pills (12px, 500 weight)**: Genre chips and keywords under the poster now share identical 12px sizing, 500 medium weight, and 24px pill geometry with Discovery filter tags and shelf status pills.
  * **Clean Subordinate Metadata (13px)**: Brought Year · Language metadata down from 15px/450 weight to 13px/500 weight, correctly subordinating factual metadata to the display title.
  * **Synopsis & Notes Reading Harmony (14px, 1.6 line-height)**: Brought the private thoughts journal textarea from 15px/1.7 down to 14px/1.6, creating consistent reading and writing flow between synopsis and personal reflections.
  * **Legible Status Badges & Controls**: Fixed the related-card status badge from unreadable 0.48rem (~7.7px) to 11px/600 weight, and aligned header stepper buttons to 12px.
  * **Eliminated Weight 450**: Replaced all blurry 450 font weights across genres, keywords, and release metadata with standard 500/400 weights.
- [x] **Movie Detail Refinements: Clean Poster, Inline Rating, Gap Removal & Unified Pill Geometry**
  * **Unobstructed Poster Artwork & Inline Rating**: Stripped corner badges (`★ 6.4` and `532 votes`) from the movie poster to keep artwork 100% clean. Re-placed rating and vote count inline beside the year and language (`2006 • English • ★ 6.4 (532 votes)`), removing the stray leading bullet dot before the release year.
  * **Restored Favourite Button**: Restored the circular heart button next to the movie headline, enabling immediate favorite status toggling.
  * **Clean Cast Row**: Removed the stray leading bullet dot directly following the `Cast:` label (`Cast: Nathan Baesel • Angela Goethals...`).
  * **Eliminated Status Pill Gap**: Removed the artificial `min-height: 405px` and margin offsets on `.detail-top-info`, creating a consistent, natural `24px` spacing directly above the status pill row.
  * **True Borderless Left-Spine Note**: Formatted notes with ONLY an editorial left vertical spine (`border-left: 2px solid rgba(255, 255, 255, 0.22); padding-left: 14px`), no bottom border, no resize grip, and omitted redundant movie title headers from Grey critique insertions.
  * **Unified Pill Geometry (`border-radius: 999px`)**: Standardized genre chips, keyword chips, and the `Hide tracked movies` button with smooth `999px` pill geometry.
- [x] **Discover Total Movie Count & Pagination Top Breathing Space**
  * **Discover Total Count Display**: Eradicated the useless batch message ('24 movies on this page') on the Discover page. It now always displays the actual total movie count (e.g. 1,820 movies).
  * **Pagination Breathing Room on Top**: Set margin-top: 52px on .pagination to give generous, elegant breathing room below the bottom row of movie cards, centered across the 670px grid with universal 8px squircle buttons.
  * **Title & Metadata Ample Separation**: Created generous 16px breathing room between the faint yellow movie title and the inline metadata (• Year • Language).
- [x] **Movie Detail Faint Yellow Title, Genre/Keyword Chips & Borderless Journal Note**
  * **Main Title Faint Yellow**: Softened the headline from stark white to faint brand yellow (#DEC68B), with release metadata (• Year • Language) resting inline beside it at a subordinate 15px scale.
  * **Flat Genre & Keyword Chips**: Reverted genres into structured squircle chips and unified keyword chips with slight brand yellow text (#DEC68B), completely flat with zero glow, inner shadow, or drop shadow.
  * **Borderless Journal Note**: Eradicated the boxed-in 'Personal Memories' card and rigid <textarea> field. Sits directly in the natural flow below the Action Cockpit with an editorial left spine (▎) in brand gold, auto-expanding as thoughts are typed with seamless auto-save.
- [x] **Movie Detail Typography & Information Hierarchy Overhaul**
  * **Title with Inline Year & Language**: Title maintains prominent display sizing, followed inline by factual release metadata (• Year • Language) in a refined, muted 15px font.
  * **Clean Text Genres (Pills Removed)**: Eliminated heavy bordered badge pills from genres, replacing them with clean inline editorial text separated by dot dividers (Crime • Drama).
  * **User Judgment Placement**: Relocated star rating and vote count directly below genres and above the plot summary, logically grouping user-related rating data.
  * **Underline-Free Interactive Credits**: Stripped underlines and border-bottom rules from director and actor clickable links. Added a leading dot (• ) and generous bullet spacers (  •  ) between cast members to eliminate crowding while preserving full clickability.
  * **Suppressed Status Kicker**: Suppressed the kicker badge from the top of the title pending future prominent placement.
- [x] **Movie Detail Left-Anchored Canvas (Halved Left Space & Poster/Button Alignment)**
  * **Halved Left Dead Space**: Reduced the desktop left offset from ~140–155px centering margin down to a clean `64px` left padding, shifting the entire movie detail layout to the left as requested.
  * **Strict Vertical Alignment**: Left-anchored both `.detail-header-inner` and `.detail-hero` at `margin: 0`, guaranteeing that the `[ ← Back to ... ]` button and the left edge of the poster are 100% vertically aligned on the exact same `64px` axis.
- [x] **Movie Detail Cinematic Poster Scaling (270x405px)**
  * **Proportional Poster Expansion**: Stepped the movie poster up from `240x360px` to `270x405px` (+12.5% increase in width and height, adhering to the 2:3 aspect ratio).
  * **Harmonious Grid & Alignment Update**: Expanded `.detail-hero` grid column to `270px` (with `30px` gap), aligned `.detail-top-info` min-height to `405px`, and broadened container bounds to `970px` while maintaining complete fluidity for both normal and Grey docked modes.
- [x] **Movie Detail Refresh-Resilient Hash Routing (#movie:ID)**
  * **Full Refresh Resistance**: Added `#movie:${id}` hash routing and session persistence to the single movie detail page. When pressing F5 (refresh), bookmarking, or sharing a direct movie URL, the app restores the background shelf context and re-opens the exact movie detail view instantly.
  * **Seamless Back Navigation & Browser History**: Closing the movie or clicking browser back cleanly transitions back to the origin shelf view (`#watched`, `#rewatch`, `#discover`, etc.) and keeps the history stack in perfect sync.
- [x] **Movie Detail Consistent 510px Description Reading Measure**
  * **Unified Reading Width**: Standardized the maximum width of the movie description (`.dialog-overview`) and credits (`.credits-lines`) to `510px` across both normal full-width view and Grey docked view. This locks in the comfortable, book-like typographical measure (~65-75 characters per line) and eliminates excessively wide, stretched-out paragraphs on wide screens.
- [x] **Movie Detail Grey Drawer Responsiveness (Zero Text Cutoff)**
  * **Flexible Dynamic Column Sizing**: Replaced rigid `width: 670px` and `min-width: 540px` with fluid `width: 100%; max-width: 670px; min-width: 0;` on `.detail-top-info`, `.dialog-overview`, and `.credits-lines`.
  * **Grey Docked Open Text Wrap**: Added `overflow-wrap: break-word` and explicit responsive width rules when Grey is open (`body.grey-docked-open`), ensuring the plot description and cast lines wrap cleanly within the available screen width without clipping against Grey's 420px drawer.
- [x] **Movie Detail True Inline Favorite Flow (Multi-Line Title Support)**
  * **Eliminated Flexbox Blockification**: Converted `.detail-title-wrap` from a flex container (`flex-wrap: wrap`) to a block/inline text container, allowing `<h1>` to remain genuinely `display: inline` and `.favorite-button` to remain `display: inline-flex`.
  * **Seamless Inline Heart Flow**: The favourite button now sits directly at the end of the title on the same line (even when the title wraps across multiple lines, e.g. *The Naked Gun: From the Files of Police Squad!*), completely eliminating the accidental 3rd-line orphan wrap.
- [x] **Movie Detail Uniform Vertical Rhythm (Harmonious 22px Section Gaps)**
  * **Eliminated Compounding Flexbox Margins**: Cleared the redundant 24px bottom margin on `#detail-action-cockpit` and standardized the gap between the rating row and Personal Memory to a clean, intentional 22px (down from an accidental 48px void).
  * **Uniform Section-to-Section Rhythm**: Harmonized every inter-section vertical gap across the entire lower canvas to exactly 22px (Action Cockpit → Personal Memory → Related Movies), paired with a snug 12px gap between status pills and star rating and an 8px label-to-textarea gap.
- [x] **Movie Detail Brand Muted Yellow Accents & Flowing Keywords**
  * **Brand Muted Yellow Rating & Vote Count**: Styled the vote count text (`(13.9k votes)`) and star icon (`★`) in matching brand muted yellow (`#DEC68B`), with coordinating icon hue for harmonious visual hierarchy.
  * **Flowing Poster Keywords**: Maintained natural horizontal flex-wrapping for `.poster-keywords` below the 240px poster column.
- [x] **Movie Detail Dynamic Origin Return, Overview Order Restoration & Prominent Kicker**
  * **Dynamic Back Navigation Label**: Replaced generic `"Back to movies"` with dynamic context-aware origin return labels: `"Back to Watched"`, `"Back to Rewatch"`, `"Back to Watch Later"`, `"Back to Discovery"`, `"Back to Favourites"`, `"Back to Nope"`, `"Back to Notes"`, and `"Back to [Person]"`.
  * **Restored Canonical Order (Overview before Credits)**: Restored the exact order in `.detail-top-info`: Title & Heart → Genres → Metadata row → Dynamic Plot Overview → Director & Cast lines (`.credits-lines`).
  * **Enlarged Status Kicker**: Increased the uppercase status kicker font size to 14px with a 16px status icon (`gap: 8px; margin-bottom: 12px; font-weight: 700`), giving clear visual prominence above the title.
- [x] **Movie Detail Header Parity (Exact 64px Match with Discover/Library)**
  * **Unified 64px Header Height**: Aligned `.detail-page-header` to the exact 64px height (`height: 64px !important; min-height: 64px !important; max-height: 64px !important; padding: 0 24px !important;`) of the Discover and Library `.topbar` navigation header, establishing complete visual consistency and navigation continuity across views.
- [x] **Movie Detail Color Parity, Spacing Tightening & Anchored Credits Architecture**
  * **Unified Site & Header Canvas Color**: Standardized `.movie-detail-page` to identical `--bg` (`#09090b`), eliminating conflicting radial gradient overlays and ensuring total color harmony between `.detail-page-header`, the detail page canvas, and the rest of the application.
  * **Reduced Header-to-Details Space**: Slimmed `.detail-page-header` from 60px to 48px (`padding: 6px 16px`) and tightened `.detail-page-content` top padding from 24px to 12px, connecting the header smoothly to the movie details.
  * **Anchored Director & Cast Placement**: Positioned `Director:` and `Cast:` directly below the metadata row at the exact same vertical position across all movies, eliminating vertical jumping between movies.
  * **Dynamic Description Loading**: Enabled full dynamic expansion for the overview description text without artificial height constraints or internal scrollbars.
  * **Below-Poster Baseline Lock & Collision Prevention**: Configured `.detail-top-info` with `min-height: 360px` and a 24px vertical margin before `#detail-action-cockpit`, ensuring the shelf status pills always start below the 360px poster baseline across all movies with zero overlap onto cast or description lines.
- [x] **Movie Detail Predictable Top Zone Placement & Below-Poster Status Lock**
  * **Consistent Placement for Description, Director & Cast**: Standardized vertical positions for all movie details. The header stack (Kicker, Title, Genres, Meta) occupies the top with generous breathing room, the description loads dynamically in a clean scrollable zone, and `Director:` and `Cast:` sit anchored at the bottom of the 360px box.
  * **Status Always Starts Below Poster**: The 360px top zone guarantees that the shelf status pills and 10-star rating row always begin strictly below the bottom baseline of the 240x360px poster across all movies.
  * **Uncramped Header Hierarchy**: Relaxed spacing throughout the top stack: 10px kicker-to-title, 14px title-to-genres, 14px genres-to-meta, and 16px meta-to-description.
  * **Removed Related Movies Divider**: Eradicated the divider line above `.related-panel` to keep the transition to Related Movies borderless.
  * **Uncramped Header Hierarchy**: Relaxed spacing throughout the top info stack: 10px kicker-to-title, 14px title-to-genres, 14px genres-to-meta, and 16px meta-to-description, giving clean visual breathing room.
  * **Eradicated Artificial Dead Space Beneath Description**: Removed rigid fixed height and `margin-top: auto` on credits; `Director:` and `Cast:` now sit naturally 18px below the description with consistent line-height (1.68) and relaxed 15px font sizing.
  * **Removed Related Movies Divider**: Removed the top border line above `.related-panel` to keep the transition to Related Movies seamless and borderless.
  * **Uppercase Semantic Status Kicker**: Formatted kicker to clean uppercase semantic text (`WATCHED`, `REWATCH`, `NEW DISCOVERY`, `WATCH LATER`, `NOPE`, `UNTRACKED`) with color-coded accents.
- [x] **Movie Detail Zen Hierarchy Reordering, Liberated Cockpit & Icon Refinement**
  * **Status Kicker Scale & Tone**: Enlarged the status kicker to 14px with status icons in a muted tone and status label in regular muted white (`#D1D5DB`).
  * **Title & Enlarged Heart in Enclosed Circle**: Vertically aligned the title with the heart button (`gap: 12px`), with the heart glyph enlarged (`1.35rem`) inside the circular toggle button (`width: 32px; height: 32px; border-radius: 50%`).
  * **Harmonious Typographic Spacing Rhythm**: Balanced vertical rhythm across the entire column: 8px kicker-to-title, 12px title-to-genres, 12px genres-to-meta, eliminated the 30px gap above overview down to a clean 16px, 16px between overview and director, 7px between credit lines, and eliminated the 48px gap above status pills down to a natural 18px flow directly beneath credits.
  * **Strict Hierarchy Reordering**: Restructured the movie header layout: Movie Title → Genre chips directly under title (`#dialog-genres`) → Year, language, star rating (`★ 7.5`), and vote count with icon (`[vote icon] (1.1k votes)`) directly under genres without "TMDB" text (`#dialog-meta`).
  * **Neutral Status Selector Pills**: Removed gaudy/neon colored borders from shelf selector pills; active pills now take a calm neutral border (`1px solid rgba(255, 255, 255, 0.22)`) with icons retaining their color in a muted tone.
  * **Clear Star Rating Action**: Added a clear icon button (`✕`, `#clear-verdict`) in the 10-star rating row that appears when a movie is rated, enabling 1-click rating reset back to unrated.
  * **Liberated Action Cockpit & Natural Text Alignment**: Removed the enclosing card box around the status pills and stars (`.personal-panel` background, border, shadow set to none; zero padding), allowing shelf selector chips and star rating to align naturally with the text of the movie descriptions.
  * **Suppressed Remnant Feedback Notifications**: Eradicated lingering feedback messages (`Watched saved.`, `✓ 8/10 saved.`) so status and verdict updates remain silent and clean.
- [x] **Movie Detail Strict Zen Alignment & Single-Row Ergonomics**
  * **Locked Top Nav to Content Edges**: Aligned the inner container of `.detail-page-header` (`.detail-header-inner`, width `min(938px, calc(100% - 32px))`) strictly with `.detail-hero` below it. The left edge of `← Back to results` sits on the exact same vertical x-axis as the left edge of the movie poster, and the right edge of `< Prev | Next >` aligns with the right edge of the 670px main column (Action Bar / Notes box / 6th Related Movie).
  * **Neutral Calm Surface on Nav Pills**: Neutralized the yellow/gold tint on `← Back to results`; styled both `← Back to results` and `< Prev | Next >` with `background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.10); color: #D1D5DB; border-radius: 8px;`.
  * **Tightened Inline Credits Gap**: Tightened the spacing between `Director:` / `Actors:` labels and their values to `8px` (`color: #9CA3AF` for labels, `#E5E7EB` with subtle underline for names) eliminating the wide tab gap.
  * **Subtle Circular Favourite Heart Toggle**: Wrapped the Favourite heart (`♥`) next to the movie title in a circular toggle button (`width: 32px; height: 32px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; background: rgba(251, 113, 133, 0.08); border: 1px solid rgba(251, 113, 133, 0.28);`).
- [x] **Refined Title, Heart & Metadata Vertical Spacing**
  * **Snug Title-to-Heart Alignment**: Tightened the horizontal gap between the movie title and the heart icon from 14px/19px down to a snug 6px with an unpadded 20px button container, eliminating floating distance.
  * **Balanced Vertical Breathing Room**: Increased the bottom margin of the title wrap to 14px, providing clean vertical separation between the title and the metadata row below.
- [x] **Relaxed Typographic Spacing for Plot Overview & Credits Lines**
  * **Spacious Credits Rhythm**: Replaced cramped 4px stacking with a distinct 10px flex gap between Director and Actors lines, and added `min-width: 68px` to labels for clean key-value column alignment.
  * **Breathing Room**: Increased vertical spacing above and below the plot overview (`margin: 14px 0 20px 0`, `line-height: 1.72`), expanded the gap above the action cockpit card to 24px, and removed noisy baseline underlines from actor links.
- [x] **Full Responsiveness when Grey Cinema Companion is Docked Open**
  * **Fluid Adaptive Widths**: Converted fixed layout constraints on both the single movie page and main library/discover shell to fluid responsive grids when Grey is open (`calc(100vw - 420px)`), preventing blowout, truncation, or unresponsive lockup.
  * **Sidebar & Movie Grid Adaptation**: Slims sidebar to 240px below 1400px and collapses cleanly below 1140px; wraps movie posters using `repeat(auto-fill, minmax(95px, 105px))` so content remains fully accessible without horizontal clipping.
- [x] **Faded Secondary Section Headings (Personal Memory & Related Movies)**
  * **Muted Visual Hierarchy**: Reduced heading styles on `.detail-notes-header h2` and `.related-heading h2` from stark `#FFFFFF` (weight 700) to quiet, secondary `#8E8B97` (weight 500, `0.95rem`), eliminating visual distraction from primary movie details.
- [x] **Movie Detail Page Canvas Alignment & Original Poster Proportions**
  * **Original Poster Scale**: Restored the poster to its exact original dimensions (`240px` by `360px`, `10px` border radius).
  * **Eliminated Space Between Poster and Main Text**: Pushed the poster to the right edge of the 310px column (`margin-left: auto; align-items: flex-end`), creating a tight, standard 20px gap between the poster and the 670px main body.
  * **670px Body & 6-Column Related Movies**: Constrained the movie body, action cockpit, personal memory, and related movies to 670px, exactly matching the Discover/Library search bar and 6-column movie grid (`repeat(6, minmax(0, 105px))`).
- [x] **Movie Detail Page Canvas Alignment (Poster in Place of Sidebar)**
  * **2-Column Structural Parity**: Positioned the movie poster in the 310px first column (directly replacing the 310px sidebar from Discover/Library), and placed the movie body details in the second column (matching the library canvas start). The back button aligns directly above the poster in column 1, and the stepper aligns to the right.
  * **Main Canvas Parity**: Aligned the single movie detail page (`.detail-page-content` and `.detail-page-header`) to start at the exact same horizontal coordinate as the Discover and Library main canvas (`padding-left: 330px`, matching the 310px sidebar + 20px library gutter). Navigation between Discover/Library and the movie detail page produces seamless visual continuity without horizontal layout jumping.
  * **Responsive Collapsing**: Automatically collapses the 330px offset on viewports <= 860px to standard 16px padding.
- [x] **Favourites Heart Button - Reversible 2-Way Toggle**
  * **Interactive Reversible Toggle**: Restored the Hall of Fame Heart button in the shelf ribbon (`#shelf-favorites-btn`) as a clickable 2-way toggle.
  * **Memory Return**: 1st click remembers the previous shelf (e.g. `Watched` or `Watch later`), illuminates the Heart in crimson/gold, and loads Favourites. 2nd click un-highlights the Heart and immediately returns to the previous shelf.
- [x] **Personal Memory Label Heading for Movie Notes**
  * **Cohesive Section Heading**: Added a clear, styled `<h2>Personal Memory</h2>` heading to `.detail-notes-header` inside the movie notes card, visually matching the `<h2>Related Movies</h2>` styling (`1.15rem`, weight 700, `#FFFFFF`, clean line height) with status feedback on the right.
- [x] **Removed Note Icon from Library Movie Posters**
  * **Clean Poster Surface**: Eradicated the small note icon badge (`.card-note-mark`) from movie posters across the library and discover grids, creating an uncluttered poster presentation.
- [x] **Movie Detail Unified Typography Hierarchy & Standalone Unboxed Heart**
  * **Unified Typography Hierarchy**: Standardized all typography across the movie detail cockpit under --font-ui (Plus Jakarta Sans) with balanced font scaling (Title: ~30px 700, Overview: 14.5px 1.65 line-height, Credits: 13.5px with clean non-underlined links, Meta: 13px, Badges/Tags: 11px, Notes: 13.5px), eradicating size and font inconsistencies.
  * **Standalone Unboxed Heart**: Removed the enclosing circle, borders, and backgrounds from the detail page Heart button (#favorite-button), leaving a crisp, floating standalone heart icon beside the title that fills with solid red when favorited.
- [x] **Movie Detail Page Canvas Parity, Inline Heart & Typography Proportions**
  * **Main Canvas Geometry Parity**: Expanded the single movie detail page header and content from the cramped 1080px box to the exact full canvas bounds of Discover and Library (width: min(100% - 32px, 1536px)), eliminating layout pinching.
  * **Title & Inline Heart**: Placed the 32px circular Heart toggle directly beside the movie title (.detail-title-wrap), removing awkward vertical dead space.
  * **Reduced Title Scale**: Reduced movie title font-size from oversized 3.45rem (~55px) to a balanced, cinematic clamp(1.65rem, 2.5vw, 2.2rem) with crisp 1.15 line-height.
  * **Interactive Cockpit Shelf Pills**: Wired the status pills (Discovery, Watch later, Watched, Rewatch, Nope) with instant 1-click status toggling and semantic status borders matching the Zen chip design system.
  * **Dynamic Kicker Status Colors**: Set the header kicker to dynamically reflect the movie's status color (Emerald for Watched, Sky Blue for Watch Later, Amber for Rewatch, Crimson for Nope, Cinema Gold for New Discovery).
- [x] **Passive Unclickable Heart in Library Shelf Ribbon**
  * **Unclickable Heart**: Converted the ribbon heart (.shelf-favorites-btn) from an interactive button into a passive indicator (<span> with pointer-events: none !important; cursor: default !important; user-select: none !important), disallowing clicks while retaining active reflection when viewing Favourites.
- [x] **Eradicated Inner Glow & Shading Across Sidebar Filter Chips (Languages, Genres, Countries, Entities)**
  * **Zero Inner Glow / Shadow**: Removed the colored background fills and inner shading (rgba 6% fills) from active filter chips (.tri-chip.is-included, .tri-chip.is-excluded, .filter-chip.is-active, .selected-entity).
  * **Clean Transparent Body Parity**: Chips in Languages, Genres, Countries, and Person/Studio entities now remain completely transparent (ackground: transparent !important, ox-shadow: none !important), exactly matching the clean, unshaded look of inactive Country chips while borders and glyphs clearly indicate selection.
- [x] **Refined 1.25px Inactive & 1.75px Active Ribbon Chip Borders**
  * **1.25px Inactive Border**: Upgraded the idle chip hairline border from 1px to a crisp 1.25px (rgba(255, 255, 255, 0.16)), eliminating fadedness and providing solid squircle definition across both Discover presets and Library shelves.
  * **1.75px Active Border**: Elevated selected status-colored chip borders to 1.75px (85% opacity) for a distinct tactile emphasis, while maintaining pure transparent backgrounds (zero inner shades).
- [x] **Distinct 1.5px Status-Colored Active Chip Borders (No Inner Shades)**
  * **Thicker Active Border**: Increased selected chip border thickness from 1px to a crisp 1.5px with 80% opacity, providing a clear, tactile badge emphasis over idle 1px chips without layout shifting.
  * **Zero Inner Shades**: Maintained completely transparent backgrounds and zero box shadows across all states.
- [x] **Status-Colored Active Chip Borders with Pure Transparent Backgrounds (No Inner Shades)**
  * **Icon-Matched Active Borders**: Each selected library shelf chip takes the exact semantic color of its icon for its hairline border (Emerald #4ADE80 for Watched, Sky Blue #38BDF8 for Watch Later, Warm Amber #FB923C for Rewatch, Crimson Red #EF4444 for Nope, Soft Gold #DEC68B for New Discovery).
  * **Zero Inner Shades**: Completely eliminated all background fills and tints across idle, hover, and active states (ackground: transparent !important, ox-shadow: none !important), rendering clean, unshaded squircle outlines with high-contrast white text.
- [x] **Semantic Status-Colored Library Shelf Icons (Dimmed & Refined)**
  * **Color-Coded Status Icons**: Applied dimmed semantic status tints (at 75% opacity) to library shelf chip icons: Emerald (#4ADE80) for Watched, Soft Gold (#DEC68B) for New Discovery, Sky Blue (#38BDF8) for Watch Later, Warm Amber (#FB923C) for Rewatch, and Crimson Red (#EF4444) for Nope.
  * **Dynamic Hover & Active Vibrancy**: Brightens cleanly to 100% saturation on hover and retains full semantic color fidelity when the shelf is active, without neon glare or text distraction.
- [x] **Ribbon Chips Definition & Readability (Discover Presets & Library Shelves)**
  * **Visible Hairline Borders**: Raised inactive chip border opacity to 15% white (rgba(255, 255, 255, 0.15)) and active borders to 45% cinema gold (rgba(212, 175, 55, 0.45)), giving each squircle clean visual boundary definition.
  * **Sharp, Legible Typography**: Increased font weight from thin 400 to medium 500/550 with antialiasing, lifting inactive text to neutral light grey (#D1D5DB) and active text to warm cream (#F3E8D2).
  * **Tactile Chip Body**: Lifted inactive chip background to 4.5% white and active to 9% gold, and brightened inactive icons to slate (#9CA3AF) for balanced contrast against the dark canvas.
- [x] **Refined Header Master Navigation (Crisp Typography, Hairline Underline & Toned-Down Gold Icons)**
  * **Crisp Header Titles**: Reduced font-weight from chunky 700/800 to a clean SemiBold 600 with subpixel antialiasing and balanced 0.09em letter-spacing, eliminating text bleed and blur across DISCOVER, LIBRARY, and NOTES.
  * **Hairline Underline Indicator (Zero Glow)**: Replaced the 2px glowing highlighter with a razor-sharp 1px hairline indicator in warm cinema gold (#DEC68B), completely removing the neon box-shadow blur.
  * **Toned-Down Navigation Icons**: Removed the harsh yellow (#f2c94c) and fuzzy drop-shadow filter from active icons, replacing it with quiet, muted cinema gold (#DEC68B) and razor-sharp rendering.
- [x] **Unboxed Personal Action Lenses (Notes & Heart) with Balanced Proportions**
  * **Unenclosed Floating Icons**: Removed squircle box containers, borders, and backgrounds from the Personal Notes (#shelf-notes-lens-btn) and Favourites Heart (.shelf-favorites-btn) action lenses in the library shelf ribbon row, rendering them as borderless, transparent standalone icons.
  * **Optical Mass & Proportion Balance**: Increased Personal Notes icon SVG size to 18px to optically balance the 16px Heart icon.
  * **Active States Preserved**: Retained cinema gold stroke (#DEC68B) for active Notes lens and solid red stroke/fill (#E05252) for active Favourites Heart.
- [x] **Right-Aligned Personal Action Lenses (Notes & Heart)**
  * **Negative Space Demarcation**: Applied `margin-left: auto` to `.shelf-ribbon-divider`, anchoring the divider, Notes lens (`📄`), and Favourites Heart (`♡`) buttons flush against the right edge of the 670px shelf ribbon row.
  * **Visual Separation**: Established open negative space between the 5 shelf status chips on the left and the 2 personal archive lenses on the right, perfectly matching the 670px search bar alignment above.
- [x] **Full Library Search Area Restoration (Canvas Header, Dual Micro-Pills & Notes Lens)**
  * **Zero-Shift Library Canvas Header**: Reconnected `#library-canvas-header` visibility switching in `setActiveView`, `toggleDetailPage`, `restoreSearchSnapshot`, and filmography mode. It mirrors `#discover-canvas-header` with exact 102px vertical geometry parity and 670px 6-column alignment, eliminating layout shift.
  * **Dual Micro-Pills in Search Bar**: Restored full interactive wiring and styles for `#library-scope-toggle` (toggling between `[ ◫ This shelf ]` ⇄ `[ ☷ All shelves ]` with `.is-all-shelves` highlight) and `#library-target-toggle` (cycling between `[ ✦ All ]` → `[ 🏷 Title ]` → `[ 📝 Notes ]` with `.is-active-target` highlight).
  * **Dynamic Human-Readable Live Placeholder**: Restored `updateLibrarySearchPlaceholder` to continuously reflect current search scope and field in plain English (*"Search in Watched…"*, *"Search titles in Watched…"*, *"Search notes across all shelves…"*, *"Search all notes…"*) without requiring cryptic syntax prefixes.
  * **Bidirectional Notes Lens & Ribbon Divider**: Restored styling and interaction for `.shelf-ribbon-divider` (1px vertical hairline) and `#shelf-notes-lens-btn` (28px squircle with active gold border/stroke and double-click to exit), working in symmetry with `.shelf-favorites-btn`.
- [x] **Universal 8px Squircle Chips & Nope 'X' Icon Consistency**
  * **8px Squircles Everywhere (No Ellipsoids)**: Replaced 999px pill/capsule radii with clean 8px squircles across all chips: preset ribbon chips, library shelf ribbon chips, scope/target toggles, sidebar tri-chips, filter chips, profile workshop chips, sort chips, status chips, and selected entity tags.
  * **Nope Icon Standardization to 'X'**: Replaced prohibition/ban circle ('dont' circle-slash) with a crisp 'X' across the entire interface: Material Symbols glyph set to 'close' (on poster badges and sidebar status filter) and inline SVG vectors updated to clean crossed lines (in library shelf ribbon and movie detail cockpit).
- [x] **Zen Discovery Search Bar, Ribbon Chips & 102px Header Parity**
  * **Zen Search Bar (.toolbar-search)**: Standardized to 36px height, 670px width (flush with 6-column movie grid), sleek borderless dark fill (rgba(20, 20, 25, 0.92)), subtle border (rgba(255, 255, 255, 0.08)), 8px squircle radius, quiet 14px magnifying icon, clean placeholder in #8E8B97, and zero-glow gold hairline on focus.
  * **Preset & Library Ribbon Chips (.ribbon-chip)**: Standardized to 28px height, 12px font size, 999px geometry, max-width: 120px with ellipsis overflow, soft warm cream active text (#E6D5B8), subtle warm gold border (rgba(212, 175, 55, 0.28)), dark fill (rgba(212, 175, 55, 0.05)), and zero glow.
  * **Zero-Shift 102px Vertical Geometry Parity**: Unified Row 1 (36px search bar), 14px inter-row gap, Row 2 (32px ribbon), and 20px bottom margin identically across both Discover and Personal Library canvases for seamless view transitions.
- [x] **Material Symbols Poster Parity, Favourite Hearts Removal & Unified Pill Harmony**
  * **Material Symbols on Posters**: Standardized 22px poster corner badges to use the exact same Material Symbols glyphs (uto_awesome, check, schedule, 
eplay, lock) as the sidebar. Untracked movies receive no badge.
  * **Eradicated Favourites Hearts from Discover Posters**: Suppressed the uninformative ♥ favorite badge on movie posters in Discover mode while preserving it in Library views.
  * **Unified Zen Chip Harmony**: Standardized active Library Status and Sort chips to soft warm cream text (#E6D5B8), quiet muted gold border (
gba(212, 175, 55, 0.28)), and left alignment (justify-content: flex-start, padding: 0 12px, gap: 8px). Inactive glyphs recede in quiet grey (#6B7280), completely eliminating dark yellow chip blocks.
- [x] **Material Symbols Glyphs, Spacing Harmony & Dismiss Hover Bugfix**
  * **Material Symbols Glyphs**: Integrated self-hosted Material Symbols Outlined variable font (pp/static/fonts/MaterialSymbolsOutlined.woff2) for crisp, standardized typography across Sort Results (	rending_up, star, how_to_vote, schedule, history, sort_by_alpha) and Library Status (uto_awesome, schedule, check, 
eplay, lock, 
adio_button_unchecked).
  * **Muted Brand Yellow Everywhere & Left-Aligned Text**: Applied calm, desaturated muted brand yellow (#DEC68B active, #8E8468 inactive) across all chip glyphs, eradicating harsh saturated yellow. Standardized Sort and Library Status 50/50 pills to clean left-aligned layout (justify-content: flex-start, padding: 0 12px, gap: 8px) so all icons and text start at the exact same horizontal position.
  * **Zero Inner Glow Guarantee**: Ensured flat, glare-free aesthetic across all chips, pills, and active filter states (ox-shadow: none !important;).
  * **Hindi Dismiss Hover Bug Fix**: Resolved edge case in 
efreshCompactCloud where background excluded status prevented Hindi from receiving the chip-unpin (×) dismiss button on hover; all visible language chips now reliably display dismissal triggers.
- [x] **Zen Sidebar Palette, Tri-State Click Mechanics & Split-Contrast Pills**
  * **Desaturated Warm Zen Palette**: Replaced harsh neon yellow (`#FACC15`) and coral red (`#F87171`) with a warm, calm Zen palette: warm sand/ochre (`rgba(212, 175, 55, 0.06)` background, `rgba(212, 175, 55, 0.32)` border) and muted dusty rose/terracotta (`rgba(190, 80, 80, 0.06)` background, `rgba(190, 80, 80, 0.30)` border).
  * **3-State Click Cycle (Genres, Languages, Countries)**: Clicking cycles sequentially through State 0 (Neutral `#9CA3AF`), State 1 (Included `+` in warm gold), State 2 (Excluded `-` in dusty rose), and back to Neutral. Right-click or Alt-click jumps directly to Excluded in one click.
  * **Split-Contrast Pill Typography**: On `+ Crime`, `+` glyph renders in `#D4AF37` and the word in soft warm cream `#E6D5B8`. On `- Animation`, `-` glyph renders in `#D06B6B` and the word in soft dusty rose-grey `#D8A8A8`.
  * **Hover Dismissal for Countries & Languages**: Trimmed default display to core 10 countries and 8 languages, revealing a clean inline `×` on hover (`color: #9CA3AF`, hover `#CE8484`, no circular grey box) to unpin/dismiss chips.
  * **Muted Accordion Header Icons**: Changed category header icons (`⇅`, `📺`, etc.) to a subtle antique gold/grey (`#8E8468`), keeping the focus on active content.
  * **Zero Inner Glow & Consistent Library Status**: Removed all inset/box shadows across all sidebar chips. Standardized Library Status pills to the identical 28px height, 12px font, and 999px pill geometry.
  * **Search Profiles Uniformity & Ribbon Pinning**: Standardized Search Profile chips to the exact same 12px font size, 28px height, and 999px squircle/pill geometry as Languages and Themes. Restored the inline star pin button (`★`/`☆`) to pin/unpin profiles to the top ribbon, and replaced the oversized delete glyph with the standardized thin 13px `×` (U+00D7).
- [x] **Zen Design Refinements Batch: Header, Pagination, Badges, Scope & Toasts**
  * **Vertical Axis Alignment & Gap Tightening**: Synchronized topbar navigation with main content column on the exact same vertical x-axis. Shaved 18px of dead space out of the sidebar-to-canvas canyon, achieving a cohesive 24px visual gap.
  * **Icon-Only 22px Poster Badges (Task 14)**: Replaced wide all-caps text banners with compact 22px rounded-square frosted badges (✦, ✓, ↻, ◷, ✕) with distinct muted tones, preserving 100% of movie title art visibility.
  * **Pagination Zen & Legibility (Task 10)**: Bound pagination to universal 8px squircle geometry, increased top vertical separation gap to 38px, and elevated disabled "Previous" button opacity to 0.45 with clean hairline border.
  * **Floating Top-Right Toast & Preset Overflow (Task 11)**: Replaced disruptive full-width red notice box with a fixed floating toast sliding in from top-right with auto-dismiss. Capped preset ribbon chips at 115px with ellipsis so all 6 fit without clipping.
  * **Single Dynamic 2-State Library Scope (Task 16)**: Replaced 160px double-box with a compact squircle switch flipping between "In: This shelf" and "In: All shelves".
  * **Reversible 2-Way Favourites Toggle (Task 17)**: Converted Hall of Fame Heart button into a 2-way toggle that remembers previous shelf and returns with 1 click.
  * **Nope Mode Hotkey Alt+N (Task 13)**: Migrated off bare "X" key to deliberate Alt+N shortcut and removed clutter hint from the search placeholder.
  * **Grey Docked Responsive Grid Collapse (Task 20)**: Added responsive auto-fill and 4-column scaling for poster grid and canvas headers when Grey drawer is open on viewports under 1440px.


- [x] **Personal Library Floating Card Parity & Right-Aligned [Pages | Continuous] Toggle**
  * **Sidebar Card Parity**: Applied floating card envelope to .library-filters-workspace matching .discovery-workspace (16px border-radius, warm gold hairline border, dark translucent glass fill, and 12px 14px padding) eliminating layout shift.
  * **Right-Aligned Browse Mode with Generous Space**: Positioned [ Pages | Continuous ] at the far-right edge of the ribbon row (margin-left: auto), separated from the 5 status chips by a generous open gap of negative space, styled as a quiet 2-segment switch (#131317) to prevent visual mixing.
  * **Movie Counter Font Size**: Elevated top-right counter typography to 14px (var(--text-base)) for confident readability.

- [x] **UI & UX Zen Architecture: Squircle Geometry, Top-Right Telemetry & Canvas Parity**
  * **Universal 8px Squircle Geometry**: Retired puffy 999px hotdogs across Search Bar, Nope Mode toggle, Ribbon chips, Preset Action rows, Library modifier pills, and all sidebar filter chips (.tri-chip genres/languages, .sort-chip, .filter-chip, and .selected-entity pills).
  * **Top Bar Demarcation & Double-Wall Removal**: Elevated .topbar bottom border to subtle warm gold (rgba(242, 201, 76, 0.22)) and removed the sidebar's right divider (border-right: none), giving the left card space to breathe.
  * **Extreme Top-Right Telemetry & Font Harmony**: Bound search and Nope Mode to exact 670px 6-column grid width with Nope flush right, and positioned the movie counter at the extreme top right in open negative space with unified UI typography (var(--font-ui), var(--text-xs), #8e8b97).
  * **Eradicated 'Filtered Discovery' Headline**: Eradicated the giant 32px title; posters rise ~50px directly beneath the preset ribbon.
  * **Preset Action Rows Geometric Consistency**: Converted 'Update active preset' and 'Save current search as preset' to full-width 8px squircle action rows separated by 12px space, with quiet dashed border, uniform Regular 400 weight (12px), and 12x12px inline vector SVGs.
  * **Positive vs Negative Selection Tokens**: Preserved faded brand yellow (+, rgba(242, 201, 76, 0.75)) for positive inclusions and muted rose (−, #cf9b9e) for exclusions.
  * **Personal Library Zen Alignment**: Positioned Library search in top canvas with identical 36px squircle styling; relocated core personal shelves (New discovery, Watch later, Watched, Rewatch, Nope) into top ribbon; converted Favourites and Has Notes into a twin modifier strip ([ ★ Favourites only ] [ 📝 Has notes ]) at the top of the Library sidebar; removed duplicate bottom Sort accordion.

- [x] **Visual Separation & Counter Deduplication Fix**
  * **Warm Gold Borders**: Added subtle brand yellow / warm gold borders to the Left Sidebar (.discovery-workspace: rgba(242, 201, 76, 0.28)), the Search Bar (.toolbar-search: rgba(242, 201, 76, 0.3)), the Top Ribbon Pills (.ribbon-chip: rgba(242, 201, 76, 0.25)), and Nope Mode (.nope-mode-toggle: rgba(242, 201, 76, 0.25)), eliminating the pitch-black lack of separation.
  * **True Total Movie Count**: Resolved the 12/24 batch slice count by using the full TMDB/search total (response.tmdb_total_results || response.total_results), always displaying the true total number of movies.
  * **Counter Deduplication**: Suppressed the duplicate movie count in the top toolbar row (.discover-toolbar-row #result-count), leaving only the clean total counter next to [Pages | Continuous].

- [x] **Task 6: Movie Grid Spacing, Right-Edge Alignment & Centered Zen Pagination**
  * **Snapping Right Edge to 6th Column**: Bound .discover-canvas-header and .section-heading to max-width: 670px, snapping header controls ([Pages | Continuous] and movie count) cleanly to the right edge of the 6th poster column.
  * **Poster Grid Breathing Room**: Preserved the original compact Letterboxd poster scale (105px cards with 10px 8px gaps), aligning the canvas boundary to 670px.
  * **Hover Title Legibility Overlay**: Added smooth bottom gradient title/year overlay on hover (.movie-card:hover .card-copy) for instant readability on dark or stylized poster artwork.
  * **Centered Zen Pagination**: Centered pagination strip under the movie grid (max-width: 670px) with Option A active page pill (#161618 dark fill, muted gold border rgba(242,201,76,0.5), soft off-white text #f5f3ee, regular weight, 32px height) and quiet neutral inactive pills.

- [x] **Top Search Bar & Nope Mode: Zen Redesign**
  * **Top Search Bar**: Retired the bright yellow 'Search' button. The bar is now a clean, minimalist 36px pill with dark #141419 fill, subtle border (rgba(255, 255, 255, 0.08)), muted magnifying icon, and soft focus glow (rgba(242, 201, 76, 0.5)), smoothly triggered on Enter.
  * **Nope Mode Toggle**: Replaced the loud bright red box with a calm 36px Zen pill (#161618 dark fill, subtle neutral border rgba(255,255,255,0.08), muted grey text #9c9aa5, regular weight, with only the ✕ icon tinted in soft muted rose #cf9b9e). In active state, it engages a calm muted rose glow without pulsing strobe animations.

- [x] **Top Ribbon Preset Pills: Option A & Zen Philosophy Alignment**
  * Active preset ribbon chip (.ribbon-chip.is-active) now uses the Option A Zen formula: dark #161618 fill, muted gold border (rgba(242, 201, 76, 0.5)), soft off-white text (#f5f3ee), regular 400 weight, and subtle 8px ambient glow.
  * Inactive ribbon chips use dark #161618 fill, subtle border (rgba(255, 255, 255, 0.08)), muted silver/grey text (#9c9aa5), and regular 400 weight.

- [x] **Pure Zen Movie Counters: Eliminate Pagination Noise & De-Box Counts**
  * **No Pagination Arithmetic**: Eradicated all occurrences of '24 of 1,820 movies' and 'X movies on this page'. The counter now displays strictly the pure total count (e.g. '1,820 movies' or '687 movies').
  * **De-Boxed & Softened**: Removed pill borders and backgrounds from .result-count and .shelf-movie-count, rendering them as borderless, quiet dimmed text (#716e7a, 12px, regular weight).

- [x] **Sidebar Zen Mode: Selected Entity Pills, Uniform Input Heights & Preset Alignment**
  * **Selected Entity Pills (Keywords, Actors, Directors, Studios)**: Excluded entity pills now use the calm genre exclusion phenomenon (rgba(220, 100, 100, 0.08) fill, rgba(220, 100, 100, 0.22) border, soft muted rose text #cf9b9e, 60% opacity fade, no strikethrough). Included entity pills adopt Option A (#161618 dark fill, rgba(242, 201, 76, 0.5) gold border, #f5f3ee warm off-white text, muted + prefix at rgba(242, 201, 76, 0.68) with medium weight, subtle 8px gold glow). Dismissal × icon is quiet muted grey fading to red on hover; 'Clear all' link styled as a quiet, borderless 11px link.
  * **Uniform Input Heights Across Sidebar**: Standardized all sidebar text, number, and search data entry fields (Minimum Votes, Rating Min/Max, Release Year From/To, Keywords & Themes, Actors, Directors, Studios, and Library filter inputs) to a consistent 34px height (height: 34px !important; min-height: 34px !important; line-height: 32px; border-radius: 6px;). Suppressed default WebKit search clear/cancel adornments.
  * **Preset Action Links Left-Edge Alignment**: Shifted Update active preset and + Save current search as preset right (padding-left: 29px !important;) so their left edges (↻ and +) align directly under the letter 'A' of 'Atmospheric thrillers' in the preset pills above them.

- [x] **Phase 4 Implementation: Database, Storage & Memory Hygiene**
  * **Goal**: Enable persistent SQLite WAL mode and synchronous NORMAL, add performance indexes on high-frequency query paths, eliminate redundant schema PRAGMA checks inside hot read paths, enforce excluded movie metadata pruning, purge expired discovery/credits cache payloads, and cap client-side state objects to prevent memory leaks.
  * **Key Changes**:
    * **SQLite WAL & Synchronous Configuration ([`database.py`](file:///f:/Movie_Excluder/movie-excluder/app/database.py))**: Configured `PRAGMA journal_mode = WAL` and `PRAGMA synchronous = NORMAL` at startup in `initialize_database()` so WAL mode is persistent without re-executing PRAGMAs on every connection.
    * **Performance Indexes ([`database.py`](file:///f:/Movie_Excluder/movie-excluder/app/database.py))**: Added `idx_user_movie_status` on `user_movie_data(status, updated_at DESC)`, `idx_movie_keywords_keyword` on `movie_keywords(keyword_id)`, `idx_movie_genres_genre` on `movie_genres(tmdb_genre_id)`, and `idx_movie_credits_person` on `movie_credits(tmdb_person_id)`.
    * **Hot-Loop Optimization ([`user_movie_repository.py`](file:///f:/Movie_Excluder/movie-excluder/app/user_movie_repository.py))**: Removed dynamic `PRAGMA table_info(user_movie_data)` inspection from `get_user_movie_data_map`, querying `is_favorite` directly to eliminate redundant SQLite roundtrips during movie list loading.
    * **Storage Invariant & Excluded Metadata Pruning ([`movie_metadata_repository.py`](file:///f:/Movie_Excluder/movie-excluder/app/movie_metadata_repository.py), [`movie_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/movie_service.py), [`storage_repository.py`](file:///f:/Movie_Excluder/movie-excluder/app/storage_repository.py))**: Added `purge_movie_metadata(tmdb_id)` to remove cast/crew credits and official TMDB keywords when movies are marked excluded (`NOPE`). In `cleanup_old_cache(days)`, added automatic pruning of expired `tmdb_discover_cache` and `tmdb_person_credits_cache`, unreferenced `movie_country_cache`, and metadata for excluded movies.
    * **Bounded Client State & Memory Protection ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added LRU cache eviction capping `discoveryCache` at 40 pages and bounded `greyChatHistory` to the last 40 conversation turns.
    * **Full Verification**: Ran complete test suite (`python -m pytest`) with 220 passed in 46.27s (100% green).

- [x] **Typography Standardization & Design Token Consolidation**
  * **Goal**: Standardize fragmented font-sizes, font-weights, and letter-spacings into a cohesive design token system in `:root`, eliminate ad-hoc styles, fix microscopic poster badges, and unify sidebar action buttons.
  * **Key Changes**:
    * **Design Tokens ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Established unified semantic scales for type size (`--text-2xs` to `--text-3xl`), font weights (`--weight-regular` to `--weight-heavy`), and letter spacing (`--tracking-tighter` to `--tracking-widest`).
    * **Font Size & Tracking Consolidation ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Replaced 78 ad-hoc font-sizes and 24 letter-spacing values across the entire stylesheet with the semantic design tokens.
    * **Legibility & Action Consistency ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css), [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Increased microscopic poster badges from 0.47rem (~7.5px) to `--text-2xs` (0.65rem, ~10.4px); unified sidebar action buttons ("See results", "Update", "Reset", "Refresh") to a consistent `--text-sm` and `--weight-semibold`; replaced inline JS `ratingSpan.style.fontWeight = "700"` with `"var(--weight-bold)"`.
    * **Documentation ([`FONT_REPORT.md`](file:///f:/Movie_Excluder/movie-excluder/docs/FONT_REPORT.md))**: Updated typography audit summary verdict.

- [x] **Phase 3 Implementation: Strict Tier Boundary Enforcement & Async Non-Blocking Operations**
  * **Goal**: Enforce strict 3-tier separation (HTTP routes -> business logic services -> SQLite repositories), eliminate raw database queries leaking into HTTP routes and service layers, offload banner upload disk writes to non-blocking worker threads, and synchronize client-side mention cache with movie status mutations.
  * **Key Changes**:
    * **Repository Encapsulation ([`movie_repository.py`](file:///f:/Movie_Excluder/movie-excluder/app/movie_repository.py))**: Added `is_poster_excluded(filename)`, `find_in_discover_cache(tmdb_id)`, and `resolve_genre_names(genre_ids)` to encapsulate all SQLite database queries.
    * **Service Tier Delegation ([`movie_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/movie_service.py))**: Removed direct database connection instantiation and raw SQL from `MovieService`. Added `is_poster_caching_allowed(filename)` and delegated discover cache lookups and genre resolutions directly to `self.movie_repository`.
    * **Main Route Cleanliness & Non-Blocking Disk I/O ([`main.py`](file:///f:/Movie_Excluder/movie-excluder/app/main.py))**: Replaced raw SQL in `GET /images/posters/{filename}` with `movie_service.is_poster_caching_allowed(filename)` and removed unused `get_connection` import. In `POST /entries/upload-banner`, converted blocking `target_path.write_bytes(contents)` into non-blocking `await anyio.to_thread.run_sync(target_path.write_bytes, contents)`.
    * **Client-Side Mention Cache Synchronization ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added `updateMovieMentionCacheStatus(movieId, userData)` and capped `movieMentionCache` at the last 100 entries to prevent unbounded memory growth. Wired live mention cache updates into `updateMovieCardDOM`, `handleLiberateMovie`, and `handleNopeUndo`.
    * **Full Verification**: Ran complete test suite (`python -m pytest`) with 220 passed in 137.94s (100% green).

- [x] **Phase 2 Implementation: Vibe-Coding Remnants, Config Centralization & Swallowed Error Logging**
  * **Goal**: Centralize scattered configuration settings (TMDB base URLs, image hostnames, Gemini endpoints, default and fallback models, timeouts) and replace swallowed exceptions with structured diagnostic logging across backend and frontend.
  * **Key Changes**:
    * **Centralized Configuration ([`config.py`](file:///f:/Movie_Excluder/movie-excluder/app/config.py))**: Centralized `TMDB_BASE_URL`, `TMDB_IMAGE_BASE_URL`, `DEFAULT_REQUEST_TIMEOUT`, `GEMINI_API_BASE_URL`, `DEFAULT_FLASH_MODEL`, `DEFAULT_PRO_MODEL`, `GEMINI_PRO_CANDIDATE_MODELS`, and `GEMINI_FLASH_CANDIDATE_MODELS` with sensible environment variable fallbacks.
    * **Eliminated Silent Failures in TMDB Client ([`tmdb_client.py`](file:///f:/Movie_Excluder/movie-excluder/app/tmdb_client.py))**: Replaced 7 empty `except Exception: pass` blocks in cache query/write operations with structured `logger.debug()` logging and switched hardcoded `BASE_URL` to `TMDB_BASE_URL`.
    * **Centralized Poster & Image URLs ([`poster_cache_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/poster_cache_service.py), [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Updated image generation to source from `TMDB_IMAGE_BASE_URL` on the backend and normalized `TMDB_IMAGE_HOST` across thumbnail and hover cards in the frontend.
    * **Streamlined Gemini Endpoint & Cascade Fallbacks ([`grey/service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey/service.py))**: Replaced inline hardcoded model lists and endpoint URLs with the centralized config constants, and replaced bare exception swallows in SQLite context lookups with structured debug logging.
    * **Orphaned Asset Handling ([`storage_repository.py`](file:///f:/Movie_Excluder/movie-excluder/app/storage_repository.py))**: Added structured warning logging when banner unlinking fails during maintenance runs.
    * **Full Verification**: Ran complete test suite (`python -m pytest`) with 220 passed in 128.85s (100% green).

- [x] **Self-Hosted UI Fonts (Inter active; Manrope, Geist, Plus Jakarta Sans available)**
  * **Goal**: The stylesheet requested Inter but never loaded it, so Windows silently fell back to Segoe UI.
  * **Key Changes**:
    * **Bundled Variable Fonts (`app/static/fonts/`)**: Added `Inter-Variable.woff2`, `Manrope-Variable.woff2`, `Geist-Variable.woff2` and `PlusJakartaSans-Variable.woff2` (latin subset, full weight range) registered via `@font-face` at the top of [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css).
    * **Single Font Switch**: New `--font-ui` variable in `:root` drives the body font; swap `"Inter"` for `"Manrope"` to change the whole UI. Bumped stylesheet cache version in [`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html).

- [x] **Phase 1 Full Clean Purge: Dead Endpoints, Legacy Dependencies, Dead JS & Pruned CSS**
  * **Goal**: Strip all superseded legacy routes, unused Pydantic models, dead dependencies, orphaned keyword/default-profile logic, dead JS selectors/functions, and dead CSS rules while consolidating duplicate media queries.
  * **Key Changes**:
    * **Purged 9 Dead / Unused FastAPI Routes ([`main.py`](file:///f:/Movie_Excluder/movie-excluder/app/main.py))**: Deleted superseded legacy shelf endpoints (`GET /movies/watched`, `POST /movies/watched`, `GET /movies/status/{status}`, `GET /movies/notes`, `GET /movies/favorites`), the 4 uncalled custom keyword endpoints (`/movies/{tmdb_id}/keywords/custom`, `/keywords/custom/{keyword_id}`, etc.), and the unneeded default profile route (`PUT /search-preferences/{preference_id}/default`).
    * **Removed Obsolete Pydantic Schemas ([`main.py`](file:///f:/Movie_Excluder/movie-excluder/app/main.py))**: Deleted `WatchedRequest` and `CustomKeywordRequest`.
    * **Cleaned Dependency Manifest ([`requirements.txt`](file:///f:/Movie_Excluder/movie-excluder/requirements.txt))**: Purged 17 obsolete or transitive packages (Flask, Werkzeug, itsdangerous, blinker, Jinja2, MarkupSafe, pillow, Pygments, and pinned sub-dependencies), keeping strictly the 5 active top-level packages (`fastapi`, `uvicorn[standard]`, `requests`, `python-dotenv`, `pytest`).
    * **Fixed Broken JSON Library Export ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Corrected `#export-library-json` to fetch `/movies/library/search` instead of the non-existent `/movies/personal` route.
    * **Pruned Dead Frontend JS ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Removed unused helper functions `updatePickerSummary`, `formatReleaseDate`, `setupSidebarMasterToggle()`, and `renderActiveFilterTags()`. Removed dead DOM selector references and conditional checks (`#notes-search-container`, `#notes-search-input`, `#clear-notes-search`, `#reader-save-split`, `#reader-save-menu-toggle`, `#reader-save-dropdown`, `#grey-status-text`, `#badge-quality`, `#pill-quality`, `#active-filter-tags`, and `#active-entry-tag` cleanup check).
    * **Optimized & Pruned Stylesheet ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Removed 3 unused `:root` variables (`--bg-soft`, `--blue`, `--surface-high`) and 72 unreferenced CSS classes, shaving nearly 19 KB of dead styles while strictly preserving all 411 `!important` declarations. Consolidated duplicate `@media` blocks across all 6 breakpoint sets (`(max-width: 800px)`, `(max-width: 560px)`, `(max-width: 1100px)`, `(max-width: 760px)`, `(max-width: 860px)`, `(max-width: 620px)`) into single media queries while preserving cascade order.
    * **Synchronized Test Suite ([`tests/`](file:///f:/Movie_Excluder/movie-excluder/tests))**: Deleted obsolete `test_custom_keyword_endpoints.py`, removed legacy assertions in `test_movie_status_list_endpoint.py`, `test_favorite_endpoints.py`, `test_search_preference_endpoints.py`, and `test_web_ui.py`. All 220 tests across the entire test suite pass 100% green.

- [x] **Zero-Flash Lifecycle Fixes for Discover, Single Note Reader, and Movie Detail Page**
  * **Goal**: Eliminate initial page flash on refresh across the Discover page, Single Note Reader, and Single Movie Detail Page, and add deep-linked URL routing and persistent state memory for single movie pages.
  * **Key Changes**:
    * **Discover "Favourites" Title Flash Elimination ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html))**: Fixed [`setAuxiliaryView`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js#L2846-L2875) so `#section-heading-block` is only unhidden if the active view is truly an open library shelf (`isLibrary && state.mode !== "filmography"`), preventing `setEntriesVisible(false)` from accidentally revealing the heading on Discover. Cleared the hardcoded `"Favourites"` DOM placeholder in `<h2 id="library-title"></h2>` and removed static `is-active` from the Favourites shelf link in [`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html).
    * **Zero-Flash Single Note Reader Reload ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: In [`initializeApp`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js#L9832-L9865), when refreshing an `entry-reader` URL, bypassed the foreground `loadShelf("entries")` call. Now immediately sets auxiliary view to `"entry-reader"`, fetches the target note directly via `GET /entries/{id}`, and calls `openEntryReader(entry)` while loading background timeline and tags silently in parallel, completely eradicating the intermediate flash of the notes list stream.
    * **Movie Detail URL Routing & Persistent Refresh Memory ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added `#movie:${movieId}` URL hash synchronization in [`openMovieDetails`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js#L5254-L5295) and persistent tracking of the origin view and scroll coordinates. Added movie detail route handlers to [`initializeApp`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js#L9736-L9758) and the `hashchange` listener to seamlessly restore open films across F5 browser refreshes, and cleanly restore the origin shelf hash upon closing details.

- [x] **Completely Blackhole `Looking Out For` (UI + Logic + Backend) & Hide Filter Sidebar on `Storage` Page**
  * **Goal**: Completely remove the `Looking Out For` feature across UI, frontend JS, CSS, backend API, and SQLite schema, and hide the left filter sidebar (`#app-sidebar`) whenever viewing the `Storage` page.
  * **Key Changes**:
    * **End-to-End Removal of `Looking Out For` ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css), [`main.py`](file:///f:/Movie_Excluder/movie-excluder/app/main.py), [`movie_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/movie_service.py), [`movie_repository.py`](file:///f:/Movie_Excluder/movie-excluder/app/movie_repository.py), [`storage_repository.py`](file:///f:/Movie_Excluder/movie-excluder/app/storage_repository.py), [`database.py`](file:///f:/Movie_Excluder/movie-excluder/app/database.py))**: Removed `#looking-out-page`, the footer `Looking Out For` button + `#release-alert-badge`, `#looking-out-control` on the Single Movie Detail Page, `.looking-out-*` CSS rules, frontend handlers (`loadLookingOutFor`, `createLookingOutCard`, `updateReleaseAlerts`, `refreshReleaseAlertBadge`), the Storage stat card for `Looking Out For`, `/movies/looking-out-for` and `/settings/release-alerts` routes/service/repository methods, and dropped the `looking_out_for` table on startup.
    * **Full-Width `Storage` View Without Left Filter Sidebar ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Hid `#app-sidebar` and collapsed `.app-layout` to a centered single column (`margin: 0 auto`) whenever `#storage-page` is open, restoring `#app-sidebar` automatically when returning to `Discover`, `Personal Library`, or `Notes`.

- [x] **Quick Keyboard Triage on Movie Detail Page (`U`, `D`, `W`, `L`, `R`, `X`, `F`) & `Untracked` Dropdown Option**
  * **Goal**: Pair `←` / `→` movie navigation on `#movie-detail-page` with instant single-key shelf assignment and an explicit `Untracked (U)` option so movies (especially from the Excluded/Nope shelf in Continuous mode) can be untracked or sorted from the detail page.
  * **Key Changes**:
    * **`Untracked` Option & Single-Key Shelf Shortcuts ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html))**: Added `<option value="untracked">Untracked (U)</option>` to `#status-select` (wired to `DELETE /movies/{id}/status`) and added keyboard listeners on `#movie-detail-page` for **`U`** (`Untracked`), **`D`** (`New discovery`), **`W`** (`Watched`), **`L`** (`Watch later`), **`R`** (`Rewatch`), **`X`** (`Nope / Excluded`), and **`F`** (toggle `♥ Favourite`).

- [x] **Simple `@movie` Mentions in Notes, Grey Side-by-Side Note Reader Fix, & Looking Out For / Storage Polish**
  * **Goal**: Enable natural `@movie` linking inside notes (with live autocomplete, hover preview cards, and 1-click navigation to movie details), fix the `.entry-reader-toolbar` two-line collision when Grey is docked open, and polish the Looking Out For and Storage pages.
  * **Key Changes**:
    * **Simple `@movie` Mentions ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Typing `@` followed by a movie title in `#reader-body-input` opens `#reader-movie-mention-popover` with poster thumbnails, release years, and personal shelf badges; selecting a film inserts `@Movie Title (Year)` which renders in Read Mode as an interactive `.note-movie-mention` chip with a floating hover preview card and 1-click navigation to the movie detail page (`← Back to note`).
    * **Grey Side-by-Side Reader Toolbar Fix ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Removed the legacy `@media (max-width: 1280px) body.grey-docked-open .entry-reader-toolbar { flex-direction: column }` rule that caused the toolbar buttons to wrap onto the note headline, keeping the toolbar on a single `36px` horizontal line and compacting `Previous`/`Next` to icon chevrons on narrower split-screen viewports.
    * **Looking Out For & Storage Polish + 1-Click Exports ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Aligned `#looking-out-page` and `#storage-page` to a clean `820px` container with `object-fit: cover` poster cards, tabular storage stat cards, and 1-click **Export Notes (.md)** and **Export Library Snapshot (.json)** actions.

- [x] **Compact Circular `↑` Back-to-Top Button Next to Grey & Continuous/Notes-Only Visibility**
  * **Goal**: Eliminate the lopsided vertical totem-pole stacking of `^ Top` above `Grey` in the bottom-right corner and prevent `^ Top` from appearing on 24-movie Paged views (Discover, Watch Later, or shelves in `Pages` mode).
  * **Key Changes**:
    * **Horizontal Circular Icon (`[ ↑ ]  [ 🐱 Grey • ]`) ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Replaced the wide `^ Top` text pill with a `40×40px` circular upward-arrow icon button placed cleanly to the left of `Grey` on the same `bottom: 24px` row (`right: 146px`, shifting beside the docked drawer when Grey is open).
    * **Context-Aware Visibility ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added [`updateBackToTopVisibility`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js#L3086-L3106) so the button only appears when scrolled down (`scrollY > 380`) inside `Continuous` library shelves or when browsing/reading in Notes—staying hidden on Discover and all `Pages` views.

- [x] **Unified Numbered Pagination Across All Views & Exact 6-Column Grid Centering**
  * **Goal**: Standardize page numbering across every view in the app (Discover, Filtered Discovery, Title/Keyword Search, Personal Library Shelves, Movie Notes, Notes Cards, and Looking Out For) and center `#pagination` directly beneath the 6-column poster grid.
  * **Key Changes**:
    * **Unified Numbered Pagination ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Removed the separate `Page X` capsule variant so all views render the same numbered pagination bar (`‹ Previous   1  2  3 … N   Next ›`) with uniform `38px` button heights, symmetrical `106px` `Previous` / `Next` buttons, crisp SVG chevrons, and tabular page numbers.
    * **Exact 6-Column Poster Grid Centering ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Locked `#pagination` to `width: 100%; max-width: 670px; margin: 3.5rem 0 2rem` to match the exact `670px` width (`6 × 105px + 5 × 8px`) and left-alignment of `.movie-grid`, placing the center of the pagination bar dead-center between poster columns 3 and 4.

- [x] **Notion / Bear Style Debounced Auto-Save for Notes, `✓ Done` Mode Switch, & Inline `"✓ Saved"` Indicator**
  * **Goal**: Replace manual `Save` / `Cancel` buttons and the giant full-width `#notice` banner with debounced background auto-save, `Ctrl+S` muscle memory, a `✓ Done` button to return to Read Mode, a quiet `Move to Drafts` pill, and an inline `"Saving…" → "✓ Saved"` toolbar status indicator.
  * **Key Changes**:
    * **Debounced Auto-Save + `Ctrl+S` Muscle Memory ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Automatically saves title, body, tags, and banner changes ~750ms after pausing typing (plus instant in-place save on `Ctrl+S` without leaving Edit mode, and auto-flush when clicking `← Notes`).
    * **Inline Toolbar Status & Top Banner Removal ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Added `#reader-save-status` and `#reader-view-save-status` (`Saving…` → `✓ Saved`) directly in the toolbar, eliminating the full-width reddish `#notice` banner that previously pushed the page down by 60px.
    * **Removed Shortcut Hint ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html))**: Removed the `Tip: Press Ctrl + Enter to save` footer hint below the note textarea.

- [x] **Zero-Shift Single Note View (Read Mode vs. Edit Mode) & Notes Polish Batch**
  * **Goal**: Eliminate all layout jumping and shapeshifting when toggling between Read Mode and Edit Mode inside `#entry-reader` (modeled on [`zero_shift_note_editor_mockup_v2_1792772628276.jpg`](file:///C:/Users/Narasimha/.gemini/antigravity/brain/253ff604-4289-4fb0-89c6-082d7ea9ebbb/zero_shift_note_editor_mockup_v2_1792772628276.jpg)), plus complete the active Notes & Movie Detail UI polish items.
  * **Key Changes**:
    * **Zero-Shift Reader & Editor ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Locked the top toolbar to a fixed `36px` height with a pro-designer SVG `← Notes` back pill anchored on the left in both modes, segmented `[ ← Previous | Next → ]` stepper buttons, removed the redundant `#entry-reader-type` (`note`) label above the headline, unified `#entry-reader-title` and `#reader-title-input` typography/margins, matched the gold tag pills (`[ tag ]` vs `[ tag × ]`) and `26px` dashed `+ Tag` / `🖼️ Banner` controls, and locked the divider and body text/textarea to identical coordinates.
    * **Reader Keyboard Stepper ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added `ArrowLeft` and `ArrowRight` shortcuts inside `#entry-reader` (when not editing) to step to Previous and Next notes.
    * **List Mode Row Polish ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Fixed `.card-action-btn` opacity on `.entry-ledger-row:hover` so `📌`, `✎`, and `📥` fade in cleanly on row hover; removed the repetitive `edited` row badge and attached a hover/click timestamp tooltip on `.ledger-date` (`Created ... · Updated ...`); and added breathing room between `.entries-search-bar` and `#entry-active-filters`.
    * **Personal Memory Header Alignment ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Vertically aligned `#notes-feedback` with the `"Minimize"` button and simplified the save confirmation copy to `"Note saved"`.

- [x] **Banner-Less / High-Density Compact View for Notes & Journal + Footer & Storage Cleanups**
  * **Goal**: Prevent archive browsing exhaustion as notes and journal entries grow in number by introducing a high-density, banner-less chronological index stream with simple year-wise navigation, plus clean up legacy "Notes & Links" storage wording and redundant footer buttons.
  * **Key Changes**:
    * **Banner-Less Chronological Index ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css), [`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html))**: Added `#notes-view-switcher` (`[ ≡ List | ☷ Cards ]`, defaulting to `List`). List view renders single-line typographic rows (`Pin · Short Date • Bold Title + subtle edited badge · Tag Pills`) inside a 920px column container with zero reading-time/word-count clutter and pagination-free continuous timeline streaming.
    * **Historical Date Anchoring ([`general_entry_repository.py`](file:///f:/Movie_Excluder/movie-excluder/app/general_entry_repository.py), [`main.py`](file:///f:/Movie_Excluder/movie-excluder/app/main.py))**: Anchored `GET /entries` and timeline summary aggregations to `created_at` so editing an older note never teleports it out of its original `YYYY · MONTH` chapter.
    * **Collapsible Year-Wise & Month-Wise Sidebar ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Grouped sidebar timeline filters under collapsible year headers (`▾ 2026 (13)`) supporting 1-click full-year filtering or individual month drill-down, paired with instant filter breadcrumb chips (`#entry-active-filters`).
    * **Hover-Only Action Tray & Writer Keyboard Shortcuts ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Row actions (`📌`, `✎`, `📥`) remain invisible until row hover/focus; added keyboard navigation (`j`/`k` or `ArrowDown`/`ArrowUp`, `Enter` to open, `n` for new note, `Escape` to close reader or clear filters) and exact scroll restoration when returning from the reader.
    * **Storage & Footer Cleanup ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`test_web_ui.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_web_ui.py))**: Updated `#purge-deleted-entries` button to `"Permanently delete notes"` (removing legacy `"& Links"` phrasing) and removed redundant `Notes` and `Movie Notes` links from the bottom footer bar.

- [x] **Library Infinite Scroll Toggle (Excluding Watch Later)**
  * **Goal**: Provide an optional user toggle across the library shelves to seamlessly switch between standard pagination and continuous infinite movie poster scrolling, keeping pagination as the default mode and strictly preserving pagination on Watch Later.
  * **Key Changes**:
    * **Toggle Switch ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Added `#shelf-view-toggle` (`Pages` / `Continuous`) next to `#shelf-count`. Default is always `Pages`. Watch Later is strictly excluded by deliberation (toggle automatically hides and forces paged mode).
    * **Continuous Batch Engine & Silent Hairline Dividers ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Lightweight `IntersectionObserver` dynamically appends subsequent 30-movie batches separated by a text-free gradient hairline rule (`.continuous-batch-divider`) spanning across the grid.
    * **Floating "Back to Top" Pill ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css), [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added `#back-to-top-btn` that smoothly reveals when scrolling down, supporting both 1-click smooth glide and keyboard shortcuts (`Home` or `t`). Vertically stacked cleanly above the Grey pill (`bottom: 78px; right: 24px`) to prevent any icon collision.
    * **Shelf Coverage**: Supported across Watched, Rewatch, Favorites, Excluded (Nope), New Discoveries, and Movie Notes. Navigation to/from movie detail pages preserves exact scroll position and all loaded batches.

- [x] **Debounced Auto-Save for Personal Memory & Manual Save Button Removal**
  * **Goal**: Upgrade the single movie detail page's "Personal Memory" note editor to automatically save thoughts as you type (debounced) and on blur/navigation, eliminating the manual "Save notes" button and accidental loss of notes.
  * **Key Changes**:
    * **Debounced Auto-Save ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Triggers auto-save ~750ms after user pauses typing, with instant save on textarea blur, detail navigation (prev/next/close/back-to-origin), or `Ctrl+S`.
    * **Header Status Micro-Indicator ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css), [`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html))**: Removed the manual `#save-notes` button. Added quiet inline status indicator (`Saving…` → `✓ Saved`) directly next to *Minimize* in the Personal Memory header.

- [x] **Persistent Grey Chat Memory & Live Personal Memory Integration**
  * **Goal**: Expand Grey's conversational memory window, remove artificial midnight session wipes, and bridge live movie notes directly into Grey's prompt for seamless, contextual to-and-fro.
  * **Key Changes**:
    * **Expanded Turn Window ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py))**: Increased conversational history from 6 to 16 messages (8 back-and-forth exchanges) in backend prompt generation and client chat payloads.
    * **Multi-Day Session Persistence ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Removed calendar date reset check from `loadGreyDailySession`, preserving conversations across days until explicitly cleared.
    * **Live Note Context Bridging ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`main.py`](file:///f:/Movie_Excluder/movie-excluder/app/main.py), [`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py))**: Provided `live_movie_notes` in `/grey/chat` schema, auto-flushed unsaved drafts on send, and prioritized live text in Grey's inspected movie prompt context.

- [x] **Removal of `/watchlist` Chip and Watchlist Builder Skill**
  * **Goal**: Completely remove the `📝 /watchlist` quick action chip and strip out the artificial `/watchlist` (Toggle Watchlist Builder) skill module from Grey, eliminating clutter and keeping Grey focused on sharp recommendations and research.
  * **Key Changes**:
    * **UI Quick Skills Bar ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html))**: Removed `📝 /watchlist` button from `#grey-skills-bar` and slash command suggestions.
    * **Backend Skill Cleanup ([`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py))**: Removed `watchlist` skill handler and routing table entries.

- [x] **Eliminate Redundant Context Strip Subtitles ("Personal observations", etc.)**
  * **Goal**: Remove obvious, patronizing filler subtitles from Grey's top context strip, keeping headers punchy, minimal, and informative.
  * **Key Changes**:
    * **Context Subtitle Cleanup ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Dropped `"Personal observations"` when viewing Notes without tag filters, `"Browsing new titles"` in Discover, and `"All shelves"` in Movie Notes. Added `.grey-context-detail:empty { display: none; }` to collapse empty badges cleanly.

- [x] **Movie Detail Full-Width Topbar, Hover Popover Polish, & Discover Spacing**
  * **Goal**: Modernize the top navigation of the single movie detail page into a full-width edge-to-edge bar, polish the movie card notes hover popover with prominent brand-yellow title typography, close baseline spacing with rating/votes, ensure top-only positioning and adaptive width, eliminate redundant personal keywords UI, and optimize sidebar top padding.
  * **Key Changes**:
    * **Full-Width Header ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Extended the frosted-glass header edge-to-edge (100% width) across the single movie detail page with sticky positioning, centered 1080px content grid, and 24px side gutters.
    * **Hover Popover Polish ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Removed redundant `📝 Note` badge, styled movie titles prominently in NOPE brand accent yellow (`#f2c94c`), placed rating and vote count immediately adjacent with a cohesive 10px baseline gap, removed raw notes duplication from native browser tooltips, enforced strict top-only positioning, and enabled responsive width expansion (up to 400px) for longer notes.
    * **Personal Keywords Cleanup ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`test_web_ui.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_web_ui.py))**: Removed the `(+)` toggle button, input form, and feedback line under the movie poster, keeping official TMDB keywords as clean read-only badges.
    * **Discover Sidebar Padding ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Collapsed stacked top margins/padding across `.discovery-workspace`, `#workspace-controls`, and `.advanced-controls` to eliminate the 46px void above the "See results" button.

- [x] **Breathing Space for Personal Memory Saved Feedback**
  * **Goal**: Provide comfortable vertical spacing between the "Save notes" button and the "Personal memory saved." confirmation text in the movie details panel.
  * **Key Changes**:
    * **Detail Notes CSS ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Added `margin-top: 0.65rem` to `#notes-feedback` and collapsed empty feedback nodes (`:empty { display: none; }`) so confirmation text has breathing space beneath the button without causing awkward whitespace when idle.

- [x] **Native Markdown Table Support in Notes & Grey Table Formatting**
  * **Goal**: Support standard Markdown tables (`| Col 1 | Col 2 |`) in notes, journal posts, and Grey chat with dark-theme styling, and teach Grey to format and update movie comparison tables.
  * **Key Changes**:
    * **Markdown Table Parser ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added `tryRenderMarkdownTable` to parse pipe-delimited table rows, separator rows with alignments (`:---:`, `---:`, `:---`), and body rows into structured `<table>`, `<thead>`, `<tbody>` elements with support for inline links, bold text, and formatting inside both `appendEntryBody` and `appendGreyMessage`.
    * **Modern Dark CSS ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Added responsive `.note-table-wrap` with horizontal scroll for narrow screens, subtle borders, muted headers (`#f3f4f6`), comfortable cell padding, and dark theme hover highlights.
    * **Grey Skill Integration ([`notes_editor.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/notes_editor.md))**: Taught Grey to format side-by-side film comparisons, matrix breakdowns, and ranking lists as clean Markdown tables, and to extract and append new films as matching rows when a note already contains a table.

- [x] **Minimalist Confirmation for "Grey It" / Note Appends**
  * **Goal**: Replace the verbose echo of the entire critique block upon saving with a clean, punchy acknowledgment like `"Greyed it."`.
  * **Key Changes**:
    * **Succinct Acknowledgment ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Updated `saveGreyToMovieNotes` so Grey replies with `"Greyed it."` instead of dumping the entire multi-line critique block into the drawer, eliminating repetitive clutter.

- [x] **Save Grey's Critique to Movie Notes (`grey says`, `g says`, `grey it` & Quick Pill)**
  * **Goal**: Seamlessly save Grey's sharp film suggestion/critique directly into that movie's notes on single movie pages via conversational triggers or a quick action pill, preserving existing notes and appending cleanly below.
  * **Key Changes**:
    * **Trigger & Pill Handler ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added regex triggers for `grey says`, `g says`, `grey it` (with optional colons/punctuation) and attached a `[ 📝 Save to Movie Notes ]` pill to Grey's critique responses.
    * **Clean Append Formatting**: Emits formatted note starting with `Grey says:\nTitle (Year) [Genre 1, Genre 2]\n<critique>`. If notes already exist, appends to the bottom separated by a clean blank line (`\n\n`) without ever overwriting prior personal notes.
    * **Immediate Sync**: Saves directly via `PUT /movies/{tmdb_id}/notes`, updates the `#movie-notes` textarea, updates discovery cache, and gives instant visual feedback.

- [x] **Multi-Keyword Comma-Separated Notes Search**
  * **Goal**: Allow multi-term comma-separated queries like `grey says, horror` or `scorsese, crime` that check note bodies, movie titles, and genre tags together using `AND` matching logic.
  * **Key Changes**:
    * **Database Repository ([`user_movie_repository.py`](file:///f:/Movie_Excluder/movie-excluder/app/user_movie_repository.py))**: Extended `search_notes()` to split by comma and build combined SQL clauses matching `u.notes`, `m.title`, or `EXISTS (SELECT 1 FROM movie_genres mg JOIN genres g ON mg.tmdb_genre_id = g.tmdb_genre_id WHERE mg.tmdb_id = u.tmdb_id AND g.name LIKE ...)`.
    * **Super Advanced Search Service ([`super_advanced_search_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/super_advanced_search_service.py))**: Validates comma-separated `notes_query` terms and ensures candidate movies match each term across note text, titles, or genre definitions.
    * **Unit Tests ([`test_movie_notes.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_movie_notes.py), [`test_super_advanced_search_service.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_super_advanced_search_service.py))**: Added comprehensive unit test coverage for comma-separated term searches across notes and genres.

- [x] **GIF Frequency Cooldown & Zero-Clutter Quiet Mode**
  * **Goal**: Eliminate reaction GIF fatigue by enforcing a minimum 4-turn spacing between reaction media, and provide a prompt/command-driven quiet mode for the session with zero UI clutter.
  * **Key Changes**:
    * **Turn Cooldown Counter ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Tracks conversational turns in memory (`state.greyTurnsSinceReaction`), enforcing a minimum 4-turn cooldown between any visual media reactions.
    * **Conversational Quiet Commands ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added prompt commands (`no gifs`, `no gifs this session`, `quiet mode`, `/quiet`, `/focus`) to mute reaction media for the active session, with `gifs ok`, `reset session`, or `/normal` to re-enable.

- [x] **Suppress Unsolicited Shelf Categorization Chips (`+ Add to Watchlist`, `✨ New Discovery`)**
  * **Goal**: Prevent Grey from generating unsolicited shelf action chips/pills below movie critiques so users categorize films manually.
  * **Key Changes**:
    * **System Prompt Updates ([`grey_system_prompt.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/grey_system_prompt.md), [`grey_core.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/grey_core.md))**: Added explicit instructions forbidding AI-generated shelf categorization chips (`+ Add to Watchlist`, `✨ New Discovery`, etc.).
    * **Backend Pill Sanitization ([`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py))**: Strips any status-changing action pills from the response payload before returning to the frontend.

- [x] **Keyboard Scrolling on Single Movie View**
  * **Goal**: Enable keyboard scrolling (`ArrowUp`, `ArrowDown`, `PageUp`, `PageDown`, `Space`, `Home`, `End`) when viewing the single movie detail page.
  * **Key Changes**:
    * **Focusable Viewport ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html))**: Added `tabindex="-1"` to `#movie-detail-page`.
    * **Global Keyboard Listener ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Intercepts navigation keys when the single movie page is open and active focus is not inside an input/textarea, scrolling the detail page smoothly in both full-screen and docked Grey panel layouts.

- [x] **Contextual Reaction Media & Hybrid Context Index (`assets/gifs_n_media/*`)**
  * **Goal**: Enable Grey to deliver contextual reaction GIFs and transparent stickers with semantic accuracy using a local `reactions.json` file and automatic filename fallback.
  * **Key Changes**:
    * **Static Route Mount ([`main.py`](file:///f:/Movie_Excluder/movie-excluder/app/main.py))**: Mounted `/assets` pointing directly to `assets/gifs_n_media/` for zero-lag local browser image delivery.
    * **Dynamic Media Scanner & Fallback Reader ([`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py))**: `get_reactions_index()` parses `assets/gifs_n_media/reactions.json` when present, or cleanly infers context from filenames for unlisted media.
    * **Curated Reaction Index ([`reactions.json`](file:///f:/Movie_Excluder/movie-excluder/assets/gifs_n_media/reactions.json))**: Configured cinema context for all active GIFs (e.g., Scorsese/masterpiece for `absolute-cinema`, De Niro approval, Cillian Murphy deadpan comedy, Apollo 13 sci-fi disaster, sleepy snoozefest, and mobster cat).
    * **Chatbox Renderer ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js) & [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Rendered and styled reaction media within message bubbles, persisting across daily sessions.
    * **Unit Tests ([`test_grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_grey_service.py))**: Added comprehensive test coverage for indexing, fallback handling, and sanitized reaction delivery (25/25 passing).

- [x] **Minimalist Grey Cat Face Icon for Grey**
  * **Goal**: Replace the paw prints (`🐾`) in Grey's launcher pill and drawer header with a clean, vector cat face featuring sharp ears, sleek eyes, nose, and whiskers in a subtle grey tone.
  * **Key Changes**:
    * **Vector Cat Face Icon ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html))**: Swapped emoji paws in `.grey-pill-icon` and `.grey-avatar` for a crisp inline SVG cat face.
    * **Dark Theme Styling ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Styled with `currentColor` and muted grey tones (`#9ca3af` / `#b0b8c4`) that brighten on hover.

- [x] **Vote Count Tooltips on Discover Movie Posters & Badges**
  * **Goal**: Show the number of votes when hovering over movie posters in Discover mode, exactly like the existing Related Movies cards.
  * **Key Changes**:
    * **Poster Card Tooltip ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: In `createMovieCard`, formatted `posterButton.title` to include `• (${voteCountStr})` using the existing `formatVoteCount(movie.vote_count)` helper, displaying e.g. `Upgrade (2018) • (4.2k votes)`.
    * **Rating Badge Tooltip ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Attached a descriptive title to `.card-rating` (e.g. `★ 7.5 (4.2k votes)`) so hovering over the bottom-right score directly reveals total vote volume.

- [x] **Grey Note Editing: Exact Library Matching, Literal Format Precedence & Toggle Deduplication**
  * **Goal**: Ensure Grey respects literal formatting constraints (such as "as it is" or "raw text" overriding format mimicry), strictly resolves movies against existing library records instead of external/newer releases, and eliminates duplicate entries by properly replacing existing toggles/headings.
  * **Key Changes**:
    * **Literal Format Precedence ([`notes_editor.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/notes_editor.md))**: Added Rule 0 setting explicit prompt priority so instructions like "as it is", "raw", "verbatim", or "without toggles" override automatic format mimicry.
    * **Strict Library Record Lookup ([`grey_core.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/grey_core.md) & [`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py))**: Upgraded candidate title resolution and library search to match singular/plural stems and normalized titles directly against stored `user_movie_data` / `movies` records, preventing external title/year hallucinations.
    * **Universal In-Place Deduplication ([`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py))**: Extended `_deduplicate_and_format_note_body` to match existing entries formatted as Notion toggles (`>> Title`), Markdown headings (`### Title`), or numbered items, and normalize titles (stripping leading articles and years) so variations match and replace cleanly in-place with zero duplicate appends.
    * **Unit Tests ([`test_grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_grey_service.py))**: Added comprehensive test coverage for in-place toggle replacement and raw format precedence; full test suite passes (236/236).

- [x] **Ctrl+E Keyboard Shortcut to Enter Edit Mode**
  * **Goal**: Support standard `Ctrl+E` / `Cmd+E` (and `E` while reading) keyboard shortcuts to transition directly into edit mode without requiring mouse clicks.
  * **Key Changes**:
    * **Journal Reader ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added window `keydown` listeners for `Ctrl+E` / `Cmd+E` and single-key `E` when viewing a post to immediately switch the reader into edit mode.
    * **Movie Memory Notes ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added `Ctrl+E` handling when viewing movie details to open the memory panel and focus the textarea.
    * **Action Tooltip ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html))**: Added shortcut indicator to the Edit button tooltip.

- [x] **Ctrl+S Keyboard Shortcut to Save Posts After Edit**
  * **Goal**: Support standard `Ctrl+S` / `Cmd+S` keyboard shortcuts to save changes when editing journal posts, drafts, and movie memory notes without triggering the browser's default "Save Page As" dialog.
  * **Key Changes**:
    * **Post / Journal Reader Editor ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added `Ctrl+S` / `Cmd+S` listeners across reader inputs (`readerTitleInput`, `readerBodyInput`, `readerTagInput`) and window-level listener during active edit mode (`state.readerEditing`) to save the post retaining its status (`published` or `draft`).
    * **Movie Memory Notes ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Added `Ctrl+S` / `Cmd+S` listener to the movie memory notes textarea (`#movie-notes`) calling `saveSelectedNotes()`.
    * **Action Tooltips ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html))**: Added shortcut hints to save/publish buttons.


- [x] **File-Based Research Partner & Clean Conversational Workflow (`data/research/*.md`)**
  * **Goal**: Enable direct file-based research storage in `data/research/*.md` accessible in VS Code, with zero UI clutter, automatic dynamic disk indexing, and conversational file commands.
  * **Key Changes**:
    * **Zero UI Clutter**: Completely removed drawer header buttons, modal overlays, session badges, and research chips from [`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css), and [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js).
    * **File-Based Research Directory (`data/research/`)**: Stored as clean, editable `.md` files that can be edited or deleted directly in VS Code / File Explorer.
    * **Dynamic Disk Indexer ([`grey_service.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_service.py))**: Real-time `Path("data/research").glob("*.md")` scanning on every prompt. Index updates instantly when files are created, renamed, or deleted outside the app.
    * **Lean Research Partner Skill ([`research_partner.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/research_partner.md))**: Replaced complex database session logic with concise instructions for `save_research_file`, `append_research_file`, `delete_research_file`, and conversational indexing via `{{RESEARCH_FILES_INDEX}}`.
    * **Comprehensive Verification ([`test_grey_research_sessions.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_grey_research_sessions.py))**: Verified all operations and edge cases; full test suite passes (234/234).

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

- [x] **Grey Research Mode: Saved Sessions, On-the-Fly Appends, and Interactive Index**
  * **Goal**: Support dedicated, opt-in cinema research topics where conversations can be frozen into investigations, new discoveries appended on the fly without breaking browsing flow, and topics reviewed via an interactive Index.
  * **Architecture & Layering**:
    * **Database Schema ([`database.py`](file:///f:/Movie_Excluder/movie-excluder/app/database.py))**: Added `grey_research_sessions` table (`id`, `title`, `description`, `messages_json`, `created_at`, `updated_at`) with indexed `updated_at`.
    * **Repository ([`grey_research_repository.py`](file:///f:/Movie_Excluder/movie-excluder/app/grey_research_repository.py))**: Clean query layer for session creation, retrieval, fuzzy title matching, appending discoveries, and deletion.
    * **Skill Module & Prompt ([`research_partner.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/skills/research_partner.md), [`grey_core.md`](file:///f:/Movie_Excluder/movie-excluder/app/prompts/grey_core.md))**: Taught Grey how to freeze sessions (`save_research_session`), append discoveries (`append_research_session`), output conversational index lists from `{{RESEARCH_SESSIONS_INDEX}}`, and synthesize findings into notes.
    * **FastAPI Routes ([`main.py`](file:///f:/Movie_Excluder/movie-excluder/app/main.py))**: Registered endpoints for listing, fetching, creating, appending, and deleting research sessions.
    * **Frontend UI ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js), [`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html), [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - `📌 Save Current Chat` and `📑 Index` buttons in Grey drawer header.
      - Active research session badge with one-click exit back to General Chat.
      - Sleek, backdrop-blurred Research Index overlay displaying session titles, entry counts, and delete actions.
      - Automatic background appending to active research topics.
    * **Unit Tests ([`test_grey_research_sessions.py`](file:///f:/Movie_Excluder/movie-excluder/tests/test_grey_research_sessions.py))**: Comprehensive test coverage across repository, endpoints, and skill routing; all 235 tests pass.

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

### AG. UI/UX Zen Redesign: Poster Badges, Typography De-Thickening & Sidebar Mechanics (done — Oct 24)
* **Poster Badge Zen & Scale Fix**: Eliminated untracked badges; fully suppressed status badges and favorite marks inside personal library shelves (`#movie-grid:not([data-view="discover"]) .status-badge`, `[data-view="favorites"] .favorite-mark`) for clean poster walls. Discover cards feature dark high-contrast badges (`rgba(10, 10, 14, 0.90)`), soft drop-shadows, off-white text, and non-clipping labels.
* **Category Label Halation & Glare Elimination**: Replaced bold stark-white category headers (`#ffffff`, 700) with Regular (`400`) muted silver (`#9c9aa5`) with `+0.015em` letter-spacing. Active/open headers step to Medium (`500`) in warm off-white (`#f5f3ee`), eliminating halation bloom.
* **Inverted Input Scale Fixed**: De-escalated numeric inputs (Rating, Minimum Votes, Release Year) to Regular (`400`), `12px` (`--text-xs`), and muted `#c5c2cb` with compact `32px` heights, restoring parent title dominance.
* **Native Number Steppers Removed**: Stripped visual spinner arrows across number inputs (`appearance: textfield`) while preserving physical keyboard Up/Down arrow nudging.
* **3-State Click (Exclude First) & Quiet Red**: Replaced clumsy mode switches with direct 3-state cycling (1st click = Exclude, 2nd click = Include, 3rd click = Off). Excluded pills recede at 60% opacity with soft maroon borders and no strikethrough.
* **Balanced Sidebar Header Row**: Restored dim uppercase `FILTERS` micro-label on the left to symmetrically balance `↺ Reset` on the right below the full-width `See results` button.
* **Sort Results 50/50 Grid**: Formatted sidebar sort drawer into an even 2-column grid (`grid-template-columns: 1fr 1fr`), removing jagged text-length edges.
* **Sort Results Promoted to Top**: Slid Sort Results out of the #4 middle spot to the very top of the accordion (above Genres), cleanly separating output ordering from data filters.
* **True Dirty State for 'See results'**: 'See results' remains calm neutral grey on initial load and reset, only illuminating in warm gold when the user actively modifies a filter.
* **Search Profiles Zen Redesign**: Consolidated split ribbon/reserve areas into a single `SAVED PRESETS` cloud without dead void gaps. Removed star icons (`★` / `☆`), highlighted active presets in warm gold, and replaced crowded buttons with a quiet `+ Save current search as preset` link.
* **Empty Entity Drawer Collapse**: Added zero-height collapse for empty `.selected-entities:empty` containers, removing dead black voids below the keywords input box.
* **Clean Range Inputs & Minimal Placeholders**: Restored dark `#141419` backgrounds, `6px` radius, and subtle gold focus rings to Rating and Release Year boxes. Eliminated tutorial chatter in placeholders (`From (e.g. 1990)` -> `1990` - `2024`, `6.0` - `10.0`, `500`).
* **Removed Redundant Sub-Header Row**: Eradicated `SAVED PRESETS / 4/6` inside the Search Profiles drawer; first preset pill now breathes with a clean 10px top gap.
* **Strict Dirty-Only Preset Update**: `↻ Update "Preset"` remains completely hidden until a filter is actively changed; tight 8px gap between action links.
* **Universal Option A Pill Styling**: Applied Option A (dark `#161618` fill, soft off-white `#f5f3ee` text, muted gold border `rgba(242, 201, 76, 0.5)`, regular weight) universally across all sidebar selection pills (Genres, Languages, Sort Results, Countries, Presets, Library Statuses), eliminating muddy yellow fills and swollen text.
* **Same-Line Paired Inputs**: Forced `sidebar-range-row` into a non-wrapping flex row (`flex-wrap: nowrap`, 50/50 input sizing), locking Min – Max Rating and From – To Year boxes on a single horizontal line with a centered dash.
* **Symmetrical 2x3 Library Status Grid**: Moved `Untracked` directly into the status pill group as the 6th pill in a balanced 2-column x 3-row grid, eradicating the awkward dashed-border checkbox.
* **Minimalist Vector Pin & Hover Delete**: Replaced red OS emoji pushpins with sleek inline vector SVGs (pinned in warm gold, unpinned in subtle stroke). Preset deletion `✕` is now completely hidden until hovering over a row.
* **Tight Left-Aligned Action Links**: Reduced spacing between `↻ Update` and `+ Save` to 8px and aligned both flush against the left boundary under the preset pills.
* **Separated Ribbon Pin vs Preset Delete**: Each preset chip in `SAVED PRESETS` now provides an explicit `📌` icon to toggle ribbon pinning and a distinct `✕` icon to permanently delete the preset.
* **Left-Aligned '+ Save' Text Action**: Replaced the centered dashed box with a clean, left-aligned plain text link directly beneath the presets.

---

*Last Updated: October 24, 2026*


- **UI/UX Zen Shelf Ribbon & Icons**: Embedded crisp vector SVGs in front of Personal Library shelf status chips and right-aligned `[ Pages | Continuous ]` toggle with generous negative space and 8px squircle styling.

- **UI/UX Zen Favourites Heart & Nope Hotkey**: Replaced shelf view toggle with a dedicated Favourites Heart button on the library ribbon; decoupled Nope Mode from the Discover search bar to prevent submit-button confusion, replacing it with an instant `X` / `Escape` keyboard shortcut and floating status banner.

### AH. UI/UX Zen: Unified Canvas Geometry, Zero-Shift Transitions & Preset Ribbon Polish (done — Oct 25)
* **Unified 670px Canvas Search Geometry**: Embedded the Library search scope switch (`[ ◫ This shelf ]` ⇄ `[ ☷ All shelves ]`) directly inside the right edge of the Library search bar as a quiet 24px frosted squircle pill. Discover and Library search inputs now share identical 670px outer bounding boxes with zero width shift.
* **Unchoked Preset Ribbon Chips**: Expanded preset chip `max-width` from artificial 115px choke to 220px with natural content expansion (`flex: 0 0 auto`), allowing preset titles (e.g. *The current best sci-fi*, *Atmospheric thrillers*, *new search filter test*) to display fully without premature ellipsis cutting off text. Added hover title tooltips to all preset chips.
* **Locked 32px Ribbon Height & 28px Chips**: Synchronized `.profile-ribbon` and `.library-shelf-ribbon` to exact identical `32px` container height and `28px` chip height (`gap: 8px`), eliminating vertical layout jitter when toggling tabs.
* **Pixel-Locked Poster Grid Origin**: Locked total canvas header height (`36px` search + `14px` gap + `32px` ribbon + `20px` bottom margin = `102px`) across both Discover and Library tabs, guaranteeing that Row 1 of the poster grid (`#movie-grid`) starts at the exact same pixel in both views with zero vertical jump. Permanently disabled legacy `.section-heading` element.

* **Standardized Poster Overlay Badges**: Unified all 4 poster overlay corners (Top-Left Status, Top-Right Favourite Heart, Bottom-Left Note, Bottom-Right Rating) to use the exact same dark glassmorphism container: `background: rgba(10, 10, 12, 0.88)`, `border: 1px solid rgba(255, 255, 255, 0.14)`, and `backdrop-filter: blur(4px)` with matched 22px heights and 6px border radii.
* **Status Icon Weight & Color Contrast**: Differentiated library statuses via high-contrast icon hues and matched visual weights; upgraded Watched status to a dedicated `#4ADE80` checkmark with heavy `2.5px` stroke-width to perfectly balance the filled Discovery star and Favourite heart. Upgraded Note badge to a vector SVG.
* **Library Scope Toggle Visibility Restored**: Fixed `.toolbar-search button` rule that was suppressing `#library-scope-toggle` when placed within the search bar form; the `[ ◫ This shelf ]` pill now displays clearly inside the right side of the search input.

* **Unification of 3 Vertical Alignment Axes & Pagination Breathing Room**:
  - **Inner-Left Sidebar Axis**: Nudged top header "NOPE" logo and bottom footer "NOPE" identity block with `15px` left inset to sit on the exact same vertical x-axis as the sidebar card's inner content edge (the left edge of "See results", "FILTERS", and accordion filter icons).
  - **Main Content Left Axis**: Aligned footer navigation (`.footer-nav`) in a matched 2-column grid (`padding-left: 16px`) so the left edge of "Storage" and "API" locks directly onto the exact same vertical x-axis as top navigation tabs (DISCOVER, LIBRARY, NOTES), Search Bar, Ribbon row, and Poster Column 1.
  - **Far-Right Viewport Axis**: Synchronized the right margin of the top movie counter (`#result-count` / `#shelf-count`) and the bottom-right "Grey" status pill (`#grey-toggle`) using a unified right viewport formula `max(40px, calc((100% - 1536px) / 2 + 40px))` so the right edge of "movies" aligns vertically with the right border of the Grey pill across all display resolutions.
  - **Pagination Breathing Room**: Increased top margin of `#pagination` to `42px` (`margin: 42px 0 28px 0 !important;`), providing a clean ~40px separation gap between the bottom row of movie posters and the pagination bar.

* **Pagination CSS Parser Recovery & Breathing Room Reflection**:
  - Repaired a corrupted nested selector block around line 6560 (`body.grey-docked-open .library`) that was causing browsers' CSS parsers to discard subsequent styles including the pagination rules.
  - Appended a guaranteed pagination override enforcing `margin: 44px 0 28px 0 !important;` alongside the 8px squircle buttons, 0.45 disabled button opacity, and `#dedbd4` active typography so the breathing room and Zen pagination controls reflect cleanly across all views.

* **3-State Search Target Switch & Dynamic Live Placeholder**:
  - Embedded matching 24px squircle Pill 2 (`#library-target-toggle`) beside the scope toggle in the 670px Library search bar, directly cycling across `[ ✦ All ]` → `[ 🏷 Title ]` → `[ 📝 Notes ]`.
  - Added dynamic human-readable live placeholder (`updateLibrarySearchPlaceholder`) that automatically updates as the user navigates shelves and toggles pills (e.g. *"Search notes in Watched…"*, *"Search titles across all shelves…"*, *"Search in Watched…"*, *"Search entire library…"*, *"Search all notes…"*) without requiring manual syntax prefixes.
* **Bidirectional Personal Notes Ribbon Lens (`[ 📝 ]`)**:
  - Embedded a dedicated `[ 📝 ]` notes lens button beside the Favourites Heart (`[ ♡ ]`) at the right end of the shelf ribbon, separated by a subtle 1px vertical hairline divider.
  - Supports bidirectional workflows: clicking `[ 📝 ]` from any shelf (e.g. *Watched*) immediately activates the notes lens for that shelf; clicking any shelf from the full notes collection narrows the notes strictly to that shelf; clicking the active notes button or double-clicking immediately exits back to the primary shelf view.
* **Streamlined Library Sidebar Parity**:
  - Completely removed the redundant `Has notes` modifier strip from the Personal Library sidebar, giving it the exact same clean structure and card geometry as the Discover sidebar (top `FILTERS` / `Reset` header followed immediately by accordion filter pills).

### AI. Personal Library Cross-Shelf Search & Title Matching Precision (done — Oct 25)
* **Word-Boundary Prefix Matching for Search-As-You-Type**:
  - Removed restrictive trailing lookahead assertion `(?![a-z0-9])` from both backend (`_build_word_boundary_pattern` in `app/movie_repository.py`) and frontend (`buildLibraryWordBoundaryRegex` in `app/static/app.js`).
  - Search queries now match progressive word stems and prefixes starting at word boundaries (e.g. `god` matches *The Godfather*, `bat` matches *Batman*, `inter` matches *Interstellar*, `dark kni` matches *The Dark Knight*) while properly rejecting intra-word false positives (e.g. `bat` does not match *Wombat*).
* **Search Target Pill Synchronization in Client-Side Ranking**:
  - Synchronized `searchMode` in `applyLibraryFilters()` with `state.librarySearchTarget`. When Pill 2 is switched to `[ 🏷 Title ]`, client-side ranking strictly filters by title and original title, preventing movies that only match in overview/plot or notes from leaking into Title results.
* **Instant Cross-Shelf Exploration (`All shelves`)**:
  - Toggling Scope to `[ ☷ All shelves ]` without entering search text now immediately queries and displays the full cross-shelf personal library (1,300+ movies) instead of silently no-oping or reloading only the current shelf.
  - Toggling Target to `[ 🏷 Title ]` or `[ 📝 Notes ]` while in All Shelves immediately re-executes search and re-ranks results.
* **Poster Status Badges & Nope Differentiation in All-Shelves View**:
  - Dynamically enabled status badges on poster cards during All Shelves searches (`#movie-grid.is-all-shelves-search .status-badge`), displaying the correct shelf indicators (Watched checkmark, Watch Later clock, Rewatch arrows, New Discovery star, and Excluded badge) so users can immediately distinguish which shelf each movie belongs to.
  - Added `.is-noped` styling for excluded movies during All Shelves searches to visually flag rejected titles.
  - Bumped cache buster to `v=20261025_zen_107` in `app/web/index.html`.
* **Shelf Ribbon Action Ordering (Mental Model Alignment)**:
  - Repositioned the personal notes lens (`[ 📝 ]`) to sit first right after the hairline divider, followed immediately by the favourites heart button (`[ ♡ ]`).
  - Updated flex margins (`margin: 0 4px 0 auto` on `.shelf-ribbon-divider`) so the divider and both buttons cleanly align to the right edge of the shelf ribbon with uniform spacing.
  - Bumped asset cache buster to `v=20261025_zen_108` in `app/web/index.html`.
* **Discover & Sidebar Typography Whiteness Elevation (Without Weight Halation)**:
  - Stepped up inactive sidebar category headers (*Sort*, *Genres*, *Rating*, *Release Year*, *Keywords*, *Languages*, *Countries*, *Studios*) from dim `#9c9aa5` mid-grey to crisp `#dedbd4` pearl off-white.
  - Stepped up hovered and open active category titles to `#ffffff`.
  - Stepped up `FILTERS` micro-header from `#716e7a` to `#a5a2ad` silver, and the `Reset` action link to `#c5c2cb`.
  - Stepped up input placeholders from dim `#615e6b` to readable `#7e7b89`.
  - Stepped up movie card year/language metadata and top telemetry counters from `#9c9aa5` / `#8e8b97` to `#b8b5bf`.
  - Stepped up top navigation tabs (DISCOVER, LIBRARY, NOTES) from `#9c9aa5` to `#c5c2cb`.
  - Maintained thin `400` Regular weight throughout to ensure zero halation or chunky letter bleeding.
  - Bumped asset cache buster to `v=20261025_zen_109` in `app/web/index.html`.
* **Library Sidebar Filter Aesthetics Parity with Discover**:
  - Repositioned **Sort Results** to the #1 top spot in the Library sidebar, creating exact structural parity with Discover (*Sort Results* → *Genres* → *Release Year* → *Keywords & Themes* → *Cast & Crew* → *Languages*).
  - Upgraded Library Sort Results (`#lib-sort-cloud`) to use the exact Discover 2-column squircle grid (`.sort-chip-cloud` and `.sort-chip`).
  - Upgraded Library Release Year (`#card-lib-year`) to the same-line paired inputs layout (`.sidebar-range-row` with centered dash `-`).
  - Upgraded Cast & Crew and Keywords & Themes to match Discover's compact entity grid (`.entity-grid.sidebar-entity-grid`) with screen-reader labels and clean placeholders.
  - Linked `.is-dimmed` dynamic state to `#reset-library-filters` so it dims when no filters are active and lights up as soon as a filter is chosen.
  - Bumped asset cache buster to `v=20261025_zen_110` in `app/web/index.html`.
* **Library Sidebar Strict 1:1 Parity with Discover**:
  - **Scrollbar Elimination**: Removed `max-height: 220px` and `overflow-y: auto` from `.chip-cloud`, replacing with `max-height: none !important` and `overflow-y: visible !important` with scrollbar suppressed so Genres and Languages expand naturally without internal scrollbars, matching Discover's `.tri-chip-cloud`.
  - **Font Size & Padding Normalization**: Scaled down `.filter-chip` from `var(--text-sm)` (14px) and 5px 11px padding to `var(--text-xs)` (12px) and `4px 9px` padding with `gap: 5px`, perfectly matching Discover's `.tri-chip` dimensions.
  - **Cast & Crew Hierarchy**: Placed **Actor** above **Director** in the Library sidebar's Cast & Crew picker, locking structural parity with Discover.
  - Bumped asset cache buster to `v=20261025_zen_111` in `app/web/index.html`.

### 2026-10-25 - Zen Single Movie Detail Redesign & Parity Alignment
- **2-Tier Instant Action Cockpit**: Replaced stacked Status dropdown + Save button + Verdict card with a unified card containing 5 auto-saving shelf pills (Library ribbon SVG icon parity, zero inside color fills) on Tier 1 and a 10-star rating bar with score badge on Tier 2.
- **Top Bar & Navigation Parity**: Synchronized detail header height to 64px matching .topbar. Standardized neutral ← Back to [Shelf] button and unified Prev/Next segmented pill control. Removed legacy faded NOPE watermark.
- **Hero & Dossier Layout**: Compacted poster to natural 220px x 330px (2:3 aspect ratio, uncropped). Bare inline heart toggle beside title. Aligned director and cast credits to crisp off-white (#dedbd4) with subtle labels.
- **Notes & Related Parity**: Added generous 18px separation between action cockpit and notes canvas; updated notes placeholder to 'Thoughts, observations, or anything worth remembering...'. Standardized Related Movies grid to 105px width with 22px icon status corner badges.
- **Bug Fix**: Enforced strict display hiding on #movie-grid when viewing the Notes tab (entries view).

### AI. Full Zen Foundation Restoration & Single Movie Detail Zen Architecture (v121)
- **Zen Foundation Restored**: Completely reconstructed and restored all Zen refinements in `index.html`, `styles.css`, and `app.js` (`v=20261025_zen_121`).
- **Ribbon & Lens Hierarchy**: Preserved Personal Notes lens button (`[ 📝 ]`) preceding favourites heart button (`[ ♡ ]`), with hairline divider pushed right.
- **Library Sidebar Parity**: Sort Results placed at top with squircle chip cloud, coupled release year inputs (`#lib-year-from` & `#lib-year-to`) separated by centered hyphen, Actor positioned above Director, and `.chip-cloud` scrollbars removed.
- **Typography Whiteness**: High-contrast `#dedbd4` and `#ffffff` typography applied across all category accordion triggers, headers, and navigation tabs.
- **Single Movie Detail Zen Layout**: Standardized 64px frosted topbar with uppercase tracked navigation (`Back to Movies`, `Prev` / `Next`), bare title-height inline heart, 2-tier Action Cockpit (`width: fit-content`), separated Notes card, and 105px standardized related movie posters.

- [x] **Single Movie Page Note Auto-Expansion, Ribbon Chip Truncation & Neutral Highlighting**
  * **Goal**: Fix note truncation on single movie detail pages, eliminate chopped chip borders in the preset ribbon, and replace childish colored borders with vibrant icon highlights on shelf chips.
  * **Key Changes**:
    * **Robust Note Reading & Auto-Resize ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js) & [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Overhauled `autoResizeJournalNote()` with a robust line-count heuristic fallback for hidden views, re-measuring accurately when `dialogContent` becomes visible; replaced `overflow: hidden` and `min-height: 28px` with `overflow-y: auto`, `min-height: 72px`, natural font-style, and vertical resizing so movie notes (and "Grey says" critiques) are completely visible and effortless to read.
    * **Preset Ribbon Chip Truncation ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Applied `flex-shrink: 1`, `min-width: 48px`, and text ellipsis truncation to the last ribbon chip so that the chip button itself (with 8px squircle borders and right padding) closes neatly inside the 670px canvas without getting sliced by container overflow.
    * **Shelf Ribbon Icon Highlighting ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Removed childish colored border highlights across library shelf chips, keeping a clean neutral dark squircle outline (`rgba(255, 255, 255, 0.38)`) while making the status icon itself brightly illuminate with its signature color on hover and active states.

- [x] **Universal Poster Overlay Badges: Rating on Left & Vote Count on Right**
  * **Goal**: Universalize movie poster badge positioning across Discover, Library shelves, and Related Movies with rating on the bottom-left and vote icon with formatted vote count on the bottom-right.
  * **Key Changes**:
    * **Card Badge Placement ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js) & [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - Moved `.card-rating` to `bottom: 4px; left: 4px;` in gold with star prefix (`★ 7.5`).
      - Added `.card-votes` at `bottom: 4px; right: 4px;` featuring a micro vote ballot icon and compact formatted vote count (e.g. `17.7k`, `850`, `1.2M`) with full vote volume on tooltip.
      - Implemented identically across `createMovieCard` (Discover & all Library shelves) and `createRelatedMovieCard` (Related Movies panel).

- [x] **Streamline Movie Hover Preview & Tone Down Popover Title**
  * **Goal**: Remove redundant rating and vote count badges from the library poster hover note preview (since they are already rendered on the poster corners) and tone down the popover title yellow.
  * **Key Changes**:
    * **Note Popover Header ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Cleaned the header in `showPosterNotePreview` so it solely displays the movie title and year, removing duplicate ratings and vote numbers.
    * **Tooltip Cleanup ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**: Removed redundant vote count strings from poster button tooltips in Discover, Library, and Related cards.
    * **Toned Down Title Styling ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**: Softened `.poster-note-popover-title` from stark `var(--accent)` (`#f2ca52`) to the calm brand yellow (`#DEC68B`), balancing legibility with visual comfort.

- [x] **Universal Custom Hover Title Preview Across Discover & Related Cards**
  * **Goal**: Replace the sluggish native browser tooltip in Discover and Related Movies with the sleek, dark frosted glass hover popover matching the Library hover card.
  * **Key Changes**:
    * **Compact Title-Only Popover Mode ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js) & [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - Added `.poster-note-popover.is-title-only` styling featuring a compact, auto-width 8px squircle pill with no bottom separator.
      - Enabled `schedulePosterNotePreview` on all Discover and Related movie cards: displays movie title in soft brand yellow (`#DEC68B`) and release year in muted grey upon hover, seamlessly expanding if the movie has personal notes.
      - Stripped `title` attributes so native OS tooltips never clash with the custom popover.

- [x] **Refine Hover Title Micro-Pill Typography**
  * **Goal**: Tone down the weight, scale, and padding of the hover title popover so it appears as a subtle, elegant micro-pill.
  * **Key Changes**:
    * **Popover Typography ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - Reduced title size from `0.88rem` down to `0.75rem` and weight from `700/800` to a calm `550`.
      - Reduced year size to `0.69rem` (`400` weight).
      - Tightened padding to `4px 9px` with a sleek `6px` squircle corner radius.

- [x] **Elevate Active Preset Chip Border Prominence**
  * **Goal**: Fix overly subtle highlight border on active Discover preset ribbon chips so the selected preset is clearly identifiable.
  * **Key Changes**:
    * **Active Preset Styling ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - Replaced the low-opacity `0.58` hairline border with a defined `1.5px solid rgba(222, 198, 139, 0.92)` brand yellow border.
      - Added a gentle `rgba(222, 198, 139, 0.06)` ambient warm background wash.
      - Crisp `#F3F4F6` text at `550` weight makes the active preset clearly stand out against inactive chips.

- [x] **Unify Library Shelf Ribbon: Muted Yellow Icons, Crisp White Text & Parity Highlight Border**
  * **Goal**: Strip rainbow status colors from shelf chips, unifying all shelf icons in muted brand yellow with white text and an identical highlight border matching the preset chips.
  * **Key Changes**:
    * **Shelf Icon Harmonization ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - Replaced divergent rainbow status colors with universal muted brand yellow (`rgba(222, 198, 139, 0.72)` / `#DEC68B` on hover/active) across all shelf chips.
      - Retained clean `#FFFFFF` text across all states.
      - Applied identical highlight styling to match Discover preset chips: `1.5px solid rgba(222, 198, 139, 0.92)` border with `rgba(222, 198, 139, 0.06)` ambient wash.

- [x] **Relocate Rating & Votes Exclusively to Hover Card for Clean Poster Artwork**
  * **Goal**: Strip all rating and vote number overlays from movie posters across Discover, Library shelves, and Related cards, rendering them exclusively in the clean hover preview card.
  * **Key Changes**:
    * **Clean Poster Artwork ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js) & [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - Completely removed `.card-rating` and `.card-votes` overlay elements from poster cards, restoring 100% unobstructed, distraction-free movie poster artwork.
    * **Refined Hover Card Header ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js) & [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - Integrated rating and vote count into `.poster-note-popover-header` as a neat, balanced pair (e.g. `★ 7.5 (17.7k)`) aligned with the movie title and year.
      - Styled in soft brand yellow (`#DEC68B`) with muted vote numbers, keeping the hover card minimal and elegant.

- [x] **Intelligent & Conditional Browse Mode Toggle (Paged `book-open` vs Continuous `∞`) & Floating Scroll-to-Top**
  * **Goal**: Provide seamless switching between Paged and Continuous scroll with Option 1 Lucide icons (`book-open` vs `∞`), position the toggle on the far right of the filter ribbon directly beneath the movie count, auto-hide the toggle intelligently when a shelf or search has only a single page (<= 30 movies or single TMDB page like Watch Later), enable endless single-movie stepper auto-fetching in continuous mode, and ensure instant cache-backed continuous scrolling in Discover view and reliable Scroll-to-Top positioning in Grey mode.
  * **Key Changes**:
    * **Intelligent Visibility Guard ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**:
      - Added `shouldShowShelfViewToggle()`: evaluates whether `totalPages > 1` and total movie items exceed page size (`> 30` in library, `> 20` in discover).
      - If a shelf or status has only a few movies (e.g. Watch Later, small filtered queries), the toggle remains completely hidden and unobtrusive.
      - Automatically appears when multi-page navigation is possible across Library shelves and Discover.
    * **Unified Discover Cache & Prefetch Continuous Scroll ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**:
      - Extracted unified `fetchDiscoveryBatch()` used by `executeDiscoverySearch()`, `prefetchDiscoveryPage()`, and `loadNextContinuousBatch()`.
      - Corrected continuous endpoint to use `/movies/discover/super-advanced` (or `/advanced`) and unified `discoveryCache` Map: when scrolling down, subsequent batches are retrieved instantly from memory cache and the following page is prefetched speculatively.
    * **Zen Toggle Styling & Alignment ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html) & [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - Inserted `.shelf-view-toggle` into `.discover-ribbon-row` and `.library-ribbon-row` with `margin-left: auto`, perfectly locking to the right edge directly beneath `#result-count` and `#shelf-count`.
      - Styled 28px pill with `book-open` and `infinity` SVG icons; active state glows in soft Zen gold (`#DEC68B` / `rgba(222, 198, 139, 0.14)`).
      - Remembers preference across sessions in `localStorage`.
    * **Continuous Stepper Auto-Fetch ([`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**:
      - In Continuous Mode, stepping through movies with `[ ‹ Prev | Next › ]` (or arrow keys) automatically fetches the next batch when reaching the end of the loaded queue, making single-movie navigation endless.
    * **Floating Scroll-to-Top Badge & Grey Mode Docking Parity ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css) & [`app.js`](file:///f:/Movie_Excluder/movie-excluder/app/static/app.js))**:
      - Refined `#back-to-top-btn` into a compact 34×34px badge (`border-radius: 8px`, `rgba(20, 20, 24, 0.90)` with `backdrop-filter: blur(12px)`).
      - Fixed alignment: in normal mode, positioned at `right: 144px; bottom: 26px; z-index: 1060`, vertically centered and leaving a clean 11px gap to the left of the 109px-wide Grey pill with zero overlap.
      - Fixed Grey mode library scrolling: in `body.grey-docked-open`, `.site-shell` is the scrolling container rather than `window`; added `getActiveScrollPosition()` checking `elements.shell.scrollTop`, wired shell scroll listeners, and positioned button at `right: calc(420px + 24px); bottom: 26px; z-index: 1060`.
      - Smoothly fades in after 450px of scroll in both normal and Grey modes; clicking it smoothly scrolls the active scroll container to top.

- [x] **Keyword Chips Beneath Poster & Static Zero-Hover Interaction for Keyword & Genre Chips**
  * **Goal**: Relocate keyword chips beneath the poster in the poster column, and convert both keyword and genre chips into static, non-interactive textual chips with no hover or highlight effects.
  * **Key Changes**:
    * **Keyword Relocation ([`index.html`](file:///f:/Movie_Excluder/movie-excluder/app/web/index.html) & [`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - Moved `#dialog-keywords` into `.detail-poster-column`, positioning it directly beneath `.dialog-poster-wrap` with a clean `14px` top margin matching the 270px poster column width.
    * **Static Non-Interactive Styling ([`styles.css`](file:///f:/Movie_Excluder/movie-excluder/app/static/styles.css))**:
      - Applied `cursor: default`, `pointer-events: none`, and eliminated all `:hover` color, border, and transform changes for both keyword chips (`.poster-keywords .tag`) and genre chips (`.dialog-genres .tag`).
      - Genre chips remain in their current position above the plot overview.
