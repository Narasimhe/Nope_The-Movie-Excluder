# Changelog

All notable changes to Movie Excluder are documented here.

---

# v0.1.0 - Core Architecture Complete
Date: 2026-07-25

## Added

### Project Structure
- Established project architecture
- Created application modules
- Added test structure

### Database
- SQLite database
- Database initialization
- Movies table
- User movie data table

### TMDB Integration
- TMDB client
- Movie metadata retrieval
- Local caching

### Repositories
- MovieRepository
- UserMovieRepository

### Service Layer
- MovieService

### User Movie Data
- Watchlist
- Watched
- Rewatch
- Excluded (NOPE)
- Verdict
- Notes

### Testing
- Database tests
- MovieRepository tests
- UserMovieRepository tests

---

## Next Milestone (v0.2.0)

- Business rules
- Watchlist logic
- Watched logic
- Rewatch logic
- Excluded (NOPE) logic
- Service layer refinement

# Changelog

All notable changes to Movie Excluder are documented here.

---

# v0.1.0 - Core Architecture Complete
Date: 2026-07-25

## Added

### Project Structure
- Established project architecture
- Created application modules
- Added test structure

### Database
- SQLite database
- Database initialization
- Movies table
- User movie data table

### TMDB Integration
- TMDB client
- Movie metadata retrieval
- Local caching

### Repositories
- MovieRepository
- UserMovieRepository

### Service Layer
- MovieService

### User Movie Data
- Watchlist
- Watched
- Rewatch
- Excluded (NOPE)
- Verdict
- Notes

### Testing
- Database tests
- MovieRepository tests
- UserMovieRepository tests

---

## Next Milestone (v0.2.0)

- Business rules
- Watchlist logic
- Watched logic
- Rewatch logic
- Excluded (NOPE) logic
- Service layer refinement

## [Milestone 4] - Discovery Filtering Pipeline

### Added
- Added `UserMovieRepository.get_watched_movie_ids()`.
- Added `UserMovieRepository.get_excluded_movie_ids()`.
- Added `MovieService._filter_discovery_results()` to remove watched and excluded movies from discovery results.
- Added business-rule tests for repository query methods.
- Added end-to-end search filtering tests using a fake repository.

### Changed
- `MovieService.search_movies()` now filters both cached and TMDB search results before returning them.
- Discovery searches now automatically hide movies marked as Watched or NOPE.

### Architecture
- Discovery filtering is now enforced by the service layer rather than the UI.
- All search paths (SQLite cache and TMDB API) now follow the same filtering pipeline.