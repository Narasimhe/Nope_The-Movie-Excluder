# Install this update

This update keeps your existing `data/movie_excluder.db`. Never replace or delete that file.

1. Stop the running Uvicorn server (`Ctrl+C` in its PowerShell window).
2. Copy the supplied `app`, `docs`, `tests`, and `scripts` folders into your existing `movie-excluder` folder. Choose **Replace** when Windows asks about matching files.
3. Copy this `INSTALL.md` file into the project root if you want to keep these instructions.
4. Copy `data/demo.db` into the existing `data` folder. It is only a clean public template. **Do not replace `data/movie_excluder.db`.**
5. The app now initializes and migrates the database automatically when Uvicorn starts. You may still run this optional diagnostic from PowerShell:

   ```powershell
   python -m app.database
   ```

   This safely applies the same migrations and prints the working database path. Existing movies, statuses, favourites, notes, keywords, and profiles remain in place.

6. Run the complete test suite:

   ```powershell
   python -m unittest discover -s tests -p "test_*.py" -v
   ```

7. Start the app:

   ```powershell
   python -m uvicorn app.main:app --reload
   ```

8. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and press `Ctrl+F5` once so the browser discards the old JavaScript and CSS.

If the database command prints `Using database: ...movie_excluder.db` with no error, the migration succeeded.

## Fresh public copy

On a genuinely fresh copy, `movie_excluder.db` is absent. The first database access copies `demo.db` once, then the startup migration upgrades that new working copy. After that, only `movie_excluder.db` changes. Later application updates never copy over an existing user database.

To regenerate the public demo template during development:

```powershell
python scripts/build_demo_database.py
```

The script replaces only `data/demo.db`; it never opens or replaces `data/movie_excluder.db`.
