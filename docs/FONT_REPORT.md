# NOPE — Typography Report

*Snapshot taken 24 October 2026. Use it as context when asking an AI (or a designer) for an in-depth typography review or a cleanup plan.*

---

## 1. What this app is

NOPE (Movie Excluder) is a personal movie discovery and journaling web app. It has a dark, cinematic look: a near-black background, warm off-white text and a gold accent colour. The main areas are:

- **Discover**: a poster grid with a large filter sidebar on the left
- **Personal Library**: shelves such as Favourites, Watched and Rewatch
- **Notes**: a journal where you write long-form notes about films, using markdown
- **Movie detail page**: poster, credits, overview and your personal notes
- **Grey**: an AI film assistant that opens as a chat drawer

The frontend is plain HTML, CSS and JavaScript, with no framework. All styling lives in one large stylesheet of about 9,300 lines.

---

## 2. Font in use right now

**One font family is used across the whole app: Inter.**

- Inter is now bundled with the app (self-hosted), so it looks the same on every computer and works offline. Before this, Inter was named in the CSS but never actually loaded, so Windows quietly showed **Segoe UI** instead. That's why the app used to feel like a Windows settings screen.
- The font file is a "variable" version, so it supports every weight from 100 to 900 smoothly. In-between weights like 650 or 750 really do render differently from each other.
- One central setting controls the font for the whole app. Changing that single setting switches everything at once.
- **Fallback order** if Inter fails to load: Manrope, then Segoe UI, then the system font, then any sans-serif.

### Areas checked: every one uses Inter

| Area | Font |
|---|---|
| Logo / wordmark (NOPE) | Inter |
| Top navigation (Discover, Personal Library, Notes) | Inter |
| Left filter sidebar: headings, chips, buttons, inputs | Inter |
| Search bar, Nope Mode toggle, suggestion pills | Inter |
| Poster badges (Untracked, New Discovery) and ratings | Inter |
| Movie detail page: title, credits, overview, notes box | Inter |
| Notes: list cards, reader view, writing editor | Inter |
| Grey assistant: chat messages and input box | Inter |
| Footer and breadcrumbs | Inter |

**The one exception:** slash-command chips inside Grey (such as "/ebert") use a monospace (typewriter-style) font on purpose, so they look like commands.

### Fonts that were tried and rejected
- **Segoe UI** (the old accidental fallback): felt like a Windows system utility rather than a film app.
- **Newsreader** (serif) for notes: rejected for writing because raw markdown and long links looked messy in a serif, and rejected for reading because sans-serif is preferred. It has been removed completely.

---

## 3. Other fonts already bundled (ready to switch to)

These three fonts are already in the app's fonts folder. Switching to one means changing a single setting.

