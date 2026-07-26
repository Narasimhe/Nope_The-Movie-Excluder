# Personal Movie Status Model

Each movie now has one primary personal status:

- `new_discovery`
- `watch_later`
- `watched`
- `rewatch`
- `excluded`

The status can be changed freely in any direction. Changing it updates the
existing `user_movie_data` row and preserves `notes` and `verdict` (the
personal rating).

If notes or a rating are added before a status is chosen, the movie is stored
as `new_discovery`.

## Existing database migration

`initialize_database()` automatically converts the older four-flag model to
the single-status model.

If an old row contains multiple active flags, this priority is used:

1. `excluded`
2. `rewatch`
3. `watched`
4. `watch_later`
5. `new_discovery`

The migration retains the TMDB ID, notes, personal rating, and update time.

## Verification

Run the focused tests from the project root:

```powershell
python -m unittest discover -s tests -p "test_personal_movie_status.py" -v
```
