# NOPE (Movie Excluder)

A lightweight, local-first movie library and discovery app. Mark movies you don't want to see so they never show up in searches again, track your shelves, take notes, and explore films with an AI assistant.

---

<!-- Screenshots coming soon -->

---

## Features

- **Exclusion System**: Mark movies as *Nope* to permanently filter them out of discovery searches.
- **Shelves**: Organize titles into *Watched*, *Watch Later*, *Rewatch*, and *Nope*.
- **Advanced Search**: Filter by genres, release year, origin country, keywords, actors, and directors. Save custom search presets to quick-access chips.
- **Filmography Explorer**: Browse full timelines for directors and actors with role tabs and personal watch badges.
- **Notes & Journal**: Write personal movie notes and watchlists with collapsible Notion-style (`>>`) toggles and markdown support.
- **Grey (AI Assistant)**: Context-aware assistant powered by Gemini that answers film questions, evaluates scripts/pacing, and updates your notes directly.
- **Local-First & Offline**: Uses a local SQLite database and caches movie posters locally. Runs fast and works offline for saved titles.

---

## Quick Start

### Prerequisites
- Python 3.10+
- A free [TMDB API Token](https://www.themoviedb.org/settings/api)
- *(Optional)* A [Google Gemini API Key](https://aistudio.google.com/) for Grey AI

### 1. Setup
```bash
git clone https://github.com/Narasimhe/Movie-Excluder.git
cd Movie-Excluder
```

Create a `.env` file in the root directory:
```env
TMDB_READ_ACCESS_TOKEN=your_tmdb_token_here
GEMINI_API_KEY=your_gemini_key_here
```

### 2. Run

**Windows:**
```powershell
.\run.bat install
.\run.bat start
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Commands (`run.bat`)

| Command | Action |
| :--- | :--- |
| `.\run.bat start` | Start the local server |
| `.\run.bat test` | Run the pytest suite |
| `.\run.bat install` | Install/update Python dependencies |
| `.\run.bat init` | Initialize or migrate SQLite database |

---

## Project Structure

```
movie-excluder/
├── app/
│   ├── main.py                     # FastAPI routes & static file server
│   ├── movie_service.py            # Library curation & search logic
│   ├── grey_service.py             # Grey AI integration & skill routing
│   ├── tmdb_client.py              # TMDB API client
│   ├── poster_cache_service.py     # Local poster disk caching
│   ├── database.py                 # SQLite bootstrap & migrations
│   ├── prompts/                    # Grey prompts and skills
│   ├── static/                     # JavaScript (app.js) & CSS (styles.css)
│   └── web/                        # HTML UI (index.html)
├── data/                           # Local database & cached images (git-ignored)
├── docs/                           # Backlog & tasks (IMPROVEMENTS.md)
└── tests/                          # Automated tests
```

---

## Data & Privacy

All personal data (database `movie_excluder.db`, personal notes, ratings, and cached posters) stays locally in `data/` and is ignored by Git. Pulling updates will never overwrite your personal library.

---

## License

[MIT](LICENSE)
