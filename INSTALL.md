# Movie Excluder UI — Version 1

Copy the `app`, `docs`, and `tests` folders into the root of your
`movie-excluder` project. Allow Windows to replace matching files.

Run the UI test:

```powershell
python -m unittest discover -s tests -p "test_web_ui.py" -v
```

Start Movie Excluder:

```powershell
python -m uvicorn app.main:app --reload
```

Open the app:

```text
http://127.0.0.1:8000
```

Swagger remains available at:

```text
http://127.0.0.1:8000/docs
```

No database migration is required.
