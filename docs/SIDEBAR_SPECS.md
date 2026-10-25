# Complete Sidebar Design Specification (`SIDEBAR_SPECS.md`)

## 1. Visual Blueprint (Full Expanded Discover Sidebar)

```text
   N O P E   <-- (Header Logo: Left-aligned with 16px inner sidebar margin)

  +-------------------------------------------------------+
  |  [                  See results                    ]  |  <-- Neutral dark button, 1px subtle border
  |                                                       |
  |  FILTERS                                     ↻ Reset  |  <-- Flex space-between, transparent Reset
  |                                                       |
  |  ⇅  Sort Results                                   ▴  |  <-- 2-Column Grid for Sort options
  |  [  Most popular  ] [ Highest rated ]                 |
  |  [   Most voted   ] [  Newest first ]                 |
  |  [  Oldest first  ] [ *Title A-Z*   ]                 |
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
  |  🌐 Languages                                      ▴  |  <-- Multi-state pills + "+" expand button
  |  (+ English) (+ French) ( Spanish )                   |
  |  (- Tamil ) (- Telugu ) ( Hindi ) [+]                 |
  |                                                       |
  |  📍 Countries                                      ▴  |  <-- Multi-state pills + "+" expand button
  |  ( United States ) ( United Kingdom )                 |
  |  ( Canada ) ( Australia ) ( Germany ) [+]             |
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
- **Double-Wall Removal**:
  - `.sidebar` has `border-right: none`, letting the floating card float in calm negative space.
  - Category rows have no bottom divider lines (`border-bottom: none`).

### B. Outer Card Container (`.discovery-workspace`, `.library-filters-workspace`)
- **Surface**: `background: rgba(15, 15, 18, 0.6)`
- **Border**: `1px solid rgba(255, 255, 255, 0.07)`
- **Border Radius**: `14px`
- **Internal Padding**: `16px`
- **Bottom Margin**: `24px`

---

## 3. Component-by-Component Specifications

### 1. `[ See results ]` Button
- **Placement**: Pinned as the first element inside the card container.
- **Dimensions**: `width: 100%`, `padding: 9px 12px`, `min-height: 34px`.
- **Border & Radius**: `1px solid rgba(255, 255, 255, 0.1)`, `border-radius: 8px`.
- **Typography**: `13px`, `font-weight: 500`, `color: #E5E7EB`.
- **Default State**: Neutral dark `rgba(255, 255, 255, 0.04)` (no muddy yellow/brown tint).
- **Hover State**: `background: rgba(255, 255, 255, 0.08)`, `color: #FFFFFF`, `border-color: rgba(255, 255, 255, 0.2)`.
- **Dirty / Staged State (`.is-dirty`)**: Warm gold illumination (`background: rgba(250, 204, 21, 0.1)`, `border: 1px solid rgba(250, 204, 21, 0.45)`, `color: #FACC15`, `font-weight: 600`).

### 2. Header Row (`FILTERS` & `↻ Reset`)
- **Container**: `display: flex; justify-content: space-between; align-items: center; margin: 16px 0 10px 0; padding: 0;`.
- **`FILTERS` Label**: `font-size: 11px`, `font-weight: 700`, uppercase, `letter-spacing: 0.08em`, `color: #6B7280`.
- **`↻ Reset` Link**: Completely transparent (`background: transparent; border: none; padding: 0;`), `color: #9CA3AF`, `font-size: 12px`, with 12px inline SVG undo icon.
  - **Hover**: Brightens to `#F3F4F6`, icon rotates `-45deg`.
  - **Clean / Dimmed (`.is-dimmed`)**: `opacity: 0.45`, `pointer-events: none`. Automatically activates when any filter is modified.

### 3. Category Accordion Headers
- **Container Item**: `border: none; border-bottom: none; margin-bottom: 0; padding: 0; width: 100%;`.
- **Trigger Button**:
  - `background: transparent; border: none; padding: 10px 0; width: 100%; display: flex; justify-content: space-between; align-items: center; cursor: pointer;`.
  - Left side: `14px` icon (`#9CA3AF`) + `13px` title (`#D1D5DB`, regular weight `400`).
  - Right side: Dim chevron `▾` (`#6B7280`, `11px`).
  - Left alignment: Pixel 0 of content area (flush with `FILTERS` and left edge of `See results`).
  - Yellow notification numbers (`.pill-badge`) are completely hidden.
- **Hover State**: No rectangular background box; text brightens to `#FFFFFF`, icon to `#E5E7EB`.
- **Open State (`.is-open`)**: No rectangular background box; text `#FFFFFF` (medium weight `500`), icon lights up in warm gold `#FACC15`, chevron rotates 180° to `▴`.

### 4. Sort Results
- **Layout**: 50/50 2-column grid (`grid-template-columns: 1fr 1fr; gap: 6px; padding: 4px 0;`).
- **Chips**: `height: 32px`, `border-radius: 6px`, `font-size: 12px`, `background: rgba(255, 255, 255, 0.03)`, `border: 1px solid rgba(255, 255, 255, 0.08)`, `color: #9CA3AF`.
- **Active Chip**: `background: rgba(250, 204, 21, 0.1)`, `border: 1px solid rgba(250, 204, 21, 0.45)`, `color: #FACC15`.

