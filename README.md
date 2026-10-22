<div align="center">

# 🎬 NOPE (Movie Excluder)

**The local-first cinema curator built for ruthless exclusion.**

*Filter out the noise, reject the slop, and keep an honest, private film diary with an AI assistant that actually has taste.*

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![TMDB API](https://img.shields.io/badge/TMDB-01d277?style=flat&logo=themoviedatabase&logoColor=white)](https://www.themoviedb.org/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=flat&logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

<!-- Dedicated Screenshots & Demo Preview (Coming Soon) -->

## 👁️ Why NOPE?

Most movie apps try to show you **everything**. They push algorithmic hype, sponsored recommendations, and endless scrolling catalogs of mediocre titles.

**NOPE is built on the philosophy of ruthless exclusion.**

Your viewing time is finite. NOPE gives you a high-performance, private canvas to actively reject movies you never want to see, pinpoint genuine gems using deep multi-vector search, and log your thoughts in clean, human-readable notes—backed by **Grey**, an AI cinema assistant that actually respects your intelligence.

---

## ✨ Core Features

### 🎯 1. Ruthless Exclusion & Personal Shelves
- **Nope with One Click**: Reject a film and it vanishes from future discovery searches forever.
- **Dedicated Shelves**: Organize your cinema journey across **Watched**, **Watch Later**, **Rewatch**, **New Discovery**, and **Nope (Excluded)**.
- **1–10 Verdicts**: Score movies on your terms without noisy public crowd averages getting in your way.

### 🔍 2. Super Advanced Multi-Vector Discovery
- **Deep Film Filtering**: Filter by intersecting genres, keyword tags, origin countries, release decades, actor/director filmographies, and vote counts.
- **Quick-Access Ribbon Chips**: Pin and save your favorite complex search profiles (e.g. *70s Paranoia Thrillers*, *Nordic Noir*, *Sci-Fi*) for one-click discovery.
- **Career Filmography Explorer**: Click any director or actor to browse their complete career timeline with department tabs (Directing, Acting) and your personal watch badges.

### 🐾 3. Grey — The AI Cinema Assistant
- **Craft Over Genre**: Grey evaluates films strictly by script craft, pacing, tension, atmosphere, and audience respect. No corporate fluff, no pleasantries—just honest, decisive **YES** or **NOPE** reality checks.
- **Real-Time Screen Awareness**: Grey sees what movie, filmography, or note you are actively viewing on your screen.
- **Modular Skill Architecture**: Grey dynamically loads dedicated skill modules on-demand:
  - `notes_editor`: In-place note upserts, formatting mimicry, and clean Notion-style `>>` toggles.
  - `related_curator`: Script pacing and tension reality checks for related movie carousels.
  - `filmography_explorer`: Deep career context and essential film highlights.
  - `watchlist_builder`: Synthesizes full 8–12 movie tranches from your pending queue into expandable toggles.
  - `library_ops`: Shelf transitions, ratings, verdicts, and batch moves.

### 📝 4. Human-Readable Notes & Film Journal
- **Clean Notion-Style Toggles**: Write collapsible critiques and watchlist summaries using clean `>> Title (Year)` syntax without clumsy raw HTML.
- **Format Mimicry**: Grey inspects your established formatting and matches your exact style—whether you use single-line bullets (`• Title (Year) - [IMDb](url)`) or expandable toggles.
- **Zero Redundancy**: Intelligent in-place upserting guarantees that movie titles appear strictly once per note document.

### ⚡ 5. Local-First, Blazing Fast & Privacy-Focused
- **100% Local SQLite Database**: Your ratings, watched history, excluded titles, and personal notes stay entirely on your computer.
- **Offline Poster Cache**: Discovered posters are cached locally on disk with immutable headers; browsing your saved library works offline in under **2ms**.
- **Featherweight Footprint**: Built with Vanilla JS and FastAPI—uses **0% idle CPU** and less than **100MB of RAM** total.

---

## 🚀 Quick Start (60 Seconds)

### Prerequisites
- Python 3.10 or higher
- A free [TMDB API Read Access Token](https://www.themoviedb.org/settings/api)
- *(Optional)* A free [Google Gemini API Key](https://aistudio.google.com/) (to chat with Grey)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/movie-excluder.git
cd movie-excluder
```

### 2. Configure Environment Variables
Create a `.env` file in the root folder (or copy `.env.example`):
```env
TMDB_READ_ACCESS_TOKEN=your_tmdb_bearer_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Launch the App (Windows)
Double-click `run.bat` or run:
```powershell
.\run.bat install
.\run.bat start
```

### Alternative Launch (macOS / Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000). 

*On first launch, NOPE automatically generates a clean, pristine local SQLite database on your machine.*

---

## 🛠️ CLI Launcher Commands

| Command | Description |
| :--- | :--- |
| `.\run.bat start` | Launches the local FastAPI server and web UI |
| `.\run.bat test` | Runs the automated pytest suite (228+ unit & integration tests) |
| `.\run.bat install` | Installs or updates project Python dependencies |
| `.\run.bat init` | Initializes or safely migrates the local SQLite database schema |

---

## 🏗️ Architecture

```
movie-excluder/
├── app/
│   ├── main.py                     # FastAPI routes & static file mounting
│   ├── movie_service.py            # Library curation & search orchestration
│   ├── grey_service.py             # Grey AI service & dynamic skill router
│   ├── tmdb_client.py              # Resilient TMDB client with circuit breakers
│   ├── poster_cache_service.py     # Local-first disk image caching & offline circuit
│   ├── database.py                 # SQLite bootstrap & idempotent schema migrations
│   ├── prompts/
│   │   ├── grey_core.md            # Base cinephile persona & JSON output schema
│   │   └── skills/                 # On-demand modular capabilities (notes, related, etc.)
│   ├── static/                     # Vanilla JS (app.js) & Modern Dark CSS (styles.css)
│   └── web/                        # Responsive single-page application (index.html)
├── data/                           # Local SQLite database & cached posters (git-ignored)
├── docs/                           # Central roadmap & backlog (IMPROVEMENTS.md)
└── tests/                          # Comprehensive pytest test suite
```

---

## 🔒 Privacy & Ownership

- **No telemetry, no trackers, no accounts required.**
- Your database (`movie_excluder.db`), cached posters, and personal notes are ignored by Git and never leave your machine.
- Pulling code updates in the future will **never overwrite or wipe your personal data**.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
