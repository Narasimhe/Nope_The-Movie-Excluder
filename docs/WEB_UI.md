# Movie Excluder Web UI

Movie Excluder now has a local responsive interface served by the existing
FastAPI application.

## Start it

```powershell
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Swagger remains available at:

```text
http://127.0.0.1:8000/docs
```

## First UI release

- cinematic responsive homepage;
- live TMDB title search;
- poster cards with rating, year, language, status, and favourite state;
- local library navigation for every personal status;
- a main discovery workspace with Simple, Advanced, and Super Advanced modes;
- human-readable genre, language, country, keyword, person, and company filters;
- reusable search profiles with save, update, default, and delete controls;
- selectable personal-status filtering in Super Advanced mode;
- favourites list;
- full-page movie details with a back button and properly contained poster;
- status and favourite controls kept near the top of the detail page;
- naturally wrapped movie descriptions;
- genres and keywords displayed together in one metadata row;
- favourite control placed directly below the status control;
- editable personal notes below the main movie information;
- status changes;
- favourite and unfavourite actions.

The UI uses the existing API and SQLite database. It does not create a second
database or duplicate any movie logic.
