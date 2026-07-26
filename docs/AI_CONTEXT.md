# AI Context

Current Version: v0.2

---

# Project Summary

Movie Excluder is a Windows desktop application that helps users discover movies by excluding titles they have already watched, blacklisted, or filtered out based on personal preferences.

SQLite is the application's source of truth.

TMDB is used only as a metadata provider.

---

# Current Status

## Completed

- Git repository initialized
- Project documentation
- TMDB API integration
- SQLite database initialized
- Database schema designed
- Data ownership defined
- Repository standardized to `main`

## Current Focus

Connecting TMDB with SQLite so every retrieved movie is stored locally before being used by the application.

## Next Development Step

Build the local movie cache.

Expected workflow:

1. Search TMDB
2. Select a movie
3. Fetch complete metadata
4. Insert or update the `movies` table
5. Retrieve movies from SQLite

---

# Architecture

```
TMDB
      │
      ▼
SQLite Database
      │
      ▼
Application Logic
      │
      ▼
Future Desktop UI
```

---

# Data Ownership

## TMDB owns

- Movie metadata
- Posters
- Backdrops
- Release dates
- Overviews
- Ratings

## SQLite owns

- Cached movie metadata
- Application database

## User owns

- Watched status
- Blacklist
- Watchlist
- Personal rating
- Review
- Notes

The two database tables are linked using `tmdb_id`.

---

# Database

## movies

Stores factual movie information retrieved from TMDB.

## user_movie_data

Stores the user's personal interaction with each movie.

---

# Project Structure

```
movie-excluder/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── test_database.py
│   ├── test_tmdb.py
│   └── tmdb_client.py
├── assets/
├── docs/
│   ├── AI_CONTEXT.md
│   └── PROJECT_VISION.md
├── tests/
├── .env
├── .gitignore
├── movie_excluder.db
└── README.md
```

---

# Git Status

- Active branch: `main`
- Remote tracking branch: `origin/main`
- Repository is synchronized.

---

# Future Roadmap

1. Local movie cache
2. User movie status management
3. Exclusion engine
4. Recommendation pipeline
5. Desktop UI

## Current Status

Completed

- SQLite database foundation
- TMDB client
- Repository layer
- User movie data management
- Search V1
- TMDB search integration
- Bulk user data merging

Current Focus

Movie Details endpoint

Next

- Movie details retrieval
- Metadata caching
- Classification actions
- personal libraries