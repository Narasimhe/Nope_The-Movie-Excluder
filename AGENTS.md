# Movie Excluder — Agent Directives & Architecture

## Core Architectural Map
- **Backend**: FastAPI routes (`app/main.py`), Business logic & API services (`app/movie_service.py`, `app/grey_service.py`).
- **Database**: SQLite schema (`app/database.py`), Queries (`app/movie_repository.py`, `app/movie_metadata_repository.py`).
- **Frontend**: Vanilla JS (`app/static/app.js`), Modern dark CSS (`app/static/styles.css`), HTML (`app/web/index.html`).
- **AI Cinema Assistant (Grey)**: Decoupled system prompt (`app/prompts/grey_system_prompt.md`), Gemini Flash cascade.
- **Launcher & Roadmap**: 1-click batch launcher (`run.bat`), Central backlog (`docs/IMPROVEMENTS.md`).

## Architectural & Data Invariants
- **Strict Layering**: Keep HTTP routes in `main.py`, orchestration in `*_service.py`, and all SQLite queries isolated in `*_repository.py`.
- **Storage Optimization**: Movies marked as excluded (`NOPE`) must only store their TMDB ID and status flag—never cache poster images or bloated metadata for them.
- **Search Boundaries**: Never scan `.venv/`, `__pycache__/`, or binary `.db` files.

## Non-Negotiable Operational Rules
1. **NO CODE IN CHAT (SILENT FILE EDITS)**: Apply all code changes directly to the files using your editing tools. In the chat window, communicate exclusively in brief, plain English—never dump raw code blocks, diffs, or snippets into the chat unless explicitly asked.
2. **NO UNREQUESTED BROWSER SUBAGENTS**: Never launch the headless browser tool or take verification screenshots unless explicitly asked for visual UI testing.
3. **NO GIT COMMANDS**: Never run `git add`, `git commit`, or `git push` (user manages Git manually). Always preserve existing comments/docstrings and update `docs/IMPROVEMENTS.md` when completing tasks.
4. **BACKEND VERIFICATION**: Run `python -m pytest` (or `run.bat test`) only after modifying backend Python files; skip test runs for pure CSS/HTML/prompt tweaks.