### 5. Genres
- **Container**: Natural cloud (`display: flex; flex-wrap: wrap; gap: 6px; padding: 4px 0; overflow-y: visible; max-height: none;`). Zero scrollbars.
- **Pills**: `border-radius: 999px`, `padding: 4px 10px`, `font-size: 12px`.
- **Default (Unselected)**: `background: rgba(255, 255, 255, 0.03)`, `border: 1px solid rgba(255, 255, 255, 0.08)`, `color: #9CA3AF`.
- **Included (`+`)**: `background: rgba(250, 204, 21, 0.1)`, `border: 1px solid rgba(250, 204, 21, 0.45)`, `color: #FACC15`.
- **Excluded (`−`)**: `background: rgba(239, 68, 68, 0.1)`, `border: 1px solid rgba(239, 68, 68, 0.4)`, `color: #F87171`.

### 6. Numeric & Range Inputs (Rating, Minimum Votes, Release Year)
- **Geometry**: Compact `32px` uniform height, `6px` border-radius.
- **Surface**: `background: rgba(255, 255, 255, 0.03)`, `border: 1px solid rgba(255, 255, 255, 0.08)`, `color: #D1D5DB`, `font-size: 12px`.
- **Focus**: `border-color: rgba(250, 204, 21, 0.5)`, `background: rgba(255, 255, 255, 0.05)`, outline removed.
- **Placeholders**: In-box faded placeholders (`#6B7280`).
- **Spinner Arrows**: Removed via `-webkit-appearance: none` and `-moz-appearance: textfield`.
- **Range Rows (Rating, Release Year)**: 2 inputs aligned on one row with centered `–` separator (`#6B7280`).

### 7. Keywords & Themes
- **Search Input**: Full-width 32px autocomplete field with in-box placeholder.
- **Selected Tag Pills**: 999px pills with `+` inclusion (Gold) or `−` exclusion (Crimson) and inline `×` removal button.
- **Empty State**: Container collapses with 0 margin/padding when empty.
- **Clear All**: Quiet right-aligned link to wipe active keyword tags.

### 8. Languages & Countries
- **Natural Clouds**: Zero scrollbars, 999px pills wrapping naturally.
- **Multi-State Toggles**: Unselected, Included (Gold), Excluded (Crimson).
- **Expand Button (`+`)**: Compact chip at end of cloud to reveal remaining entries.

### 9. Cast & Crew
- **Stacked Structure**: Actor field above Director field.
- **Inputs**: 32px squircle inputs with in-box placeholders.
- **Filmography Link**: Clicking an actor/director tag opens their dedicated career dossier.

### 10. Studios
- **Autocomplete Input**: 32px squircle input (`Type a studio (e.g. A24, Warner Bros)...`).

### 11. Library Status
- **2x3 Grid**: Sleek 999px pills for `New discovery`, `Watch later`, `Watched`, `Rewatch`, `Nope`, `Untracked`.

### 12. Search Profiles
- **Saved Preset Chips**: Compact 999px chips with active preset illuminated in warm gold (`#FACC15`) and inactive presets in quiet grey (`#9CA3AF`). Subtle `×` on hover for 1-click removal.
- **Ghost Slot Save Link**: Full-width row with dashed border (`1px dashed rgba(255, 255, 255, 0.15)`), 8px radius, `+ Save current search as preset`, warming to gold on hover.
- **Redundant Dropdown & Dividers**: Permanently removed.

---

## 4. Color & Token Map

| Element | Background | Border | Text |
| :--- | :--- | :--- | :--- |
| **Card Container** | `rgba(15, 15, 18, 0.6)` | `1px solid rgba(255, 255, 255, 0.07)` | `#E5E7EB` |
| **See Results (Default)** | `rgba(255, 255, 255, 0.04)` | `1px solid rgba(255, 255, 255, 0.1)` | `#E5E7EB` |
| **See Results (Dirty)** | `rgba(250, 204, 21, 0.1)` | `1px solid rgba(250, 204, 21, 0.45)` | `#FACC15` |
| **Category Header** | `transparent` | `none` | `#D1D5DB` (Hover: `#FFF`) |
| **Pill (Default)** | `rgba(255, 255, 255, 0.03)` | `1px solid rgba(255, 255, 255, 0.08)` | `#9CA3AF` |
| **Pill (Included / Active)** | `rgba(250, 204, 21, 0.1)` | `1px solid rgba(250, 204, 21, 0.45)` | `#FACC15` |
| **Pill (Excluded)** | `rgba(239, 68, 68, 0.1)` | `1px solid rgba(239, 68, 68, 0.4)` | `#F87171` |
| **Inputs (Numeric / Text)** | `rgba(255, 255, 255, 0.03)` | `1px solid rgba(255, 255, 255, 0.08)` | `#D1D5DB` |

---

## 5. Cross-Pane Symmetry (Personal Library & Notes)
- Symmetrical tokens apply across `#sidebar-pane-discover`, `#sidebar-pane-library`, and `#sidebar-pane-notes`.
- All divider lines are eradicated globally.
- Both Discover and Library use the identical `FILTERS / ↻ Reset` header geometry.
