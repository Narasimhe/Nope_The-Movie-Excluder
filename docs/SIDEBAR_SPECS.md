# Complete Sidebar Design Specification (`SIDEBAR_SPECS.md`)

## 1. Visual Blueprint (Full Expanded Discover Sidebar)

```text
   N O P E   <-- (Header Logo: Left-aligned with 16px inner sidebar margin)

  +-------------------------------------------------------+
  |  [                  See results                    ]  |  <-- Neutral dark button, 1px subtle border
  |                                                       |
  |  FILTERS                                     ↻ Reset  |  <-- Flex space-between, transparent Reset
  |                                                       |
  |  ⇅  Sort Results                                   ▴  |  <-- Flat 50/50 2-Column Grid of 999px Pills
  |  (  Most popular  ) ( Highest rated )                 |
  |  (   Most voted   ) (  Newest first )                 |
  |  (  Oldest first  ) ( *Title A-Z*   )                 |
  |                                                       |
  |  📺 Genres                                         ▴  |  <-- Flex-wrap pills (+ Gold / - Crimson)
  |  ( Action ) ( Adventure ) (- Animation )              |
  |  ( Comedy ) (+ Crime ) (- Documentary )               |
  |  ( Drama ) ( Family ) ( Fantasy ) ...                 |
  |                                                       |
  |  ☆  Rating                                         ▴  |  <-- 2-Col Range Input with "–" separator
  |  [ 6.0             ]  –  [ 10.0            ]          |
  |                                                       |
  |  📊 Minimum Votes                                  ▴  |  <-- Full-width numeric input
  |  [ 200                                     ]          |
  |                                                       |
  |  📅 Release Year                                   ▴  |  <-- 2-Col Range Input with "–" separator
  |  [ 1995            ]  –  [ 2026            ]          |
  |                                                       |
  |  🏷️ Keywords & Themes                              ▴  |  <-- Search Input + Active Tag Pills + Clear
  |  [ Type a keyword or theme...              ]          |
  |  (+ twist ×) (+ whodunit ×)                           |
  |  (+ murder investigation ×)                 Clear all |
  |                                                       |
  |  🌐 Languages                                      ▴  |  <-- Multi-state pills + Hover "×" + "+" adder
  |  (+ English ×) (+ French ×) ( Spanish × )             |
  |  (- Tamil × ) (- Telugu × ) ( Hindi × )   [+]         |
  |                                                       |
  |  📍 Countries                                      ▴  |  <-- Core 10 pills + Hover "×" + "+" adder
  |  ( United States × ) ( United Kingdom × )             |
  |  ( France × ) ( Japan × ) ( India × )     [+]         |
  |                                                       |
  |  👥 Cast & Crew                                    ▴  |  <-- Stacked autocomplete search fields
  |  [ Type an actor name...                   ]          |
  |  [ Type a director name...                ]          |
  |                                                       |
  |  🎬 Studios                                        ▴  |  <-- Autocomplete search field
  |  [ Type a studio (e.g. A24, Warner Bros)...]          |
  |                                                       |
  |  📚 Library Status                                 ▴  |  <-- 2x3 Grid / chips for personal shelves
  |  ( New discovery ) ( Watch later )                    |
  |  ( Watched ) ( Rewatch ) ( Nope ) ( Untracked )       |
  |                                                       |
  |  🔖 Search Profiles                                ▴  |  <-- Saved Presets + 1-Click Remove
  |  ( Atmospheric thrillers × ) ( Prison Whodunits × )   |
  |  [ + Save current search as preset         ]          |  <-- Ghost Slot row with dashed border
  +-------------------------------------------------------+
```

---

## 2. Structural & Layout Architecture

### A. Layout Alignment
- **Header Logo Coordinate Synchronization**:
  - The `N O P E` brand mark in `.topbar` aligns horizontally with the inner content margin of the `.discovery-workspace` card.
  - Calculated as: `padding-left: max(32px, calc((100vw - 1536px) / 2 + 16px))` on `.topbar`.
