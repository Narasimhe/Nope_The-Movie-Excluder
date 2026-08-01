# Install this update

This update keeps your existing `data/movie_excluder.db`. Do not replace or delete the `data` folder.

1. Stop the running Uvicorn server (`Ctrl+C` in its PowerShell window).
2. Copy the supplied `app`, `docs`, and `tests` folders into your existing `movie-excluder` folder. Choose **Replace** when Windows asks about matching files.
3. Copy this `INSTALL.md` file into the project root if you want to keep these instructions.
4. In PowerShell, from the `movie-excluder` folder, run:

   ```powershell
   python -m app.database
   ```

   This safely adds the new tables and upgrades the official-keyword limit from 5 to 10. Existing movies, statuses, favourites, notes, keywords, and profiles remain in place.

5. Run the complete test suite:

   ```powershell
   python -m unittest discover -s tests -p "test_*.py" -v
   ```

6. Start the app:

   ```powershell
   python -m uvicorn app.main:app --reload
   ```

7. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and press `Ctrl+F5` once so the browser discards the old JavaScript and CSS.

If the database command prints `Using database: ...movie_excluder.db` with no error, the migration succeeded.
