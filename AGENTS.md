# Movie Excluder — Agent Directives & Architecture

## Core Architectural Map
- **Backend**: FastAPI routes (`app/main.py`), Business logic & API services (`app/movie_service.py`), AI Cinema Assistant (`app/grey/service.py`, `app/grey/prompts/`).
- **Database**: SQLite schema (`app/database.py`), Queries (`app/movie_repository.py`, `app/movie_metadata_repository.py`).
- **Frontend**: Vanilla JS (`app/static/app.js`), Modern dark CSS (`app/static/styles.css`), HTML (`app/web/index.html`).
- **AI Cinema Assistant (Grey)**: Decoupled package (`app/grey/`), prompt cascade (`app/grey/prompts/`), Gemini Flash cascade.
- **Launcher & Roadmap**: 1-click batch launcher (`run.bat`), Central backlog (`docs/IMPROVEMENTS.md`).

## Architectural & Data Invariants
- **Strict Layering**: Keep HTTP routes in `main.py`, orchestration in `*_service.py`, and all SQLite queries isolated in `*_repository.py`.
- **Storage Optimization**: Never cache poster images on disk for excluded (`NOPE`) or untracked discovery titles (posters stream directly via TMDB Cloudflare CDN). Disk poster caching is reserved exclusively for personal library shelves. Text metadata (credits, directors, keywords) in SQLite is preserved so movie details remain fully viewable.
- **Search Boundaries**: Never scan `.venv/`, `__pycache__/`, or binary `.db` files.

## Non-Negotiable Operational Rules
1. **NO CODE IN CHAT (SILENT FILE EDITS)**: Apply all code changes directly to the files using your editing tools. In the chat window, communicate exclusively in brief, plain English—never dump raw code blocks, diffs, or snippets into the chat unless explicitly asked.
2. **NO UNREQUESTED BROWSER SUBAGENTS**: Never launch the headless browser tool or take verification screenshots unless explicitly asked for visual UI testing.
3. **NO GIT COMMANDS**: Never run `git add`, `git commit`, or `git push` (user manages Git manually). Always preserve existing comments/docstrings and update `docs/IMPROVEMENTS.md` when completing tasks.
4. **BACKEND VERIFICATION**: Run `python -m pytest` (or `run.bat test`) only after modifying backend Python files; skip test runs for pure CSS/HTML/prompt tweaks.

## CSS Guidelines
- NEVER use `!important`. If a rule doesn't apply, fix the selector specificity or nesting order.
- NEVER use raw hex or rgb colors in component rules. Every color MUST use an existing `var(--token-name)`.
- Never append duplicate selector blocks. Inspect the existing classes in the file and edit them in-place.

### Color & Styling Guardrails
- NEVER invent new hex or rgb color codes.
- NEVER add new shades of yellow or gold. All active states, highlights, badges, and accents must exclusively use `var(--accent-primary)`, `var(--accent-subtle)`, or `var(--accent-text)`.
- If an element needs an active or highlighted look, use `var(--accent-primary)` for borders/icons, `var(--accent-subtle)` for backgrounds, and `var(--accent-text)` for text.