- **Top Search Row & Poster Grid Alignment**:
  - Top search row spans as a full-width flex container.
  - "Search any movie..." input is stretched to `width: 670px; max-width: 670px;`, aligning its right edge with the 6th poster column.
  - Plain-text movie counter (`.result-count`, `.shelf-movie-count`) is pushed with `margin-left: auto`, vertically aligning with the right edge of the bottom-right Grey pill (`right: 24px;`).
- **Footer Symmetrical Grid Alignment**:
  - `footer` uses a 2-column grid (`grid-template-columns: 310px minmax(0, 1fr)`) matching `.app-layout`.
  - `.footer-identity` (`NOPE / your private movie memory`) has `padding-left: 16px`, aligning with the sidebar inner margin and header logo.
  - `.footer-nav` (`Storage / API`) starts at pixel 310, aligning with the left edge of the 1st poster column.

### B. Outer Card Container (`.discovery-workspace`, `.library-filters-workspace`)
- **Surface**: `background: rgba(15, 15, 18, 0.6)`
- **Border**: `1px solid rgba(255, 255, 255, 0.07)`
- **Border Radius**: `14px`
- **Internal Padding**: `16px`
- **Bottom Margin**: `24px`

---

## 3. Component-by-Component Specifications

### 1. `[ See results ]` Button
- **Placement**: First element inside the card container.
- **Dimensions**: `width: 100%`, `padding: 9px 12px`, `min-height: 34px`.
- **Border & Radius**: `1px solid rgba(255, 255, 255, 0.1)`, `border-radius: 8px`.
- **Typography**: `13px`, `font-weight: 500`, `color: #E5E7EB`.
- **Default State**: Neutral dark `rgba(255, 255, 255, 0.04)` (no muddy yellow/brown tint).
- **Hover State**: `background: rgba(255, 255, 255, 0.08)`, `color: #FFFFFF`, `border-color: rgba(255, 255, 255, 0.2)`.
- **Dirty / Staged State (`.is-dirty`)**: Whisper-clean gold fill (`background: rgba(250, 204, 21, 0.05)`, `border: 1px solid rgba(250, 204, 21, 0.40)`, `color: #FACC15`, `font-weight: 600`).

### 2. Header Row (`FILTERS` & `↻ Reset`)
- **Container**: `display: flex; justify-content: space-between; align-items: center; margin: 16px 0 10px 0; padding: 0;`.
- **`FILTERS` Label**: `font-size: 11px`, `font-weight: 700`, uppercase, `letter-spacing: 0.08em`, `color: #6B7280`.
- **`↻ Reset` Link**: Completely transparent (`background: transparent; border: none; padding: 0;`), `color: #9CA3AF`, `font-size: 12px`, with 12px inline SVG undo icon.
  - **Hover**: Brightens to `#F3F4F6`, icon rotates `-45deg`.
  - **Clean / Dimmed (`.is-dimmed`)**: `opacity: 0.45`, `pointer-events: none`. Automatically activates when any filter is modified.

### 3. Category Accordion Headers (Collapsed by Default)
- **Container Item**: `border: none; border-bottom: none; margin-bottom: 0; padding: 0; width: 100%;`.
- **Trigger Button**:
  - `background: transparent; border: none; padding: 8px 0; width: 100%; display: flex; justify-content: space-between; align-items: center; cursor: pointer;`.
  - Left side: `14px` icon (`#8E8468`, muted antique gold/grey) + `13px` title (`#D1D5DB`, medium weight `500`).
  - Right side: Dim chevron `▾` (`#6B7280`, `11px`).
  - Left alignment: Pixel 0 of content area (flush with `FILTERS` and left edge of `See results`).
  - Yellow notification numbers (`.pill-badge`) are completely hidden.