| Font | Personality | Impression so far |
|---|---|---|
| **Manrope** | Warm, slightly rounded, premium, boutique | The user said it "looks much better" than Segoe UI; the strongest contender |
| **Plus Jakarta Sans** | Warm, polished, a little more elegant than Manrope; pairs well with gold | Liked enough to be picked briefly; strong alternative |
| **Geist** | Sharp, precise, modern, a bit techy (Vercel's font) | Clean, but cooler in tone than the film-diary feel |
| **Inter** (current) | Neutral, tall, compact, very readable at small sizes | Safe, professional "app" feel |

### Other options that are not bundled
- **DM Sans**: soft and friendly; heavy weights look less chunky
- **Outfit**: geometric, round, more playful personality
- **Sora**: wide, geometric, bold and slightly futuristic
- **Bebas Neue** or **Oswald**: tall, condensed, movie-poster style. Only suitable as a *display* font for big titles such as the logo or the movie detail heading, never for body text.

---

## 4. Font weights: the main inconsistency

The stylesheet uses **11 different font weights** across about **150 places**. A well-organised design system normally needs only **4 or 5**.

| Weight | Common name | Times used | Notes |
|---|---|---|---|
| 500 | Medium | 14 | Standard |
| 550 | (between Medium and Semibold) | 7 | Non-standard |
| 600 | Semibold | 29 | Standard |
| 620 | (custom) | 1 | One-off; used on @movie mention chips in notes |
| 650 | (between Semibold and Bold) | 12 | Non-standard |
| 700 | Bold | 37 | Most used |
| 750 | (between Bold and Extra-bold) | 22 | Non-standard, used a lot |
| 800 | Extra-bold | 21 | Standard |
| 850 | (custom) | 5 | Non-standard |
| 860 | (custom) | 1 | One-off |
| 950 | (near Black) | 3 | Used on the NOPE logo and a couple of headings |

**Other observations**
- **Regular weight (400) is barely used.** Most body text inherits the default, while nearly every label, button and heading is pushed to 600–800. The app leans heavy, so small text can look dense and shouty.
- **15 weight rules use "!important"**, which means some styles are fighting each other and need to be forced.
- **One weight is set from JavaScript** instead of the stylesheet (movie ratings, bold).
- With Manrope or Plus Jakarta Sans, anything above 800 is capped at 800, so the logo and a few headings would look slightly lighter.

**Suggested target scale:** Regular 400 (body text), Medium 500 (secondary labels), Semibold 600 (buttons, chips, active states), Bold 700 (headings, section titles), Extra-bold 800 (logo and hero titles only).

---

## 5. Font sizes and letter-spacing

- **78 different font sizes** are in use. Almost all are in rem units (which scale properly), and about 20 are fluid sizes that grow and shrink with the screen.
- The **small sizes are badly fragmented**: 0.65, 0.66, 0.68, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.80 and 0.82 rem are all in use. Most of these differences are too small to see, so the UI looks slightly "off" without anyone being able to say why.
- The **smallest text** is the poster status badge (Untracked / New Discovery) at 0.47rem, roughly 7.5px. That's very small and may be hard to read.
- **24 different letter-spacing values** are used, from tight (−0.07em) to very wide (0.2em). About 4 or 5 would be enough.
- No shared variables exist for font sizes, weights or letter-spacing. Colours, corner radius and shadows *do* have shared variables, but typography doesn't, which is why it has drifted.

---

## 6. The left filter sidebar in detail

**Font:** Inter, like everywhere else. What varies is the size and weight of each element.

| Sidebar element | Size | Weight | Notes |
|---|---|---|---|
| Filter section headings (Genres, Rating, Minimum Votes, Sort Results, Release Year, Keywords & Themes, Languages, Countries, Cast & Crew, Studios) | 0.82rem (about 13px) | 700 Bold | Forced with !important, overriding a general rule that says 600 |
| Yellow count badge next to a heading (the "3" next to Genres) | 0.65rem | 850 | Very heavy for a tiny number |
| Expand arrow next to each heading | 0.80rem | 700 | — |
| "See results" button | 0.74rem | 700 | Slight extra letter-spacing |
| "Update" button | 0.72rem | 700 | — |
| "Reset" button | 0.72rem | 600 | Lighter than its neighbours |
| Refresh icon button | 0.80rem | 700 | — |
| Genre / language chips (unselected) | 0.74rem | normal | — |
| Genre / language chips (selected or excluded) | 0.74rem | 600 | — |
| Tri-state chip icons (include / exclude marks) | 0.78rem | 700 | — |
| Number field labels (rating, votes, year) | 0.72rem | 600 | Forced with !important |
| Number field inputs | 0.85rem | 500 | Forced with !important |
| Cast / crew / studio field labels | 0.68rem | normal | — |
| Cast / crew / studio inputs | 0.75rem | normal | — |
| "+" add chip button (languages / countries) | 0.82rem | 700 | — |
| Saved profile buttons | 0.68rem | 600 | — |
| Notes sidebar title | 0.72rem | 800 | Uppercase, wide letter-spacing |
| Library shelf links | 0.73rem | 600 (700 when active) | — |

**Sidebar observations**
- The four action buttons at the top (See results, Update, Reset, Refresh) use **three different sizes and two different weights**, even though they sit side by side.
- Labels in the sidebar range from **0.65rem to 0.85rem** across about ten different sizes.
- The headings are bold (700) and the chips beneath are regular, which gives a clear hierarchy. But the very heavy count badge (850) competes with the heading next to it.

---

## 7. Other notable areas

| Element | Size | Weight | Style |
|---|---|---|---|
| NOPE logo | 1.5rem | 950 | Uppercase, very wide letter-spacing |
| Top navigation tabs | 0.84rem | 650 | Uppercase with letter-spacing in the current design |
| Search input | 1rem | normal | — |
| Search button | — | 800 | — |
| Nope Mode toggle | 0.88rem | 700 | — |
| Poster status badge | 0.47rem | 700 | Uppercase; very small |
| Note card title (notes list) | 1.05–1.25rem | 750 | Slightly tight letter-spacing |
| Note card preview text | 0.90rem | normal | — |
| Note reading body | 1.06rem | normal | Comfortable line height (1.76) |
| Note headings (inside a note) | 1.28–1.6rem | 650–700 | — |
| Bold text inside notes | — | 650 | — |
| Grey chat input | 0.88rem | normal | — |

---

## 8. Summary verdict

| Area | Status |
|---|---|
| Font family | ✅ Consistent: one font everywhere, bundled and self-hosted |
| Font weights | ✅ Standardized: consolidated to 5-step scale (`--weight-regular` 400, `--weight-medium` 500, `--weight-semibold` 600, `--weight-bold` 700, `--weight-heavy` 800) |
| Font sizes | ✅ Standardized: consolidated 78 fragmented sizes into a 9-step semantic scale (`--text-2xs` through `--text-3xl`) |
| Letter-spacing | ✅ Standardized: consolidated 24 ad-hoc values to a 5-step scale (`--tracking-tighter` through `--tracking-widest`) |
| Shared typography variables | ✅ Added: complete set of CSS custom properties in `:root` |
| Sidebar & Badges | ✅ Standardized: sidebar action buttons unified to `--text-sm` & `--weight-semibold`; status badges raised to `--text-2xs` for legibility |

---

## 9. Questions to ask an AI or designer for deeper analysis

1. Given a dark cinematic movie app with a gold accent, which of Inter, Manrope, Plus Jakarta Sans or Geist suits it best, and why?
2. Propose a type scale of 8 to 10 sizes and 5 weights that could replace the current 78 sizes and 11 weights. Show how each existing size would map onto the new scale.
3. Should the app use a separate display font for the logo and movie titles? If so, which one, and where exactly?
4. Is the 0.47rem poster badge too small to be legible? What is a sensible minimum size for badges?
5. How should the sidebar's action buttons and filter headings be standardised so they feel like one system?
6. What letter-spacing should be used for uppercase labels, normal body text and large headings?
7. With a heavy app that rarely uses regular weight, how much should overall weights be lowered to feel more refined without losing hierarchy?
