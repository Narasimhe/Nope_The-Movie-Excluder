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
- favourites list;
- movie details dialog with genres and keywords;
- status changes;
- favourite and unfavourite actions.

The UI uses the existing API and SQLite database. It does not create a second
database or duplicate any movie logic.
