> **AI INSTRUCTION**: Only read and process items listed under **🟢 Pending Tasks (Active Focus)**. Treat **✅ Completed Tasks** as historical archive data only—do not re-implement, modify, or discuss them unless explicitly requested by the user.

# Project Improvements & Backlog

## 🟢 Pending Tasks (Active Focus)

*(No pending tasks — backlog is clear.)*

---

## ✅ Completed Tasks

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

---

*Last Updated: October 22, 2026*