- **Default State**: All 11 sections start **COLLAPSED** on page load (`display: none !important;`). Only expands on user click.
- **Hover State**: No rectangular background box; text brightens to `#FFFFFF`, icon to `#DEC68B`.
- **Open State (`.is-open`)**: No rectangular background box; text `#FFFFFF` (medium weight `500`), icon stays subtle antique gold `#8E8468`, chevron rotates 180° to `▴` (`#9CA3AF`).

### 4. Unified Flat Zen Pills & Tri-State Mechanic
- **Flat Surface**: All `box-shadow` (including inset) and gradients removed; 100% flat surface.
- **Geometry**: `border-radius: 999px`, `height: 28px`, `padding: 0 10px`, `font-size: 12px`.
- **State 0 — Neutral (Default)**: `background: rgba(255, 255, 255, 0.02)`, `border: 1px solid rgba(255, 255, 255, 0.08)`, `color: #9CA3AF`. No prefix.
- **State 1 — Included (`+`)**: `background: rgba(212, 175, 55, 0.06)`, `border: 1px solid rgba(212, 175, 55, 0.32)`.
  - **Split Contrast**: Prefix `+` in warm gold `#D4AF37` (font-weight 600), label text in soft cream `#E6D5B8`.
- **State 2 — Excluded (`-`)**: `background: rgba(190, 80, 80, 0.06)`, `border: 1px solid rgba(190, 80, 80, 0.30)`.
  - **Split Contrast**: Prefix `-` in dusty rose `#D06B6B` (font-weight 600), label text in muted rose-grey `#D8A8A8`.
- **3-State Cycle Interaction**:
  - Regular click: `Neutral (off)` $\rightarrow$ `Included (+)` $\rightarrow$ `Excluded (-)` $\rightarrow$ `Neutral (off)`.
  - Power-user shortcut: Alt-click or Right-click toggles straight to `Excluded (-)` / `Neutral (off)`.
  - Applied to: **Genres**, **Languages**, **Countries**.
- **2-State Single-Select Radio**: **Sort Results** (Warm gold active, no `+` symbol).
- **2-State Multi-Select Toggle**: **Library Status** (Warm gold active, 50/50 2-column grid, no `+` symbol).

### 5. Sort Results & Search Profiles
- **Sort Results Layout**: 50/50 2-column grid (`grid-template-columns: 1fr 1fr; gap: 6px; padding: 4px 0;`).
- **Sort Results Chips**: 999px pills, 28px height, matching genre pill surface and typography.
- **Search Profiles Chips**:
  - Full consistency with Languages and Themes: 999px pill geometry, `28px` height, `12px` font size, `padding: 0 10px`, `gap: 5px`.
  - **Inline Ribbon Pin Button**: Shows `★` in warm gold (`#D4AF37`) when pinned to the top ribbon, and `☆` in muted grey (`#6B7280`) when in reserve, toggling pin status on click.
  - **Standardized Delete "×"**: Uses the exact same thin 13px glyph `×` (U+00D7) and hover reveal behavior (`opacity: 0` default, `opacity: 0.7` on chip hover, `#CE8484` on button hover) as Languages and Themes.

### 6. Trimmed Countries & Languages + Clean Inline Hover "×"
- **Trimmed Core Lists**:
  - **Countries**: Default top 10 (United States, United Kingdom, France, South Korea, Japan, Germany, Spain, Italy, India, Canada).
  - **Languages**: Default top 8 (English, French, Spanish, Korean, Japanese, German, Italian, Hindi).
  - All 35+ non-primary countries and languages remain cleanly accessible via the `+` chip-adder button.
- **Inline Dismiss Action (`.chip-unpin`)**:
  - Reveals a subtle inline `×` on hover (`opacity: 0.7`, brightening to `1.0` and `#CE8484` on hover).
  - `background: transparent; border: none; padding: 0; margin-left: 5px;` (zero circular grey button background).
  - Dismissing any chip cleanly hides it from the default cloud.

