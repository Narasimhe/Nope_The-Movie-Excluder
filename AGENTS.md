# Movie Excluder — Agent Directives & Architecture

## Core Architectural Map
- **Backend**: FastAPI (`app/main.py`), Services (`app/movie_service.py`, `app/grey_service.py`).
- **Database**: SQLite (`app/database.py`, `app/movie_repository.py`, `app/movie_metadata_repository.py`).
- **Frontend**: Vanilla JS (`app/static/app.js`), Modern dark CSS (`app/static/styles.css`), HTML (`app/web/index.html`).
- **AI Cinema Assistant (Grey)**: Decoupled plain-text prompt (`app/prompts/grey_system_prompt.md`), Gemini Flash cascade.
- **Launcher**: Single 1-click batch launcher (`run.bat`).
- **Roadmap & Records**: Central improvements backlog (`docs/IMPROVEMENTS.md`).

## Non-Negotiable Operational Rules
1. **STRICTLY NO CODE IN CHAT RESPONSES**: Communicate exclusively in plain English. Never output raw code blocks, diffs, or code snippets in the chat conversation unless explicitly demanded by the user.
2. **NO UNREQUESTED BROWSER SUBAGENTS**: Never launch the headless Chrome browser subagent or take verification screenshots unless the user explicitly asks for visual UI testing.
3. **DOCUMENTATION & GIT INTEGRITY**:
   - Preserve all existing code comments, docstrings, and architectural patterns.
   - Checkpoint working changes cleanly to git and push to `origin main`.
   - Keep `docs/IMPROVEMENTS.md` updated with completed items and queued feature notes.
4. **TEST SUITE VERIFICATION**:
   - Run verification via `python -m pytest` or `run.bat test` after making backend changes.
5. **NOTION TOGGLE FORMATTING**:
   - In notes, journal entries, and Grey drafts, always use Notion-style toggles `>> Title (Year)`. Never use raw HTML `<details>` or `<summary>`.
6. **SHELF INTEGRITY & ZERO CONFUSION**:
   - The 5 canonical shelves are: `new_discovery`, `watch_later`, `rewatch`, `watched`, and `excluded` (Nope).
   - If the user mentions "post", "note", "journal", or "draft", it is strictly a Journal Note operation—never confuse it with a shelf status change.
