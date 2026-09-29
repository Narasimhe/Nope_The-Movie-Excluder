# Movie Excluder

A personal movie-discovery and watch-status app powered by FastAPI, SQLite,
and TMDB metadata.

## Quick start (Windows)

Run these commands from the project folder:

```powershell
.\run.bat install
.\run.bat start
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000). The first startup
creates or safely migrates the local SQLite database automatically.

`run.bat` uses `.venv\Scripts\python.exe` when a project virtual environment
exists; otherwise, it uses the Python launcher (`py -3`).

## Common commands

```powershell
.\run.bat start   # Start the development server (the default)
.\run.bat init    # Initialize or migrate the database only
.\run.bat test    # Run the automated tests
.\run.bat install # Install or update project dependencies
```

Press `Ctrl+C` in the terminal to stop the development server.