### 7. Clean Keyword & Theme Tag Pills
- **Geometry**: Height `28px`, font size `12px`, padding `0 10px`, `border-radius: 999px`.
- **Surface**: Matches the unified flat active gold (`rgba(212, 175, 55, 0.06)`) or excluded rose (`rgba(190, 80, 80, 0.06)`).
- **Split Contrast**: Prefix `+`/`-` in `#D4AF37` / `#D06B6B`, label text in `#E6D5B8` / `#D8A8A8`.
- **Remove Button**: Murky grey circle removed (`background: transparent; border: none; padding: 0; margin-left: 4px;`). Inline glyph `×` with `opacity: 0.6` brightening to `1.0` and `#DEC68B` / `#CE8484` on hover.

### 8. Numeric & Range Inputs (Rating, Minimum Votes, Release Year)
- **Geometry**: Compact `32px` uniform height, `6px` border-radius.
- **Surface**: `background: rgba(255, 255, 255, 0.03)`, `border: 1px solid rgba(255, 255, 255, 0.08)`, `color: #D1D5DB`, `font-size: 12px`.
- **Focus**: `border-color: rgba(212, 175, 55, 0.4)`, `background: rgba(255, 255, 255, 0.05)`, outline removed.
- **Placeholders**: In-box faded placeholders (`#6B7280`).
- **Spinner Arrows**: Removed via `-webkit-appearance: none` and `-moz-appearance: textfield`.
- **Range Rows (Rating, Release Year)**: 2 inputs aligned on one row with centered `–` separator (`#6B7280`).

### 9. 22px Icon-Only Poster Corner Badges
- **Container**: Standardized `22px × 22px` rounded-square badge (`background: rgba(10, 10, 12, 0.88)`, `border: 1px solid rgba(255, 255, 255, 0.14)`, `backdrop-filter: blur(4px)`, `border-radius: 6px`).
- **Semantic Glyphs**:
  - **New Discovery**: Warm Gold sparkle/star (`#DEC68B`)
  - **Watched**: Emerald checkmark (`#4ADE80`, 2.5px stroke)
  - **Watch Later**: Sky Blue clock (`#38BDF8`)
  - **Rewatch**: Amber loop arrow (`#FB923C`)
  - **Nope**: Dusty Rose ban icon (`#CE8484`)
- **Library Shelves**: Permanently suppressed across all personal library shelf views.

---

## 4. Color & Token Map

| Element | Background | Border | Text / Accent |
| :--- | :--- | :--- | :--- |
| **Card Container** | `rgba(15, 15, 18, 0.6)` | `1px solid rgba(255, 255, 255, 0.07)` | `#E5E7EB` |
| **See Results (Default)** | `rgba(255, 255, 255, 0.04)` | `1px solid rgba(255, 255, 255, 0.1)` | `#E5E7EB` |
| **See Results (Dirty)** | `rgba(212, 175, 55, 0.06)` | `1px solid rgba(212, 175, 55, 0.32)` | `#DEC68B` |
| **Category Header** | `transparent` | `none` | Title: `#D1D5DB`, Icon: `#8E8468` |
| **All Pills (Default State 0)** | `rgba(255, 255, 255, 0.02)` | `1px solid rgba(255, 255, 255, 0.08)` | `#9CA3AF` |
| **Included / Active (State 1)** | `rgba(212, 175, 55, 0.06)` | `1px solid rgba(212, 175, 55, 0.32)` | Symbol: `#D4AF37`, Text: `#E6D5B8` |
| **Excluded (State 2)** | `rgba(190, 80, 80, 0.06)` | `1px solid rgba(190, 80, 80, 0.30)` | Symbol: `#D06B6B`, Text: `#D8A8A8` |
| **Inputs (Numeric / Text)** | `rgba(255, 255, 255, 0.03)` | `1px solid rgba(255, 255, 255, 0.08)` | `#D1D5DB` |
| **Poster Badges (22px)** | `rgba(10, 10, 12, 0.88)` | `1px solid rgba(255, 255, 255, 0.14)` | Status Tone |
