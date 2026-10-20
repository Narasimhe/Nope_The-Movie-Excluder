# Database Health, Caching & Smart Maintenance Specification

## 1. Executive Summary & Purpose

Movie Excluder relies on a local SQLite database (`data/movie_excluder.db`) as its absolute source of truth. TMDB serves strictly as an external metadata provider.

To ensure long-term speed, data integrity, and low disk footprint across years of active use, this document specifies the **Database Health and Smart Maintenance** lifecycle.

---

## 2. Current Caching Behavior (v0.2 Baseline)

The application currently operates under a lean, local-first paradigm:

- **Ephemeral Search**: Raw search results are not permanently stored in SQLite until a title is opened or actioned.
- **On-Demand Detail Caching**: When a movie detail page is viewed, its overview, director, cast, and TMDB path references are saved to SQLite to enable instant 0ms subsequent views and offline availability.
- **No Binary Media Storage**: Image posters and video assets are never saved locally as binary BLOBs; only string image paths are retained, keeping the SQLite database small (tens of megabytes even with thousands of titles).
- **Persistent Cache**: Once cached, metadata remains in SQLite indefinitely without automatic expiration.
- **Soft Deletions**: Deleted general notebook entries (`general_entries`) are soft-deleted (`is_deleted = 1`) to prevent accidental data loss.

---

## 3. Data Classification: The Two Tiers

When automated or user-triggered cleanup routines run, data is divided into two distinct classifications:

### Tier A: The Sacred Data (Permanent & Untouchable)
The cleanup engine will **never** delete, prune, or evict any title or entry that contains personal user investment:
- Any movie assigned a status: *Watched*, *Watch Later*, *Favorites*, *Rewatch*, or *Nope / Excluded*.
- Any movie containing a personal note or user verdict.
- Any movie with a custom, user-defined keyword.
- Any movie actively tracked under *Looking Out For*.
- Active general notes and links.

### Tier B: The Disposable Cache (Eligible for Smart Eviction)
Titles that were retrieved into local SQLite solely because they were viewed in detail, but have received **zero user actions**:
- No status, no verdict, no notes, no custom keywords, and not in *Looking Out For*.
- Unopened and untouched for an extended retention threshold (e.g., 90 days).
- When evicted, SQLite foreign key cascade rules clean up associated genres, credits, and keywords attached solely to the disposable title.

---

## 4. Architectural Measures & Maintenance Roadmap

### Measure 1: Automated Safety Net Backups
- Before any cleanup or maintenance routine executes, the engine creates an automated timestamped backup of the working database (e.g., `backups/movie_excluder_YYYYMMDD_HHMMSS.db`).
- The application automatically retains the latest 3 to 5 backup snapshots, rotating out older backups.
- Provides 100% fail-safe peace of mind with zero risk of irreversible data loss.

### Measure 2: SQLite Physical Compaction (`VACUUM`)
- In SQLite, deleting records frees space internally for future rows but does not reduce the file size on the user's hard drive.
- Running a post-cleanup `VACUUM` defragments the database file and physically shrinks it on disk to its minimum footprint.

### Measure 3: "Dry-Run" Preview Modal
- Maintenance actions should never run invisibly or destructively without user awareness.
- When triggering a cleanup from Settings / Storage, the UI presents an informative preview:
  - Count of disposable movie records identified (> 90 days untouched).
  - Estimated disk space to be reclaimed.
  - Count of soft-deleted notes waiting in trash.
  - Explicit confirmation button (`[Clean Stale Cache]`).

### Measure 4: Background Refresh for Active Shelves
- Titles in active user shelves (*Watch Later*, *Looking Out For*) represent films the user actively cares about.
- If their cached metadata is older than 180 days, the application quietly queries TMDB upon viewing to update release dates, vote counts, and streaming availability.
- Network or TMDB API failures never block viewing of locally saved data.

### Measure 5: 1-Click Human-Readable Export (Data Portability)
- A dedicated *Export Data* utility that produces a clean JSON and/or Markdown bundle of:
  - Personal shelves and watch histories.
  - Movie verdicts and private notes.
  - General notebook entries and tags.
- Ensures the user's personal movie history is permanently portable and machine-independent.

### Measure 6: Permanent Trash Purging & Orphan Tag Cleanup
- Soft-deleted general notes remain recoverable until the user selects an explicit *Empty Trash* action.
- Tags associated exclusively with deleted notes are automatically purged from tag recommendations and auto-suggestions, ensuring tag autocomplete remains clean and relevant.
