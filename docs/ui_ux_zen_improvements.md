> **AI INSTRUCTION**: Only read and process items listed under **Ã°Å¸Å¸Â¢ Pending Tasks (Active Focus)**. Treat **Ã¢Å“â€¦ Completed Tasks** as historical archive data onlyÃ¢â‚¬â€do not re-implement, modify, or discuss them unless explicitly requested by the user.

# UI & UX Improvements (Zen & Function)

## Ã°Å¸Å¸Â¢ Pending Tasks (Active Focus)


- [x] **Task 15: Single Movie Detail Header & Typography Architecture (Complete Editorial Flow)**
  * **[CANVAS & POSTER COLUMN (LEFT)]**:
    - **64px Left-Anchored Canvas**: Desktop left padding halved to 64px, locked in strict vertical alignment with the [ ← Back to ... ] button.
    - **Cinematic 270x405px Poster**: Stepped up from 240x360px (+12.5%, 2:3 ratio).
    - **Poster Top Overlays (Rating & Votes)**:
      * **Top-Left**: Brand yellow (#DEC68B) star icon and score (★ 6.5) on dark frosted pill.
      * **Top-Right**: Brand yellow (#DEC68B) vote count with semantic unit (e.g. 17.7k votes) in brand yellow (#DEC68B) on dark frosted pill directly overlaid on the poster.
    - **Clean Poster Base**: Keywords relocated to the right column, leaving the bottom of the poster completely uncluttered.
  * **[CREDITS FILMOGRAPHY ROUND-TRIP]**:
    - Clicking any director or actor opens their filmography view while capturing the origin movie snapshot.
    - Filmography toolbar return button dynamically labels [ ← Return to Movie Title ] (e.g. ← Return to Avatar).
    - Clicking the return button seamlessly restores the library context and re-opens the exact single movie detail page.
  * **[PENDING CODE SIGNAL] Genre Presentation as Chips**:
    - Revert genres from plain text with bullet dots back to sleek, calm chips/pills (8px squircle, subtle border, quiet muted grey text) matching the Zen chips design system. No code changes until user explicitly requests.
  * **[MAIN CONTENT COLUMN (RIGHT) - SEQUENTIAL FLOW]**:
    1. **Movie Title**: Dominant headline scale (clamp(1.85rem, 2.7vw, 2.35rem)), favorite heart removed.
    2. **Year & Language**: Dedicated row directly beneath title (2009 • EN), **no leading bullet**.
    3. *[Breathing Room Space]*
    4. **Genres [PENDING NEXT SPRINT]**: Style as sleek chips (reverting plain text dots back to calm squircle chips per user request) (•), heavy pill frames removed.
    5. *[Breathing Room Space]*
    6. **Movie Description**: Full column width parity (510px width cap removed; expands naturally to match actors and section bounds).
    7. *[Breathing Room Space]*
    8. **Director & Cast**: Interactive clickable links without underlines; cast preceded by leading bullet (• ) with generous bullet separators (  •  ).
    9. *[Breathing Room Space]*
    10. **Keyword Chips (DNA)**: Relocated from under the poster to sit beneath the Director & Cast credits.
  * **[PENDING DECISION] Prominent Status Repositioning**: Finalize new prominent placement of the movie status badge/indicator (position to be chosen).

- [ ] **Task 4: Search Profiles (Zen Redesign)**
  * **Eliminate Redundant Dropdown & Orphaned Divider**: Completely remove the bottom `<select>` dropdown box and its divider line. Clickable chips above already handle 1-click preset switching.
  * **Eradicate Dead Black Void ("IN RESERVE")**: Consolidate profiles into a single calm group labeled **`SAVED PRESETS`** (with a quiet `4/6` counter on the right). Never render an empty "IN RESERVE" header or dead vertical gap when no reserve profiles exist.
  * **Calm the Preset Chips**:
    - Remove the redundant gold star `Ã¢Ëœâ€¦` icon from all chips.
    - Inactive presets use soft, muted grey borders/text (`#9c9aa5`) and regular weight so they recede peacefully.
    - **Highlight ONLY the currently active preset** in warm gold (`var(--accent)`), making it immediately clear which profile is driving the results.
    - Keep a subtle `Ãƒâ€”` on hover/focus for 1-click removal.
  * **Clean Action Links**: Replace cramped mechanical buttons (`Save / Update / Delete`) with a quiet, borderless inline link (`+ Save current search as preset`) that illuminates only when filters have been staged or modified.

- [ ] **Task 5: Top Bar & Display Counters**
  * **Sort Controls**: Permanently retained in left sidebar per user decision, now styled as a balanced 50/50 2-column grid.
  * **Calm Search Input**: Remove the bright yellow "Search" button; rely on natural `Enter` key trigger or debounced search.
  * **Subtle Movie Counter (Context-Aware)**:
    - *Discover / Global Search*: Render as clean, dimmed secondary text without borders (e.g. *"Showing 24 of 1,820 movies"*).
    - *Personal Library Shelves (Nope, Watched, Favourites)*: Display **Total Count only** (e.g. `687 movies`) in quiet, borderless dimmed text. Page batch counts like "24" are technical noise in a personal library.

- [ ] **Task 6: Movie Grid Spacing, Alignment & Centered Pagination**
  * **Snap Header Controls to Grid's Right Edge**: Fix `.section-heading` and `.section-heading-meta` (`[Pages | Continuous]` and movie count) so they snap directly to the right edge of the movie grid, eliminating the awkward gap where controls float far out into empty space past the 6th poster column.
  * **Poster Grid Breathing Room**: Increase card grid gap (`16px`Ã¢â‚¬â€œ`20px`) and widen the grid to cleanly align with the top bar.
  * **Hover Title Legibility**: Fade in a clean text title overlay on hover to ensure movies with dark/stylized poster art are readable.
  * **Centered Pagination**: Re-align bottom pagination numbers (`1, 2, 3...`) directly to the horizontal center of the movie grid.

- [ ] **Task 7: Notes Ledger List Hierarchy & Typography**
  * **Scale Down List Note Titles**: Drop note titles in list/ledger mode from `1.00rem` (16px) Semibold (`600`) down to `0.88rem` (14px, `--text-base`) with Medium (`500`) or Regular (`400`) weight.
  * **Soften Contrast on Dark Background**: Switch note titles from stark `#ffffff` to warm off-white (`#f5f3ee`) to prevent text bleeding and dense clutter across vertically stacked rows.
  * **Harmonize Date-to-Title Transition**: Smooth the visual step between the timestamp (`Oct 24` at `12.5px`, dimmed grey) and the title.
  * **Parent Timeline Hierarchy**: Rebalance month group headers (`2026 Ã‚Â· OCTOBER`) as crisp structural bookmarks so child items stay naturally subordinate to their timeline parent.

- [ ] **Task 8: Personal Library Zen Alignment & Unified Harmony**
  * **[LOCKED IN] Item 1: Move Search Bar to Top Canvas (Pixel-Perfect Parity)**: Position 'Search library...' in the main canvas in the exact same physical coordinates, width (max 440px), height (36px pill), and styling as the Discover search bar. Toggling between Discover and Personal Library produces zero layout shift.
  * **[LOCKED IN] Distinct Topbar Demarcation**: Elevate .topbar bottom border from invisible white (0.08) to a distinct, subtle warm gold hairline (rgba(242, 201, 76, 0.22)) for crisp separation across the entire screen.
  * **[LOCKED IN] Item 2: Move 6 Shelves into Top Ribbon**: Relocate the 6 personal shelves (New discovery, Watched, Watch later, Rewatch, Favourites, Nope) into the horizontal ribbon above the posters, adopting the Zen Option A formula for the active shelf.
  * **[NOTED - PENDING DISCUSSION] Remove Nope Mode Button & Replace with Keyboard Shortcut**:
    - **Problem**: Placing `[ Ã¢Å“â€¢ Nope Mode ]` right adjacent to the search input creates false affordanceÃ¢â‚¬â€it looks and feels like a search submit button.
    - **Solution**: Remove the physical Nope Mode button from the top canvas header completely.
    - **Keyboard Shortcut**: Trigger Nope Mode via a dedicated, instant hotkey (e.g., `X` or `N` when not focused on a text input, or `Alt+X` / `Shift+X`), with `Escape` to quickly exit.
    - **Visual Feedback**: When active, show a quiet floating banner / status pill or cursor cue so the user knows they are in exclusion mode, without cluttering the search bar.
    - **Result**: The Discover search bar stands on its own with clean symmetry, zero clutter, and no confusion about what executes a search.
  * **[NOTED - PENDING DISCUSSION] Single Continuous Scroll Toggle**:
    - Replace the two-button segmented pill (`[ Pages | Continuous ]`) with a single, calm binary switch button (e.g. `[ Ã¢Ë†Å¾ Continuous ]` or toggle switch).
    - Default state is standard paginated browsing. When activated/lit, continuous scroll is enabled.
    - Eliminates redundant "Pages" button, cuts visual weight in half, and preserves clean open space on the right of the shelf ribbon.
  * **[LOCKED IN] Item 5: Remove Duplicate Sort Accordion**: Eliminate the redundant second 'Sort Results' accordion at the bottom of the Library sidebar, preserving the clean top sort.
  * **Cross-Sidebar Parity**: Symmetrically apply all Discover Zen tokens (FILTERS / Ã¢â€ Âº Reset header row, 34px inputs, muted golden separation borders) across Library and Notes.
  * **Global Structural Parity**: Any structural or stylistic refinement applied to the Discover sidebar applies symmetrically across the Personal Library and Notes sidebars.
  * **Delete Dividers Universally**: Remove horizontal divider lines and category borders across all three sidebars (Discover, Library, Notes); rely exclusively on clean vertical breathing room.
  * **Unified Geometry & Padding**: Standardize all sidebar navigation links, shelf buttons, and accordion triggers to identical geometry (`border-radius: 8px`, `padding: 8px 12px`, uniform row rhythm). Replace the chunky `999px` pill capsules in Discover with sleek rounded rows to match Library and Notes.
  * **Harmonized Font Size & Weight Across All Panes**:
    - Inactive items: Standardized to `13px` (`0.82rem`), Regular (`400`) weight, in soft off-white (`#c5c2bb` / `#9f9da8`).
    - Active items: Standardized to `13px` (`0.82rem`), Medium (`500`) weight, in warm gold (`var(--accent)`).
  * **Consistent Subdued Counts**: Replace any remaining loud notification badges with quiet, secondary right-aligned text numbers (e.g. `12` in soft dimmed grey `#7b7883`).
  * **Shared Micro-Header Standard**: Standardize section headers (`FILTERS`, `LIBRARY`, `TAGS`, `TIMELINE`) to `11px`, Medium (`500`), uppercase, dimmed grey with subtle tracking.

- [ ] **Task 9: Library Shelf Wayfinding (Context Without Badges)**
  * **Keep Library Posters Clean**: Retain zero status badges on Personal Library shelves, exactly as today.
  * **Shelf-Aware Counter**: Replace generic `687 movies` with shelf-specific wording (`687 watched`, `142 to watch`, `93 noped`, `21 to rewatch`). Delivers the reminder with zero new elements.
  * **Shelf Icon Before Counter**: Prefix the counter with the same icon as the active ribbon chip (check, clock, ban, loop). Color on the icon only, using the same muted tones as Discover badges.
  * **Stronger Active Ribbon Chip**: Active shelf chip gets a gold icon and slightly brighter text; inactive chips stay quiet grey.
  * **Per-Shelf Empty States**: One calm line per shelf when empty (e.g. `Nothing noped yet`, `Your watch-later list is empty`).
  * **Sticky Ribbon Row on Scroll**: Pin the whole ribbon row (shelf chips + counter) as a slim bar while scrolling so shelf context never disappears. Do not pin the counter on its own. Rationale: deep in a long shelf the header scrolls away and context is lost (Plex keeps its library bar pinned for the same reason). Zen styling: thin bar, same dark background, faint bottom hairline that appears only once scrolling starts.

- [x] **Task 10: Pagination Breathing Room & Cross-View Consistency**
  * **Clear Grid Separation**: Set the pagination container's top gap to ~36px-40px from the bottom poster row so pagination reads as separate from the grid's internal row spacing.
  * **One Rule Everywhere**: Same pagination spacing, width (670px grid-aligned), and centering in Discover and all Personal Library shelves (and any other paginated view).
  * **Fix Invisible "Previous" / Disabled State**: Currently `.pagination button:disabled` has `opacity: 0.28` and border opacity `0.04`, making Previous on Page 1 completely blacked out into the background. Elevate disabled state to ~0.45 opacity with a visible hairline border so the button outline remains cleanly discernible.
  * **Geometric & Color Sync**: Pagination buttons currently use chunky `border-radius: 999px` capsules. Convert to the universal 8px squircle (`border-radius: 8px`). Harmonize inactive page number text from muddy `#9c9aa5` to clean `#dedbd4` off-white.

- [x] **Task 11: Preset Ribbon Overflow & Floating Toast Notifications**
  * **Bug - 6th Preset Cut Off**: With 6 saved presets, the 6th ribbon chip is clipped at the 670px right edge (hidden scrollbar, no cue). Fix: cap chip width (~105px-120px) with ellipsis + full name on hover so all 6 always fit in one row without scrolling.
  * **Bug - Ugly Inline Notice Banner**: `showNotice()` renders a full-width boxed banner with red/rose text between the ribbon and the grid, pushing posters down. Even success messages (e.g. `Saved \"test 2 preset\"`) look like errors.
  * **Fix - Floating Toast**: Replace with a small floating toast at the top-right (below the topbar), overlaying content with zero layout shift. Calm dark pill (#161618), subtle border, off-white text; tone only via a small icon (gold = success, muted rose = error). Auto-dismiss ~3s. Exact spot: fixed to viewport, ~12px-16px below the topbar hairline, ~24px from the right edge, max ~320px wide, single line (briefly overlays the movie counter). Motion: slides in leftward from the right edge (~16px-24px travel) with a fade, ~200ms ease-out; exits with a fade + slight slide right. Respect prefers-reduced-motion (fade only). Multiple toasts stack downward, max 2. Keep clear of the Grey button (bottom-right) and the Nope Mode banner (bottom-center). Apply to every showNotice() call across Discover, Library and Notes.

- [x] **Task 12: Search Profiles - Integrate Orphaned Action Links**
  * **Problem**: `Update active preset` and `+ Save current search as preset` float as bare bright-white text below the boxed preset rows, with icons offset left of the pin column. They read as secondary actions shouting louder than the content, and Update shows even when nothing changed.
  * **Save as Last List Row (Ghost Slot)**: Render `+ Save current search as preset` as the final row of the list with identical row geometry (height, 8px radius, padding), `+` icon aligned in the same column as the pins, faint dashed border, muted grey text, warming to gold on hover. Reads as an empty slot waiting to be filled.
  * **Contextual Update on Active Row**: Remove the standalone Update link. Show a small refresh icon at the right edge of the active preset row only when its filters have been modified.
  * **Typography Parity**: Action text uses the same size, weight and muted grey as the preset rows.
  * **Full State (6/6)**: Hide the Save slot when the list is full and show a quiet `6/6` counter beside the header.

- [x] **Task 13: Nope Mode Hotkey - Replace Single-Key `X`**
  * **User Request**: Move Nope Mode off the bare `X` key to a deliberate modifier combo (user requested `Ctrl+N`), since Nope Mode is used occasionally and should not trigger accidentally. `Escape` still exits.
  * **Caveat - Ctrl+N Is Browser-Reserved**: Chrome/Edge/Firefox reserve `Ctrl+N` (new window) and do not let web pages intercept it, so it cannot work reliably in a normal browser tab. Recommended alternative: `Alt+N` (free in all major browsers, same N-for-Nope mnemonic). Confirm final combo with user before implementing.
  * **Remove Hotkey Hint From Search Bar**: Strip `(Press X for Nope Mode)` from the Discover search placeholder entirely; it is distracting and unnecessary. Placeholder becomes simply `Search any movie...`. The hotkey hint lives only in the floating Nope banner (shown while the mode is active) and optionally a hover tooltip.

- [x] **Task 14: Discover Poster Badges - Icon-Only Corner Badges**
  * **Problem - Too Wide, Covers Art**: The `* DISCOVERY` text pill spans ~55% of poster width and stamps over titles/artwork (e.g. *Digger* row 1 col 5, *Heart of the Beast* row 3 col 1).
  * **Problem - Repetitive Noise**: 6-7 posters repeating all-caps `DISCOVERY` reads as a wall of labels instead of posters.
  * **Fix - Icon-Only Badge**: Replace the text pill with a `22px x 22px` rounded-square icon badge (`backdrop-filter: blur(6px)`, `background: rgba(15, 15, 18, 0.75)`), top-left corner, matching the bottom-left Note icon scale.
  * **Icons 1:1 With Library Shelf Chips**: Discovery = sparkle (soft gold), Watched = check, Watch later = clock, Rewatch = loop, Nope = ban-circle. Reuse the exact same SVGs and muted tones as the shelf ribbon chips.
  * **Text on Hover Only**: Full status name via tooltip / `aria-label` for accessibility; no visible text label on the card.
  * **Library Shelves Unchanged**: Library posters stay badge-free (see Task 9).
  * **Distinct Muted Icon Colors (Agreed)**: At 22px, same-tone icons blur together. Each status gets its own muted tone: Discovery = soft gold (`#f2c94c`), Watched = sage green (`#72d6a0`), Rewatch = muted blue (`#79c0ff`), Watch later = muted lavender (e.g. `#b4a7e6`), Nope = muted rose (`#cf9b9e`, matching the Zen exclusion tone; replaces the loud `#ff6b6b`).
  * **Discovery Keeps Its Badge**: No badge = untracked, so Discovery must always show its sparkle icon to stay distinguishable. The icon-only format alone resolves the repetition noise.

- [ ] **Task 15: Library Search Scope Selector ([ All ] [ Title ] [ Notes ]) - Placement Decision Pending**
  * **Core Functionality**: A 3-way segmented scope selector replacing passive `Has notes` filter.
    - `[ All ]` (Default): Free-text search across Title, Overview/Plot, and Notes across the library shelf.
    - `[ Title ]`: Pure movie title lookup only.
    - `[ Notes ]`: Dual action: 1. Instantly isolates movies with personal notes; 2. Restricts free-text search strictly to words inside the user note text (ignoring plot/title words).
    - *Note on TMDB Keywords*: Resolved to keep explicit keyword searching inside the dedicated `Keywords & Themes` sidebar accordion with autocomplete, rather than adding a 4th chip.
  * **Placement Option 1 (Canvas Search Cluster - High Proximity)**: Positioned directly adjacent to the search input in the top canvas as a compact 36px 8px-squircle segmented pill. Pros: zero eye travel, direct input proximity. Cons: search bar width differs slightly from Discover.
  * **Placement Option 2 (Top of Left Sidebar - Canvas Symmetry)**: Positioned right below `FILTERS / ? Reset` in the Library sidebar card (replacing the old `[ ?? Has notes ]` button). Pros: 100% pixel-identical canvas search bar between Discover and Library; balances sidebar top slot. Cons: spatial disconnect between search bar and scope toggle.
  * **Status**: Both options documented. Final placement decision deferred to user.

- [x] **Task 16: Library Search Scope - Single Dynamic 2-State Switch Button**
  * **Problem**: The 2-button segmented pill (`[ All Shelves | Current Shelf ]`) is ~160px wide, cluttering the top canvas search row.
  * **Solution (Agreed)**: Replace with a single, compact (~75px) 8px-squircle toggle button that flips state on click.
  * **Unambiguous State Design**: Use an `In:` prefix to avoid play/pause confusion:
    - Both states have equal visual dignity (neither is dimmed or disabled): clean dark fill (#161618), subtle warm gold hairline border (rgba(242, 201, 76, 0.35)), crisp off-white text (#f5f3ee).
    - State 1: `In: This shelf` ⇄ State 2: `In: All shelves`.

- [x] **Task 17: Favourites Heart Button - Reversible 2-Way Toggle**
  * **Problem**: Clicking the Hall of Fame Heart button in the shelf ribbon is a 1-way action (loads Favourites; clicking again just reloads Favourites, trapping the user).
  * **Solution (Agreed)**: Make it a true 2-way reversible toggle (matching the existing Notes memory pattern):
    - 1st click: Remembers the previous shelf (e.g. `Watched` or `Watch later`), illuminates the Heart in crimson/gold, loads Favourites.
    - 2nd click: Un-highlights the Heart and immediately returns to the previous shelf.

---

## Ã¢Å“â€¦ Completed Tasks

- [x] **Personal Library Card Parity & Right-Aligned Browse Mode Toggle**
  * **Card Envelope Parity**: Wrapped .library-filters-workspace in the exact floating card styling as .discovery-workspace (16px rounded corners, rgba(242, 201, 76, 0.28) hairline border, dark glass background, and 12px 14px padding) for zero physical shift between tabs.
  * **Right-Aligned Browse Toggle with Generous Space**: Positioned [ Pages | Continuous ] at the far-right edge of the ribbon row (margin-left: auto), separated from the 5 status chips by a generous open gap of negative space, styled as a quiet 2-segment switch (#131317) to prevent visual mixing.
  * **Counter Typography**: Bumped top-right movie count font size to 14px (var(--text-base)) with unified UI font family.

- [x] **Top Bar Demarcation, Sidebar Double-Wall Removal & Extreme Top-Right Telemetry**
  * .topbar demarcated with distinct warm gold hairline border (rgba(242, 201, 76, 0.22)).
  * Removed vertical double-wall border on .sidebar (border-right: none), letting rounded filter cards float in negative space.
  * Extreme Top-Right Telemetry & Font Harmony: Bound search and Nope Mode to exact 670px 6-column grid width with Nope flush right, and positioned the movie counter at the extreme top right in open negative space with unified UI font (var(--font-ui), var(--text-xs), #8e8b97).
  * Eradicated giant 32px 'Filtered discovery' headline completely; posters rise ~50px directly beneath the ribbon.

- [x] **Universal 8px Squircle Geometry & Positive Selection Distinction**
  * Converted puffy 999px capsules to sleek 8px squircles across Search Bar, Nope Mode toggle, Ribbon chips, Preset Action rows, and all sidebar chips (.tri-chip genres/languages, .sort-chip, .filter-chip, and .selected-entity pills).
  * Preserved faded brand yellow (+, rgba(242, 201, 76, 0.75)) for positive inclusions and muted rose (Ã¢Ë†â€™, #cf9b9e) for exclusions.

- [x] **Preset Action Rows Geometric Consistency (Update & Save)**
  * Converted 'Update active preset' and 'Save current search as preset' into full-width 8px squircle action rows separated by 12px space.
  * Subdued dashed quiet outline (1px dashed rgba(242, 201, 76, 0.25)), uniform Regular 400 weight (12px), and crisp 12x12px inline vector SVGs (circular refresh arrow and plus).

- [x] **Personal Library Zen Alignment & Unified Ribbon Parity**
  * Library search bar mirrored in top canvas header (36px squircle, flex: 1 width, zero layout shift when toggling views).
  * 5 core personal workflow shelves (New discovery, Watch later, Watched, Rewatch, Nope) live in the top ribbon with Option A 8px squircle chips.
  * Favourites and Has Notes live as a twin modifier strip ([ Ã¢Ëœâ€¦ Favourites only ] [ Ã°Å¸â€œÂ Has notes ]) at the top of the Library sidebar under FILTERS / Ã¢â€ Âº Reset.
  * Removed duplicate bottom Sort Results accordion in Library sidebar, preserving the clean top sort.

- [x] **Visual Separation & Counter Deduplication Fix**
  * Subtle brand yellow / warm gold borders on Left Sidebar, Search Bar, Ribbon Pills, and Nope Mode for crisp visual separation.
  * True total movie count restored (never defaulting to page slices like 12 or 24).
  * Deduplicated movie counters by hiding the top-bar counter in Discover, keeping solely the counter beside [Pages | Continuous].

- [x] **Task 6: Movie Grid Spacing, Right-Edge Alignment & Centered Zen Pagination**
  * Bound .discover-canvas-header and .section-heading to max-width: 670px, snapping controls cleanly to the 6th column right edge while preserving the original compact 105px Letterboxd poster scale.
  * Added smooth hover title/year overlay on poster cards for dark/stylized artwork readability.
  * Centered pagination strip under the movie grid with Option A active page pill and 32px compact geometry.

- [x] **Top Search Bar & Nope Mode: Zen Redesign**
  * Retired the bright yellow 'Search' button. Top search input is now a sleek, borderless-feel 36px pill (#141419 fill, subtle border, quiet magnifying icon, triggers on Enter).
  * Nope Mode toggle converted to a calm 36px Zen pill (#161618 dark fill, muted grey text #9c9aa5, regular weight). Active state uses calm muted rose exclusion (#cf9b9e / rgba(220,100,100,0.12)) without pulsing animation.

- [x] **Top Ribbon Preset Pills: Option A & Zen Philosophy Alignment**
  * Active preset ribbon chip (.ribbon-chip.is-active) uses the Option A Zen formula: dark #161618 fill, muted gold border (rgba(242, 201, 76, 0.5)), soft off-white text (#f5f3ee), regular 400 weight, and subtle 8px ambient glow.
  * Inactive ribbon chips use dark #161618 fill, subtle border (rgba(255, 255, 255, 0.08)), muted silver/grey text (#9c9aa5), and regular 400 weight.

- [x] **Pure Zen Movie Counters: Eliminate Pagination Noise & De-Box Counts**
  * Eliminated all pagination arithmetic ('24 of 1,820 movies', 'X movies on this page'); now displays purely the total count (e.g. '1,820 movies').
  * De-boxed .result-count and .shelf-movie-count to quiet, borderless, dimmed text (#716e7a, 12px, regular weight).

- [x] **Sidebar Zen Mode: Selected Entity Pills, Uniform Input Heights & Preset Alignment**
  * Excluded keyword/entity pills match the quiet genre exclusion phenomenon (dimmed 60% opacity, muted rose text #cf9b9e, quiet border rgba(220,100,100,0.22), no strikethrough).
  * Included keyword/entity pills match Option A (#161618 dark fill, rgba(242,201,76,0.5) gold border, #f5f3ee warm off-white text, subtle 8px gold glow).
  * Uniform 34px height across all sidebar data entry fields (Minimum Votes, Rating, Release Year, Keywords & Themes, Actors, Directors, Studios, Library search).
  * Nudged preset action links right (29px left padding) to align under the letter 'A' of the preset chip name.

- [x] **Task 4: Search Profiles (Zen Redesign) & Input Pair Refinements**
  * **Consolidated Saved Presets (0/6)**: Eradicated the empty "IN RESERVE" black void and orphaned divider lines. All saved profiles live in one unified list with an unobtrusive counter.
  * **Calm Preset Chips**: Removed star icons (`Ã¢Ëœâ€¦` / `Ã¢Ëœâ€ `). Inactive presets use quiet muted grey (`#9c9aa5`), while the currently active preset highlights cleanly in warm gold (`#f2c94c`). Each chip includes a subtle `Ã¢Å“â€¢` for 1-click deletion.
  * **Clean Action Link**: Replaced cramped buttons (`Save / Update / Delete`) and redundant `<select>` dropdown with a quiet inline link (`+ Save current search as preset`).
  * **Empty Keywords Container Collapse**: Set `.selected-entities:empty` to collapse with zero margin/padding so the drawer hugs the input box without a dead void gap.
  * **Min Ã¢â‚¬â€œ Max Rating & Year Pair Dash**: Added a subtle, dim en-dash separator (`Ã¢â‚¬â€œ`) between the Min and Max rating boxes and From/To release year boxes, cleanly unifying them as balanced pairs.

- [x] **Task 3: Sidebar Typography (De-Thickening, Halation Fix & Input De-Escalation)**
  * **Scientific Category Label Hierarchy**: Applied Regular (`400`) in muted silver/grey (`#9c9aa5`) with `+0.015em` tracking to inactive sidebar category titles; active/open titles step to Medium (`500`) in warm off-white (`#f5f3ee`) with no pixel halation or glare.
  * **Inverted Input Scale Fixed**: Subordinated all numeric inputs (Rating, Minimum Votes, Release Year) to Regular (`400`), `12px` (`--text-xs`), and muted `#c5c2cb` with compact `32px` height, keeping parent titles as the dominant visual anchors.
  * **Native Stepper Arrows Eliminated**: Stripped visual spinner arrows (`appearance: textfield`) across number inputs while retaining physical keyboard Up/Down arrow nudging.
  * **Quiet Excluded Genres**: Dropped strikethrough per user feedback; excluded items recede gracefully at 60% opacity with a muted maroon border and soft rose text.
  * **Sort Results 50/50 Grid**: Formatted sidebar sort drawer into a clean 2-column 50/50 grid (`grid-template-columns: 1fr 1fr`), removing jagged text-length edges.
  * **Balanced Header Row**: Restored dim uppercase `FILTERS` micro-label on the left to perfectly balance the right-aligned `Ã¢â€ Âº Reset` link.
  * **Favorites Shelf Zen Mode**: Suppressed redundant `.favorite-mark` heart on the Favorites shelf for 100% clean posters.

- [x] **Task 2: Left Sidebar (Filters & Mechanics)**
  * **Single `See results` with Staged Dirty State**: Replaced the cramped 4-button row with a clean, full-width `See results` button that illuminates in warm gold only when filters are pending.
  * **Header `Ã¢â€ Âº Reset` Button (No Redundant "FILTERS" Label)**: Completely removed the redundant "FILTERS" text label; positioned a subtle right-aligned `Ã¢â€ Âº Reset` button with an undo icon right below `See results` (dimmed when inactive, bright on active filters with hover rotation).
  * **Zero Collapsed Signals**: Completely hid all yellow notification pills (`#badge-genres`, `#badge-rating`, etc.) on collapsed sidebar categories for uniform, calm row rhythm.
  * **Zero Dividers**: Removed horizontal category divider lines across the sidebar; whitespace alone creates the separation.
  * **In-Box Faded Placeholders**: Replaced stacked redundant labels ("Min rating", "Min votes", "From", "To", "Actor", "Director") with in-box faded placeholders inside compact inputs.
  * **Natural Genre Cloud**: Removed the arbitrary `max-height: 240px` and nested scrollbar, allowing all 19 fixed TMDB genres to fit comfortably in a single glance.

- [x] **Task 1: Movie Poster Badge Cleanup & Scale Fix**
  * **100% Pure Zen Library Shelves**: Suppressed all status badges when viewing Personal Library shelves (Nope, Watched, Favourites, Movie Notes). You already know what shelf you are on, eliminating 100% of repetitive stickers across your personal collection.
  * **Eliminated `UNTRACKED`**: Removed all default untracked badge pills; posters remain clean and unencumbered.
  * **Mockup-Perfect Floating Badges (Discover Mode)**: Positioned frosted dark pills (`rgba(10, 10, 14, 0.90)`) with soft black drop shadow (`box-shadow: 0 2px 8px rgba(0, 0, 0, 0.65)`) at `top: 5px; left: 5px;`.
  * **Off-White Text & Colored Micro-Icons**: Words (DISCOVERY, WATCHED, REWATCH, NOPE, WATCH LATER) render in clean off-white (`#f5f3ee`), while only the front symbol carries color (Yellow dot `Ã¢â‚¬Â¢`, Green check `Ã¢Å“â€œ`, Blue loop `Ã¢â€ Â»`, Red cross `Ã¢Å“â€¢`, Blue clock `Ã¢â€”Â·`).
  * **Zero Bleed & Zero Truncation**: No bleed-through on bright white/yellow posters, and full non-clipping text. Zero hover `+` clutter.

  * **Personal Library Shelf Icons & Ribbon Negative Space**:
    * Injected crisp inline vector SVGs in front of all 5 Personal Library shelf status chips (`New discovery` sparkle, `Watch later` clock, `Watched` check-circle, `Rewatch` refresh-circle, `Nope` ban-circle).
    * Restored full canvas width to `.library-shelf-ribbon` and enforced `margin-left: auto` on `.shelf-view-toggle`, creating wide, calm negative space between the status chips and the `[ Pages | Continuous ]` toggle.
    * Resolved CSS cascade conflict on `.shelf-view-toggle` and applied universal Zen 8px squircle geometry (`border-radius: 8px`, `border-radius: 6px` for inner mode buttons).

  * **Dedicated Favourites Hall of Fame Heart Button**:
    * Replaced the browse mode toggle in `.library-shelf-ribbon` with a dedicated, prominent Heart icon button (`[data-view="favorites"]`).
    * Snapped `.library-shelf-ribbon` to `max-width: 670px !important` so the Heart button sits flush above the 6th poster column, maintaining horizontal alignment with the status chips and separated by ~120px of quiet negative space (never floating into the empty screen void).
    * Floats at the far right edge (`margin-left: auto`) separated by calm negative space from the 5 lifecycle shelf chips (`New discovery`, `Watch later`, `Watched`, `Rewatch`, `Nope`).
    * Features gentle scale on hover and warm crimson illumination (`fill: #eb5757`) with soft glow when viewing Favourites, elevating it to a pure Hall of Fame.
  * **Nope Mode Decoupled from Search Bar & Power Hotkey**:
    * Removed the physical `[ Ã¢Å“â€¢ Nope Mode ]` button from beside the Discover search bar, eliminating the false affordance of a search submit button. The Discover search input now expands smoothly across the full 670px grid width.
    * Added global single-key hotkey **`X`** to instantly toggle Nope Mode when browsing Discover posters (when not focused on a text input), and **`Escape`** to immediately exit.
    * Active Nope Mode is communicated through a quiet, translucent floating status banner at the bottom of the viewport with undo count and hotkey hints.
