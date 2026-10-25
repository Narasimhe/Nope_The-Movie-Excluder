# Stack-Specific Code Audit & Cleanup Prompts
**Target Architecture:** Python 3.13 + FastAPI + SQLite (WAL) | Vanilla JS (ES2022+) + Custom CSS3 SPA

> **Global Constraint for Antigravity:** 
> "Do not modify any files or write any code yet. Analyze the target files and output a concise, actionable audit report with file names and line numbers."

---

## Phase 1: Dead Code & Orphaned Artifacts

* **1.1. FastAPI Route vs. Frontend Fetch Alignment**
  "Cross-reference all `@app.get/post/put/delete` routes in `app/main.py` against all `fetch()` calls in my Vanilla JS files. List any orphaned backend endpoints that the frontend never calls, and any frontend `fetch()` calls pointing to dead or mismatched URLs."

* **1.2. Pydantic Schema & Repository Pruning**
  "Scan all Pydantic models and `app/*_repository.py` methods. Identify unused Pydantic schemas, fields that are validated but dropped before reaching the database or UI, and repository SQL functions that are never called by `app/movie_service.py` or `app/grey/service.py`."

* **1.3. Vanilla JS & DOM Selector Cleanup**
  "Trace all JS functions, event listeners, and DOM queries (`querySelector`, `getElementById`) against my HTML files. List any unused JS helper functions, event listeners attached to non-existent DOM nodes, and dead URL hash-routing branches."

* **1.4. Custom CSS3 Bloat & Override Audit**
  "Cross-reference my CSS stylesheets against both my HTML templates and dynamic class manipulations (`classList.add/toggle`, `innerHTML`) in my JS files. List all unused CSS classes, dead `--custom-properties`, duplicate media queries, and `!important` declarations created during vibe-coding."

* **1.5. Dependency Manifest Verification**
  "Compare every package in `requirements.txt` against actual `import` statements across `app/` and `tests/`. List any unused packages or transitive leftovers that can be safely removed."

---

## Phase 2: Vibe-Coding Remnants & Temporary Hacks

* **2.1. Debug & Console Artifact Sweep**
  "Scan the entire repo for vibe-coding remnants. List all `print()`, `console.log()`, `console.warn()`, commented-out code blocks, temporary mock payloads, and hardcoded test IDs (like hardcoded TMDB IDs or dummy Gemini prompts)."

* **2.2. Silent Failures & Swallowed Exceptions**
  "Audit all `try...except` blocks in Python and `try...catch` / `.catch()` blocks in JS. Flag any bare `except: pass`, swallowed errors that return silent `None` or `{}` without logging, or generic `500` error catches that mask real bugs in TMDB or Gemini API calls."

* **2.3. Config & Environment Centralization**
  "Find all hardcoded URLs, file paths, SQLite pragma settings, timeouts, magic numbers, and model names (e.g., hardcoded Gemini Flash strings or TMDB base URLs) scattered across `.py` and `.js` files that should be centralized into `.env` or a dedicated config module."

---

## Phase 3: Architectural Drift & Layer Violations

* **3.1. Strict Tier Boundary Enforcement**
  "Audit my 3-tier backend (`app/main.py` -> `*_service.py` -> `*_repository.py`) for layer violations. Flag any business logic or external HTTP calls leaking into `app/main.py`, and any raw `sqlite3` queries or cursor operations happening outside of `app/*_repository.py`."

* **3.2. Async vs. Sync Blocking Audit (FastAPI + `requests`)**
  "Check `app/main.py` and the service tier (`app/movie_service.py`, `app/grey/service.py`) for event-loop blocking. Identify where synchronous `requests.get/post` (to TMDB or Gemini) or synchronous `sqlite3` calls are placed inside `async def` endpoints instead of standard `def` threadpool routes."

* **3.3. Client-Side vs. Server-Side State Duplication**
  "Compare what is stored in browser `localStorage` and `sessionStorage` against what is persisted in SQLite (shelves, notes, search state, history). Point out redundant state synchronization, stale cache traps, or storage keys that are written to `localStorage`/`sessionStorage` but never read back."

---

## Phase 4: Database, Storage & Memory Hygiene

* **4.1. SQLite WAL & Connection Lifecycle Audit**
  "Inspect `app/*_repository.py` for SQLite best practices. Verify that connections and cursors are always closed properly (using context managers), `PRAGMA journal_mode = WAL;` isn't redundantly re-executed on every minor read, and schema migration checks aren't running unnecessarily inside hot loops."

* **4.2. SQLite Schema & Cache Bloat Check**
  "Compare the SQLite table definitions and migration scripts against actual `SELECT`, `INSERT`, and `UPDATE` queries. Identify dead columns, missing indexes on frequently filtered columns (like TMDB IDs or shelf statuses), and cached data (like old payloads or excluded item metadata) that isn't being pruned."

* **4.3. Vanilla JS Memory & Event Listener Leaks**
  "Audit my Vanilla JS view-rendering and hash-routing logic. Identify where re-rendering DOM sections attaches duplicate `addEventListener` callbacks without cleaning up old ones, or where global state objects grow indefinitely during a session."

---

## Phase 5: Pre-Deletion Impact Verification

* **5.1. Blast Radius Check (Run Before Deleting Anything)**
  "I plan to remove or refactor the following items: `[paste items from previous audits]`. Trace all callers, imports, UI bindings, and `pytest` tests connected to these items. Confirm the exact blast radius and verify that no core user flows will break."
