const IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500";
const JOURNAL_TIME_ZONE = "Asia/Kolkata";
const JOURNAL_START_YEAR = 2026;
const JOURNAL_START_MONTH = 8;
const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

const GENRE_OPTIONS = [
  [28, "Action"], [12, "Adventure"], [16, "Animation"],
  [35, "Comedy"], [80, "Crime"], [99, "Documentary"],
  [18, "Drama"], [10751, "Family"], [14, "Fantasy"],
  [36, "History"], [27, "Horror"], [10402, "Music"],
  [9648, "Mystery"], [10749, "Romance"], [878, "Science Fiction"],
  [10770, "TV Movie"], [53, "Thriller"], [10752, "War"],
  [37, "Western"],
];

const LANGUAGE_OPTIONS = [
  ["en", "English"],
  ["fr", "French"], ["es", "Spanish"], ["de", "German"],
  ["it", "Italian"], ["pt", "Portuguese"], ["sv", "Swedish"],
  ["no", "Norwegian"], ["da", "Danish"], ["fi", "Finnish"],
  ["is", "Icelandic"], ["nl", "Dutch"], ["pl", "Polish"],
  ["cs", "Czech"], ["hu", "Hungarian"], ["ro", "Romanian"],
  ["el", "Greek"], ["tr", "Turkish"], ["ru", "Russian"],
  ["uk", "Ukrainian"], ["he", "Hebrew"], ["fa", "Persian"],
  ["ja", "Japanese"], ["ko", "Korean"], ["zh", "Chinese"],
  ["cn", "Cantonese"], ["th", "Thai"], ["vi", "Vietnamese"],
  ["id", "Indonesian"], ["ms", "Malay"], ["tl", "Tagalog"],
  ["hi", "Hindi"], ["te", "Telugu"], ["ta", "Tamil"],
  ["ml", "Malayalam"], ["kn", "Kannada"], ["bn", "Bengali"],
  ["mr", "Marathi"], ["pa", "Punjabi"], ["ur", "Urdu"],
  ["ar", "Arabic"],
];

const COUNTRY_OPTIONS = [
  ["US", "United States"], ["GB", "United Kingdom"], ["CA", "Canada"],
  ["AU", "Australia"], ["NZ", "New Zealand"], ["IE", "Ireland"],
  ["FR", "France"], ["DE", "Germany"], ["IT", "Italy"],
  ["ES", "Spain"], ["SE", "Sweden"], ["NO", "Norway"],
  ["DK", "Denmark"], ["FI", "Finland"], ["IS", "Iceland"],
  ["NL", "Netherlands"], ["BE", "Belgium"], ["CH", "Switzerland"],
  ["AT", "Austria"], ["PL", "Poland"], ["RU", "Russia"],
  ["TR", "Turkey"], ["IL", "Israel"], ["IR", "Iran"],
  ["BR", "Brazil"], ["MX", "Mexico"], ["AR", "Argentina"],
  ["ZA", "South Africa"], ["JP", "Japan"], ["KR", "South Korea"],
  ["CN", "China"], ["HK", "Hong Kong"], ["TW", "Taiwan"],
  ["TH", "Thailand"], ["IN", "India"],
];

// Compact chip clouds: only these are always visible. Anything else is added on demand via the "+" chip.
const PRIMARY_LANGUAGE_CODES = ["en", "fr", "es", "de", "ja", "ko"];
const PRIMARY_COUNTRY_CODES = ["US", "GB", "FR", "DE", "JP", "KR"];

const PICKER_CONFIG = {
  "include-genres": { options: GENRE_OPTIONS, opposite: "exclude-genres" },
  "exclude-genres": { options: GENRE_OPTIONS, opposite: "include-genres" },
  "include-languages": { options: LANGUAGE_OPTIONS, opposite: "exclude-languages" },
  "exclude-languages": { options: LANGUAGE_OPTIONS, opposite: "include-languages" },
  "include-countries": { options: COUNTRY_OPTIONS },
};

const DEFAULT_SYSTEM_FILTERS = {
  include_original_languages: ["en"],
  exclude_origin_countries: ["PK", "IN"],
  exclude_genre_ids: [16, 37, 99],
  exclude_original_languages: ["hi", "te", "ta", "ml", "kn", "bn", "mr", "pa", "ur", "ar"],
  minimum_rating: 6.0,
  maximum_rating: 10.0,
  minimum_vote_count: 100,
};

const STATUS_LABELS = {
  new_discovery: "New discovery",
  watch_later: "Watch later",
  watched: "Watched",
  rewatch: "Rewatch",
  excluded: "Nope",
};

const VIEW_COPY = {
  discover: {
    kicker: "Movie discovery",
    title: "Discover movies",
    description: "Explore TMDB with clean personal status filtering.",
  },
  new_discovery: {
    kicker: "Personal library",
    title: "New discoveries",
    description: "Movies waiting for your decision.",
  },
  watch_later: {
    kicker: "Your shortlist",
    title: "Watch later",
    description: "The movies you have deliberately saved for another day.",
  },
  watched: {
    kicker: "Personal history",
    title: "Watched",
    description: "Movies you have already finished.",
  },
  rewatch: {
    kicker: "Worth another visit",
    title: "Rewatch",
    description: "Movies you have chosen to experience again.",
  },
  excluded: {
    kicker: "Filtered out",
    title: "Nope",
    description: "Movies you do not want the app to recommend again.",
  },
  favorites: {
    kicker: "The very best",
    title: "Favourites",
    description: "Your hand-picked favourites from watched movies.",
  },
  "movie-notes": {
    kicker: "Personal memory",
    title: "Movie Notes",
    description: "Search and browse your private thoughts and observations.",
  },
};

const elements = {
  shell: document.querySelector("#app-shell"),
  form: document.querySelector("#movie-search"),
  query: document.querySelector("#search-query"),
  grid: document.querySelector("#movie-grid"),
  empty: document.querySelector("#empty-state"),
  emptyTitle: document.querySelector("#empty-title"),
  emptyCopy: document.querySelector("#empty-copy"),
  emptySearchButton: document.querySelector("#empty-search-button"),
  notice: document.querySelector("#notice"),
  kicker: document.querySelector("#library-kicker"),
  title: document.querySelector("#library-title"),
  shelfCount: document.querySelector("#shelf-count"),
  description: document.querySelector("#library-description"),
  count: document.querySelector("#result-count"),
  navLinks: [...document.querySelectorAll("[data-view]")],
  masterTabs: [...document.querySelectorAll(".master-tab")],
  sidebarPaneDiscover: document.querySelector("#sidebar-pane-discover"),
  sidebarPaneLibrary: document.querySelector("#sidebar-pane-library"),
  sidebarPaneNotes: document.querySelector("#sidebar-pane-notes"),
  ribbonChips: [...document.querySelectorAll(".ribbon-chip")],
  sidebar: document.querySelector("#app-sidebar"),
  appLayout: document.querySelector(".app-layout"),
  mobileView: document.querySelector("#mobile-view"),
  discoverWorkspace: document.querySelector("#discovery-workspace"),
  refreshFeed: document.querySelector("#refresh-feed"),
  nopeModeToggle: document.querySelector("#nope-mode-toggle"),
  nopeUndoCounter: document.querySelector("#nope-undo-counter"),
  notesSearchContainer: document.querySelector("#notes-search-container"),
  notesSearchInput: document.querySelector("#notes-search-input"),
  clearNotesSearch: document.querySelector("#clear-notes-search"),
  modeButtons: [...document.querySelectorAll("[data-discovery-mode]")],
  simpleControls: document.querySelector("#simple-controls"),
  advancedControls: document.querySelector("#advanced-controls"),
  refreshDiscovery: document.querySelector("#refresh-discovery"),
  advancedForm: document.querySelector("#advanced-search-form"),
  personalFilters: document.querySelector("#personal-filters"),
  profileSelect: document.querySelector("#profile-select"),
  saveProfile: document.querySelector("#save-profile"),
  updateProfile: document.querySelector("#update-profile"),
  deleteProfile: document.querySelector("#delete-profile"),
  profileDialog: document.querySelector("#profile-dialog"),
  profileNameForm: document.querySelector("#profile-name-form"),
  profileName: document.querySelector("#profile-name"),
  profileDialogTitle: document.querySelector("#profile-dialog-title"),
  profileDialogCopy: document.querySelector("#profile-dialog-copy"),
  profileSubmit: document.querySelector("#profile-submit"),
  cancelProfile: document.querySelector("#cancel-profile"),
  resetFilters: document.querySelector("#reset-filters"),
  pagination: document.querySelector("#pagination"),
  returnToOrigin: document.querySelector("#return-to-origin"),
  quickUpdateProfile: document.querySelector("#quick-update-profile"),
  filmographyToolbar: document.querySelector("#filmography-toolbar"),
  filmographyAvatar: document.querySelector("#filmography-avatar"),
  filmographyName: document.querySelector("#filmography-name"),
  filmographyKicker: document.querySelector("#filmography-kicker"),
  filmographyTabs: document.querySelector("#filmography-tabs"),
  filmTabAll: document.querySelector("#film-tab-all"),
  filmTabDirecting: document.querySelector("#film-tab-directing"),
  filmTabActing: document.querySelector("#film-tab-acting"),
  workspaceCollapse: document.querySelector("#workspace-collapse"),
  workspaceControls: document.querySelector("#workspace-controls"),
  workspaceSummary: document.querySelector("#workspace-summary"),
  workspaceCollapseLabel: document.querySelector("#workspace-collapse-label"),
  genreLogic: document.querySelector("#genre-logic"),
  minimumRating: document.querySelector("#minimum-rating"),
  maximumRating: document.querySelector("#maximum-rating"),
  releaseYearFrom: document.querySelector("#release-year-from"),
  releaseYearTo: document.querySelector("#release-year-to"),
  minimumVotes: document.querySelector("#minimum-votes"),
  sortBy: document.querySelector("#sort-by"),
  includeUntracked: document.querySelector("#include-untracked"),
  notesQuery: document.querySelector("#notes-query"),
  favoriteOnly: document.querySelector("#favorite-only"),
  detailPage: document.querySelector("#movie-detail-page"),
  dialogClose: document.querySelector("#dialog-close"),
  detailBackLabel: document.querySelector("#detail-back-label"),
  detailTrail: document.querySelector("#detail-trail"),
  detailNavStepper: document.querySelector("#detail-nav-stepper"),
  detailPrevBtn: document.querySelector("#detail-prev-btn"),
  detailNextBtn: document.querySelector("#detail-next-btn"),
  dialogLoading: document.querySelector("#dialog-loading"),
  dialogContent: document.querySelector("#dialog-content"),
  dialogPoster: document.querySelector("#dialog-poster-wrap"),
  dialogKicker: document.querySelector("#dialog-kicker"),
  dialogTitle: document.querySelector("#dialog-title"),
  dialogMeta: document.querySelector("#dialog-meta"),
  dialogOverview: document.querySelector("#dialog-overview"),
  dialogGenres: document.querySelector("#dialog-genres"),
  dialogKeywords: document.querySelector("#dialog-keywords"),
  dialogDirectors: document.querySelector("#dialog-directors"),
  dialogActors: document.querySelector("#dialog-actors"),
  customKeywordForm: document.querySelector("#custom-keyword-form"),
  customKeyword: document.querySelector("#custom-keyword"),
  showCustomKeyword: document.querySelector("#show-custom-keyword"),
  keywordFeedback: document.querySelector("#keyword-feedback"),
  statusSelect: document.querySelector("#status-select"),
  saveStatus: document.querySelector("#save-status"),
  statusFeedback: document.querySelector("#status-feedback"),
  favoriteButton: document.querySelector("#favorite-button"),
  verdictStars: document.querySelector("#verdict-stars"),
  clearVerdict: document.querySelector("#clear-verdict"),
  verdictFeedback: document.querySelector("#verdict-feedback"),
  notes: document.querySelector("#movie-notes"),
  saveNotes: document.querySelector("#save-notes"),
  notesFeedback: document.querySelector("#notes-feedback"),
  notesPanel: document.querySelector("#notes-panel"),
  relatedPanel: document.querySelector("#related-panel"),
  relatedMovies: document.querySelector("#related-movies"),
  relatedFamiliarToggle: document.querySelector("#related-familiar-toggle"),
  lookingOutControl: document.querySelector("#looking-out-control"),
  lookingOutToggle: document.querySelector("#looking-out-toggle"),
  lookingOutReleaseDate: document.querySelector("#looking-out-release-date"),
  entriesPage: document.querySelector("#entries-page"),
  entryList: document.querySelector("#entry-list"),
  entryPagination: document.querySelector("#entry-pagination"),
  entryFilters: document.querySelector("#entry-filters"),
  entryQuery: document.querySelector("#entry-query"),
  entryTypeFilter: document.querySelector("#entry-type-filter"),
  entryYearFilter: document.querySelector("#entry-year-filter"),
  entryMonthFilter: document.querySelector("#entry-month-filter"),
  clearEntryFilters: document.querySelector("#clear-entry-filters"),
  newEntry: document.querySelector("#new-entry"),
  entryReader: document.querySelector("#entry-reader"),
  entryReaderBack: document.querySelector("#entry-reader-back"),
  entryReaderPublish: document.querySelector("#entry-reader-publish"),
  entryReaderEdit: document.querySelector("#entry-reader-edit"),
  entryReaderPrevious: document.querySelector("#entry-reader-previous"),
  entryReaderNext: document.querySelector("#entry-reader-next"),
  entryReaderDelete: document.querySelector("#entry-reader-delete"),
  entryReaderType: document.querySelector("#entry-reader-type"),
  entryReaderTitle: document.querySelector("#entry-reader-title"),
  entryReaderDate: document.querySelector("#entry-reader-date"),
  entryReaderTags: document.querySelector("#entry-reader-tags"),
  entryReaderBody: document.querySelector("#entry-reader-body"),
  entryReaderLinks: document.querySelector("#entry-reader-links"),
  entryReaderCreated: document.querySelector("#entry-reader-created"),
  entryBannerWrapper: document.querySelector("#entry-banner-wrapper"),
  entryBannerView: document.querySelector("#entry-banner-view"),
  entryBannerImg: document.querySelector("#entry-banner-img"),
  entryBannerEdit: document.querySelector("#entry-banner-edit"),
  entryBannerPreviewBox: document.querySelector("#entry-banner-preview-box"),
  entryBannerPreviewImg: document.querySelector("#entry-banner-preview-img"),
  entryBannerPickerBar: document.querySelector("#entry-banner-picker-bar"),
  readerAddBannerBtn: document.querySelector("#reader-add-banner-btn"),
  readerCloseBannerPickerBtn: document.querySelector("#reader-close-banner-picker-btn"),
  readerChangeBannerBtn: document.querySelector("#reader-change-banner-btn"),
  readerRemoveBannerBtn: document.querySelector("#reader-remove-banner-btn"),
  readerUploadBannerBtn: document.querySelector("#reader-upload-banner-btn"),
  readerUrlBannerBtn: document.querySelector("#reader-url-banner-btn"),
  readerBannerFileInput: document.querySelector("#reader-banner-file-input"),
  readerTitleInput: document.querySelector("#reader-title-input"),
  readerEditDate: document.querySelector("#reader-edit-date"),
  readerTagsChips: document.querySelector("#reader-tags-chips"),
  readerTagInput: document.querySelector("#reader-tag-input"),
  readerBodyInput: document.querySelector("#reader-body-input"),
  readerCancel: document.querySelector("#reader-cancel"),
  readerSaveDraft: document.querySelector("#reader-save-draft"),
  readerSavePublish: document.querySelector("#reader-save-publish"),
  readerWordCount: document.querySelector("#reader-word-count"),
  readerReadTime: document.querySelector("#reader-read-time"),
  lookingOutPage: document.querySelector("#looking-out-page"),
  lookingOutGrid: document.querySelector("#looking-out-grid"),
  lookingOutPagination: document.querySelector("#looking-out-pagination"),
  releaseAlertsToggle: document.querySelector("#release-alerts-toggle"),
  releaseAlertSummary: document.querySelector("#release-alert-summary"),
  releaseAlertBadge: document.querySelector("#release-alert-badge"),
  storagePage: document.querySelector("#storage-page"),
  storageSummary: document.querySelector("#storage-summary"),
  cleanupCache: document.querySelector("#cleanup-cache"),
  purgeDeletedEntries: document.querySelector("#purge-deleted-entries"),
  storageFeedback: document.querySelector("#storage-feedback"),
  footerViews: [...document.querySelectorAll("[data-footer-view]")],
  libraryFiltersWorkspace: document.querySelector("#library-filters-workspace"),
  libraryFilterQuery: document.querySelector("#library-filter-query"),
  resetLibraryFilters: document.querySelector("#reset-library-filters"),
  librarySearchScope: document.querySelector("#library-search-scope"),
  scopeBtnAll: document.querySelector("#scope-btn-all"),
  scopeBtnShelf: document.querySelector("#scope-btn-shelf"),
  libGenresCloud: document.querySelector("#lib-genres-cloud"),
  libYearFrom: document.querySelector("#lib-year-from"),
  libYearTo: document.querySelector("#lib-year-to"),
  libLanguagesCloud: document.querySelector("#lib-languages-cloud"),
  libSortCloud: document.querySelector("#lib-sort-cloud"),
  badgeLibGenres: document.querySelector("#badge-lib-genres"),
  badgeLibYear: document.querySelector("#badge-lib-year"),
  badgeLibKeywords: document.querySelector("#badge-lib-keywords"),
  badgeLibPeople: document.querySelector("#badge-lib-people"),
  badgeLibLanguages: document.querySelector("#badge-lib-languages"),
  notesTagList: document.querySelector("#notes-tag-list"),
  notesTotalCount: document.querySelector("#notes-total-count"),
  notesViewAll: document.querySelector("#notes-view-all"),
  notesViewDrafts: document.querySelector("#notes-view-drafts"),
  notesDraftsCount: document.querySelector("#notes-drafts-count"),
  notesViewArchive: document.querySelector("#notes-view-archive"),
  notesArchiveCount: document.querySelector("#notes-archive-count"),
  notesTimelineSection: document.querySelector("#notes-timeline-section"),
  notesTimelineList: document.querySelector("#notes-timeline-list"),
  notesTagsSection: document.querySelector("#notes-tags-section"),
  notesTagsToggle: document.querySelector("#notes-tags-toggle"),
  notesTimelineToggle: document.querySelector("#notes-timeline-toggle"),
  greyContainer: document.querySelector("#grey-container"),
  greyToggle: document.querySelector("#grey-toggle"),
  greyDrawer: document.querySelector("#grey-drawer"),
  greyCloseBtn: document.querySelector("#grey-close-btn"),
  greyClearBtn: document.querySelector("#grey-clear-btn"),
  greyContextView: document.querySelector("#grey-context-view"),
  greyContextDetail: document.querySelector("#grey-context-detail"),
  greyStatusText: document.querySelector("#grey-status-text"),
  greyMessages: document.querySelector("#grey-messages"),
  greyForm: document.querySelector("#grey-form"),
  greyInput: document.querySelector("#grey-input"),
  greySendBtn: document.querySelector("#grey-send-btn"),
  greyModelTag: document.querySelector("#grey-model-tag"),
  greyModelName: document.querySelector("#grey-model-name"),
  greySkillsBar: document.querySelector("#grey-skills-bar"),
  greySlashMenu: document.querySelector("#grey-slash-menu"),
};

const state = {
  greyModelMode: "auto",
  movies: [],
  unfilteredShelfMovies: [],
  libSelectedGenres: new Set(),
  libSelectedLanguages: new Set(),
  librarySearchScope: "all",
  isSearchingLibrary: false,
  mode: "shelf",
  currentView: "new_discovery",
  selectedMovie: null,
  requestNumber: 0,
  previousScrollPosition: 0,
  discoveryMode: "simple",
  preferences: [],
  profilePassthroughFilters: {},
  defaultProfileLoaded: false,
  selectedEntities: {
    actors: [],
    directors: [],
    keywords: [],
    excludedKeywords: [],
    companies: [],
    excludedCompanies: [],
    libKeywords: [],
    libDirectors: [],
    libActors: [],
  },
  currentSearchSpec: null,
  searchPage: 1,
  searchTotalPages: 0,
  totalResults: 0,
  pageLoader: null,
  paginationExact: true,
  nopeMode: false,
  nopeUndoStack: [],
  filtersCollapsed: false,
  searchStateTimer: null,
  editingEntryId: null,
  entryPage: 1,
  entryResults: [],
  entryTotalPages: 1,
  entryReaderIndex: -1,
  entryReaderEntry: null,
  entryReturnScroll: 0,
  entryTagFilter: "",
  notesCurrentView: "all",
  notesTimelineFilter: null,
  lookingOutPage: 1,
  showRelatedFamiliar: false,
  detailRelatedMovies: [],
  profileDialogMode: "create",
  detailTrail: [],
  detailReturnLabel: "Back to movies",
  searchOriginMovie: null,
  savedSearchSnapshot: null,
  activeFilmographyPerson: null,
  readerEditing: false,
  readerTags: [],
  readerBannerUrl: null,
};

async function fetchJSON(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}.`;

    try {
      const body = await response.json();
      message = body.detail || message;
    } catch {
      // Keep the useful HTTP fallback above.
    }

    throw new Error(message);
  }

  return response.json();
}

function setSectionCopy({ kicker, title, description }) {
  elements.kicker.textContent = kicker;
  elements.title.textContent = title;
  elements.description.textContent = description;
  if (elements.shelfCount) {
    elements.shelfCount.textContent = "";
  }
}

function setActiveView(view) {
  state.currentView = view;
  if (view && elements.filmographyToolbar) {
    elements.filmographyToolbar.classList.add("is-hidden");
    state.activeFilmographyPerson = null;
  }
  elements.navLinks.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.view === view);
  });

  elements.masterTabs.forEach((tab) => {
    const tabType = tab.dataset.masterTab;
    let isActive = false;
    if (tabType === "discover" && view === "discover") isActive = true;
    else if (tabType === "library" && ["favorites", "watched", "watch_later", "rewatch", "excluded", "new_discovery", "movie-notes"].includes(view)) isActive = true;
    else if (tabType === "notes" && view === "entries") isActive = true;
    tab.classList.toggle("is-active", isActive);
  });

  // Switch sidebar pane based on master pillar
  const isDiscover = view === "discover";
  const isLibrary = ["favorites", "watched", "watch_later", "rewatch", "excluded", "new_discovery", "movie-notes"].includes(view);
  const isNotes = view === "entries";

  if (view !== null && view !== "filmography") {
    if (elements.sidebarPaneDiscover) {
      elements.sidebarPaneDiscover.classList.toggle("is-hidden", !isDiscover);
    }
    if (elements.sidebarPaneLibrary) {
      elements.sidebarPaneLibrary.classList.toggle("is-hidden", !isLibrary);
    }
    if (elements.sidebarPaneNotes) {
      elements.sidebarPaneNotes.classList.toggle("is-hidden", !isNotes);
    }
    if (elements.discoverWorkspace) {
      elements.discoverWorkspace.classList.toggle("is-hidden", !isDiscover);
    }
  }

  const appSidebar = document.querySelector("#app-sidebar");
  if (appSidebar) {
    appSidebar.classList.toggle("is-notes-mode", isNotes);
  }

  const discoverHeader = document.querySelector("#discover-canvas-header");
  if (discoverHeader) {
    discoverHeader.classList.toggle("is-hidden", !isDiscover || state.mode === "filmography");
  }
  const sectionHeadingBlock = document.querySelector("#section-heading-block");
  if (sectionHeadingBlock) {
    sectionHeadingBlock.classList.toggle("is-hidden", isDiscover || state.mode === "filmography");
  }

  if (view in VIEW_COPY) {
    elements.mobileView.value = view;
  }

  // Nope Mode is ONLY available in Discover view
  if (!isDiscover) {
    if (state.nopeMode) {
      toggleNopeMode(false);
    }
    elements.nopeModeToggle?.classList.add("is-hidden");
  } else {
    elements.nopeModeToggle?.classList.remove("is-hidden");
  }

  if (view && history.replaceState) {
    history.replaceState(null, "", `#${view}`);
  }

  if (view && ["favorites", "watched", "watch_later", "rewatch", "excluded", "new_discovery", "movie-notes", "entries", "discover"].includes(view)) {
    try {
      localStorage.setItem("nope_current_view", view);
      if (["favorites", "watched", "watch_later", "rewatch", "excluded", "new_discovery", "movie-notes"].includes(view)) {
        localStorage.setItem("nope_last_library_shelf", view);
      }
    } catch {}
  }
}

function toggleNopeMode(forceState) {
  // Disallow Nope Mode outside of Discover view
  if (state.currentView !== "discover") {
    state.nopeMode = false;
    elements.nopeModeToggle?.classList.remove("is-active");
    elements.nopeModeToggle?.setAttribute("aria-pressed", "false");
    elements.grid?.classList.remove("is-nope-mode");
    state.nopeUndoStack = [];
    updateNopeUndoCounter();
    return;
  }

  state.nopeMode = typeof forceState === "boolean" ? forceState : !state.nopeMode;
  elements.nopeModeToggle?.classList.toggle("is-active", state.nopeMode);
  elements.nopeModeToggle?.setAttribute("aria-pressed", String(state.nopeMode));
  elements.grid?.classList.toggle("is-nope-mode", state.nopeMode);

  if (!state.nopeMode) {
    state.nopeUndoStack = [];
    updateNopeUndoCounter();
  }
}

function updateNopeUndoCounter() {
  if (!elements.nopeUndoCounter) return;
  const count = state.nopeUndoStack.length;
  if (count > 0 && state.nopeMode) {
    elements.nopeUndoCounter.textContent = `Undo (${count})`;
    elements.nopeUndoCounter.classList.remove("is-hidden");
  } else {
    elements.nopeUndoCounter.classList.add("is-hidden");
  }
}

function clearNopeUndo() {
  state.nopeUndoStack = [];
  updateNopeUndoCounter();
}

async function handleLiberateMovie(movie, article) {
  const movieId = getMovieId(movie);
  const title = movie.title || movie.original_title || "Untitled movie";
  const badge = article.querySelector(".status-badge");

  // Determine what prior status the movie had
  const undoIndex = state.nopeUndoStack.findLastIndex ? state.nopeUndoStack.findLastIndex(item => item.movieId === movieId) : -1;
  let priorStatus = "untracked";
  if (undoIndex !== -1) {
    priorStatus = state.nopeUndoStack[undoIndex].previousStatus;
    state.nopeUndoStack.splice(undoIndex, 1);
    updateNopeUndoCounter();
  } else if (movie._priorStatus) {
    priorStatus = movie._priorStatus;
  }

  // Optimistic DOM update
  article.classList.remove("is-noped");
  if (badge) {
    badge.dataset.status = priorStatus;
    badge.textContent = priorStatus === "untracked" ? "Untracked" : (STATUS_LABELS[priorStatus] || priorStatus);
  }

  try {
    if (priorStatus === "untracked") {
      await fetchJSON(`/movies/${movieId}/status`, { method: "DELETE" });
      movie.user_data = null;
      clearDiscoveryCache();
    } else {
      const response = await fetchJSON(`/movies/${movieId}/status`, {
        method: "PUT",
        body: JSON.stringify({ status: priorStatus }),
      });
      movie.user_data = response.user_movie_data;
      clearDiscoveryCache();
    }
  } catch (error) {
    // Rollback on failure
    article.classList.add("is-noped");
    if (badge) {
      badge.dataset.status = "excluded";
      badge.textContent = STATUS_LABELS.excluded;
    }
    if (!movie.user_data) movie.user_data = {};
    movie.user_data.status = "excluded";
    showNotice(`Could not liberate "${title}": ${error.message}`);
  }
}

async function handleQuickNope(movie, article) {
  if (state.currentView !== "discover" || !state.nopeMode) return;

  const movieId = getMovieId(movie);
  const currentStatus = getStatus(movie) || "untracked";
  const title = movie.title || movie.original_title || "Untitled movie";

  // If already noped, click liberates it from Nope jail!
  if (currentStatus === "excluded" || article.classList.contains("is-noped")) {
    await handleLiberateMovie(movie, article);
    return;
  }

  // Remember prior status before noping
  const priorStatus = currentStatus;
  movie._priorStatus = priorStatus;

  // Push to undo stack (max 3)
  state.nopeUndoStack.push({
    movieId,
    previousStatus: priorStatus,
    title,
    userData: movie.user_data ? { ...movie.user_data } : null,
  });
  if (state.nopeUndoStack.length > 3) {
    state.nopeUndoStack.shift();
  }
  updateNopeUndoCounter();

  // Optimistic UI update
  article.classList.add("is-noped");
  let badge = article.querySelector(".status-badge");
  if (!badge) {
    badge = document.createElement("span");
    badge.className = "status-badge";
    const posterBtn = article.querySelector(".poster-button");
    if (posterBtn) posterBtn.append(badge);
  }
  if (badge) {
    badge.dataset.status = "excluded";
    badge.textContent = STATUS_LABELS.excluded;
  }
  if (!movie.user_data) {
    movie.user_data = {};
  }
  movie.user_data.status = "excluded";

  try {
    const response = await fetchJSON(`/movies/${movieId}/status`, {
      method: "PUT",
      body: JSON.stringify({ status: "excluded" }),
    });
    movie.user_data = response.user_movie_data;
    clearDiscoveryCache();
  } catch (error) {
    // Rollback on failure
    article.classList.remove("is-noped");
    if (badge) {
      badge.dataset.status = priorStatus;
      badge.textContent = priorStatus === "untracked" ? "Untracked" : STATUS_LABELS[priorStatus];
    }
    movie.user_data.status = priorStatus;
    state.nopeUndoStack = state.nopeUndoStack.filter((item) => item.movieId !== movieId);
    updateNopeUndoCounter();
    showNotice(`Could not nope "${title}": ${error.message}`);
  }
}

async function handleNopeUndo() {
  if (!state.nopeMode || state.nopeUndoStack.length === 0) return;

  const lastItem = state.nopeUndoStack.pop();
  updateNopeUndoCounter();

  const { movieId, previousStatus, title, userData } = lastItem;
  const article = elements.grid?.querySelector(`.movie-card[data-movie-id="${movieId}"]`);
  const restoreStatus = (previousStatus && previousStatus !== "untracked") ? previousStatus : "untracked";

  if (article) {
    article.classList.remove("is-noped");
    const badge = article.querySelector(".status-badge");
    if (badge) {
      badge.dataset.status = previousStatus;
      badge.textContent = previousStatus === "untracked" ? "Untracked" : (STATUS_LABELS[previousStatus] || previousStatus);
    }
  }

  const movie = state.movies.find((m) => getMovieId(m) === movieId);

  try {
    if (restoreStatus === "untracked") {
      await fetchJSON(`/movies/${movieId}/status`, { method: "DELETE" });
      if (movie) {
        movie.user_data = null;
      }
    } else {
      const response = await fetchJSON(`/movies/${movieId}/status`, {
        method: "PUT",
        body: JSON.stringify({ status: restoreStatus }),
      });
      if (movie) {
        movie.user_data = response.user_movie_data;
      }
    }
    clearDiscoveryCache();
  } catch (error) {
    showNotice(`Could not undo "${title}": ${error.message}`);
  }
}

function updateMovieCardDOM(movieId, userData) {
  if (!movieId) return;
  const card = elements.grid?.querySelector(`.movie-card[data-movie-id="${movieId}"]`);
  if (!card) return;

  const status = userData?.status;
  const badge = card.querySelector(".status-badge");
  if (badge) {
    badge.dataset.status = status || "untracked";
    badge.textContent = status ? (STATUS_LABELS[status] || status) : "Untracked";
  }

  const posterBtn = card.querySelector(".poster-button");
  if (posterBtn) {
    let favMark = posterBtn.querySelector(".favorite-mark");
    if (userData?.is_favorite) {
      if (!favMark) {
        favMark = document.createElement("span");
        favMark.className = "favorite-mark";
        favMark.textContent = "♥";
        favMark.setAttribute("aria-label", "Favourite");
        posterBtn.append(favMark);
      }
    } else if (favMark) {
      favMark.remove();
    }
  }

  if (state.currentView === "discover") {
    card.classList.toggle("is-noped", status === "excluded");
  } else {
    card.classList.remove("is-noped");
  }
}

function showNotice(message) {
  elements.notice.textContent = message;
  elements.notice.classList.remove("is-hidden");
}

function clearNotice() {
  elements.notice.textContent = "";
  elements.notice.classList.add("is-hidden");
}

function updatePickerSummary() {
  // Chips show their active state directly
}

function buildMultiPicker(container, config) {
  if (!container) return;
  const chipCloud = document.createElement("div");
  chipCloud.className = "chip-cloud";

  config.options.forEach(([value, label]) => {
    const chip = document.createElement("label");
    chip.className = "filter-chip";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = String(value);
    checkbox.dataset.label = label;
    const text = document.createElement("span");
    text.className = "chip-label";
    text.textContent = label;

    chip.append(checkbox, text);
    chipCloud.append(chip);

    checkbox.addEventListener("change", () => {
      chip.classList.toggle("is-active", checkbox.checked);

      if (checkbox.checked && config.opposite) {
        const opposite = document.querySelector(`#${config.opposite}`);
        const oppositeCheckbox = opposite ? [...opposite.querySelectorAll("input")].find(
          (item) => item.value === checkbox.value,
        ) : null;

        if (oppositeCheckbox) {
          oppositeCheckbox.checked = false;
          oppositeCheckbox.closest(".filter-chip")?.classList.remove("is-active");
        }
      }

      updateFilterPillBadges();
      scheduleSearchStateSave();
    });
  });

  container.replaceChildren(chipCloud);
}

const TRI_PICKER_CONFIG = {
  "genres-picker": {
    options: GENRE_OPTIONS,
    includeId: "include-genres",
    excludeId: "exclude-genres",
    numeric: true,
  },
  "languages-picker": {
    options: LANGUAGE_OPTIONS,
    includeId: "include-languages",
    excludeId: "exclude-languages",
    numeric: false,
  },
};

function buildTriStatePicker(containerId, config) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const chipCloud = document.createElement("div");
  chipCloud.className = "tri-chip-cloud";

  config.options.forEach(([value, label]) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "tri-chip";
    chip.dataset.value = String(value);
    chip.dataset.state = "off";

    const icon = document.createElement("span");
    icon.className = "tri-chip-icon";

    const text = document.createElement("span");
    text.className = "tri-chip-label";
    text.textContent = label;

    chip.append(icon, text);
    chipCloud.append(chip);

    chip.addEventListener("click", (e) => {
      e.preventDefault();
      const current = chip.dataset.state;
      let next = "off";
      if (containerId === "genres-picker") {
        const mode = state.genreMode || "exclude";
        if (mode === "exclude") {
          next = current === "exclude" ? "off" : "exclude";
        } else {
          next = current === "include" ? "off" : "include";
        }
      } else {
        next = current === "off" ? "exclude" : current === "exclude" ? "include" : "off";
      }
      setTriChipState(chip, next, config);
      updateFilterPillBadges();
      renderActiveFilterTags();
      scheduleSearchStateSave();
    });
  });

  container.replaceChildren(chipCloud);
}

function setTriChipState(chip, state, config) {
  chip.dataset.state = state;
  chip.classList.toggle("is-included", state === "include");
  chip.classList.toggle("is-excluded", state === "exclude");

  const icon = chip.querySelector(".tri-chip-icon");
  if (icon) {
    icon.textContent = state === "include" ? "+" : state === "exclude" ? "−" : "";
  }

  const val = chip.dataset.value;
  const incCheckbox = document.querySelector(`#${config.includeId} input[value="${val}"]`);
  const excCheckbox = document.querySelector(`#${config.excludeId} input[value="${val}"]`);

  if (incCheckbox) incCheckbox.checked = (state === "include");
  if (excCheckbox) excCheckbox.checked = (state === "exclude");
}

function syncTriPickers() {
  Object.entries(TRI_PICKER_CONFIG).forEach(([containerId, config]) => {
    const incValues = new Set(getPickerValues(config.includeId).map(String));
    const excValues = new Set(getPickerValues(config.excludeId).map(String));
    const container = document.getElementById(containerId);
    if (!container) return;

    container.querySelectorAll(".tri-chip").forEach((chip) => {
      const val = chip.dataset.value;
      let state = "off";
      if (incValues.has(val)) {
        state = "include";
      } else if (excValues.has(val)) {
        state = "exclude";
      }
      chip.dataset.state = state;
      chip.classList.toggle("is-included", state === "include");
      chip.classList.toggle("is-excluded", state === "exclude");

      const icon = chip.querySelector(".tri-chip-icon");
      if (icon) {
        icon.textContent = state === "include" ? "+" : state === "exclude" ? "−" : "";
      }
    });
  });
  refreshCompactClouds();
}

function initializePickers() {
  Object.entries(PICKER_CONFIG).forEach(([id, config]) => {
    const container = document.querySelector(`#${id}`);
    buildMultiPicker(container, config);
  });
  Object.entries(TRI_PICKER_CONFIG).forEach(([id, config]) => {
    buildTriStatePicker(id, config);
  });
  refreshCompactClouds();
}

/* ---------- Compact language / country chip clouds ---------- */

// Languages excluded by default are applied silently by the search engine and never shown as chips.
const BACKGROUND_EXCLUDED_LANGUAGES = new Set(DEFAULT_SYSTEM_FILTERS.exclude_original_languages);

const COMPACT_CLOUD_CONFIG = [
  {
    hostSelector: "#languages-picker",
    cloudSelector: ".tri-chip-cloud",
    chipSelector: ".tri-chip",
    kind: "languages",
    noun: "language",
    options: LANGUAGE_OPTIONS,
    primary: PRIMARY_LANGUAGE_CODES,
    valueOf: (chip) => chip.dataset.value,
    isActive: (chip) => chip.dataset.state && chip.dataset.state !== "off",
    isBackground: (chip) => chip.dataset.state === "exclude" && BACKGROUND_EXCLUDED_LANGUAGES.has(chip.dataset.value),
    backgroundHint: (value) => (BACKGROUND_EXCLUDED_LANGUAGES.has(value) ? "excluded by default" : ""),
  },
  {
    hostSelector: "#include-countries",
    cloudSelector: ".chip-cloud",
    chipSelector: ".filter-chip",
    kind: "countries",
    noun: "country",
    options: COUNTRY_OPTIONS,
    primary: PRIMARY_COUNTRY_CODES,
    valueOf: (chip) => chip.querySelector("input")?.value,
    isActive: (chip) => Boolean(chip.querySelector("input")?.checked),
    isBackground: () => false,
    backgroundHint: (value) => (DEFAULT_SYSTEM_FILTERS.exclude_origin_countries.includes(value) ? "excluded by default" : ""),
  },
  {
    hostSelector: "#lib-languages-cloud",
    cloudSelector: null,
    chipSelector: ".filter-chip",
    kind: "languages",
    noun: "language",
    options: LANGUAGE_OPTIONS,
    primary: PRIMARY_LANGUAGE_CODES,
    valueOf: (chip) => chip.dataset.langCode,
    isActive: (chip) => chip.classList.contains("is-active"),
    isBackground: () => false,
    backgroundHint: () => "",
  },
];

function getPinnedChips(kind) {
  try {
    const parsed = JSON.parse(localStorage.getItem(`nope_pinned_${kind}`) || "[]");
    return Array.isArray(parsed) ? parsed.map(String) : [];
  } catch {
    return [];
  }
}

function setPinnedChips(kind, values) {
  try {
    localStorage.setItem(`nope_pinned_${kind}`, JSON.stringify([...new Set(values.map(String))]));
  } catch {}
}

function getCompactCloud(config) {
  const host = document.querySelector(config.hostSelector);
  if (!host) return null;
  return config.cloudSelector ? host.querySelector(config.cloudSelector) : host;
}

function refreshCompactClouds() {
  COMPACT_CLOUD_CONFIG.forEach(refreshCompactCloud);
}

function refreshCompactCloud(config) {
  const cloud = getCompactCloud(config);
  if (!cloud) return;

  const primary = new Set(config.primary);
  const pinned = new Set(getPinnedChips(config.kind));

  cloud.querySelectorAll(config.chipSelector).forEach((chip) => {
    const value = config.valueOf(chip);
    const isPrimary = primary.has(value);
    const isPinned = pinned.has(value) && !isPrimary;
    const visible = isPrimary || isPinned || (config.isActive(chip) && !config.isBackground(chip));
    chip.classList.toggle("is-hidden", !visible);
    chip.classList.toggle("is-pinned", isPinned);

    chip.querySelector(".chip-unpin")?.remove();
    if (isPinned) {
      const unpin = document.createElement("span");
      unpin.className = "chip-unpin";
      unpin.setAttribute("role", "button");
      const chipName = (chip.querySelector(".tri-chip-label, .chip-label")?.textContent || chip.textContent).trim();
      unpin.setAttribute("aria-label", `Remove ${chipName} from the list`);
      unpin.title = "Remove from list";
      unpin.textContent = "×";
      unpin.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        setPinnedChips(config.kind, getPinnedChips(config.kind).filter((item) => item !== value));
        refreshCompactClouds();
      });
      chip.append(unpin);
    }
  });

  let adder = cloud.querySelector(":scope > .chip-adder");
  if (!adder) {
    adder = document.createElement("button");
    adder.type = "button";
    adder.className = "chip-adder";
    adder.textContent = "+";
    adder.title = `Add a ${config.noun}`;
    adder.setAttribute("aria-label", `Add a ${config.noun}`);
    adder.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      toggleCompactAdderPanel(config, adder);
    });
  }
  cloud.append(adder); // always keep the + chip last
}

function closeCompactAdderPanels(except = null) {
  document.querySelectorAll(".chip-adder-panel").forEach((panel) => {
    if (panel !== except) {
      panel.remove();
    }
  });
  document.querySelectorAll(".chip-adder.is-open").forEach((button) => {
    if (!except || button !== except.__adderButton) {
      button.classList.remove("is-open");
    }
  });
}

function toggleCompactAdderPanel(config, adderButton) {
  const host = document.querySelector(config.hostSelector);
  if (!host) return;

  const existing = host.parentElement?.querySelector(`.chip-adder-panel[data-host="${config.hostSelector}"]`);
  if (existing) {
    closeCompactAdderPanels();
    return;
  }
  closeCompactAdderPanels();

  const panel = document.createElement("div");
  panel.className = "chip-adder-panel";
  panel.dataset.host = config.hostSelector;
  panel.__adderButton = adderButton;

  const input = document.createElement("input");
  input.type = "text";
  input.className = "chip-adder-input";
  input.placeholder = `Find a ${config.noun}…`;
  input.autocomplete = "off";
  input.setAttribute("aria-label", `Find a ${config.noun}`);

  const list = document.createElement("div");
  list.className = "chip-adder-list";
  list.setAttribute("role", "listbox");

  const renderOptions = () => {
    const query = input.value.trim().toLowerCase();
    const cloud = getCompactCloud(config);
    const visibleValues = new Set(
      [...(cloud?.querySelectorAll(config.chipSelector) || [])]
        .filter((chip) => !chip.classList.contains("is-hidden"))
        .map((chip) => config.valueOf(chip)),
    );
    const matches = config.options.filter(([value, label]) =>
      !visibleValues.has(String(value)) &&
      (!query || label.toLowerCase().includes(query) || String(value).toLowerCase() === query),
    );

    list.replaceChildren();
    if (!matches.length) {
      const empty = document.createElement("p");
      empty.className = "chip-adder-empty";
      empty.textContent = query ? `No ${config.noun} matches “${input.value.trim()}”.` : `All ${config.kind} are already shown.`;
      list.append(empty);
      return;
    }

    matches.forEach(([value, label]) => {
      const option = document.createElement("button");
      option.type = "button";
      option.className = "chip-adder-option";
      option.setAttribute("role", "option");
      option.textContent = label;
      const hint = config.backgroundHint(String(value));
      if (hint) {
        const hintEl = document.createElement("span");
        hintEl.className = "chip-adder-hint";
        hintEl.textContent = hint;
        option.append(hintEl);
      }
      option.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        setPinnedChips(config.kind, [...getPinnedChips(config.kind), String(value)]);
        refreshCompactClouds();
        closeCompactAdderPanels();
      });
      list.append(option);
    });
  };

  input.addEventListener("input", renderOptions);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      event.preventDefault();
      closeCompactAdderPanels();
      adderButton.focus();
    } else if (event.key === "Enter") {
      event.preventDefault();
      list.querySelector(".chip-adder-option")?.click();
    }
  });
  panel.addEventListener("click", (event) => event.stopPropagation());

  panel.append(input, list);
  host.after(panel);
  adderButton.classList.add("is-open");
  renderOptions();
  input.focus();
}

document.addEventListener("click", (event) => {
  if (!event.target.closest?.(".chip-adder-panel, .chip-adder")) {
    closeCompactAdderPanels();
  }
});

function getPickerValues(id, numeric = false) {
  return [...document.querySelectorAll(`#${id} input:checked`)].map((input) =>
    numeric ? Number(input.value) : input.value,
  );
}

function syncSortChips(val) {
  const currentVal = val || elements.sortBy?.value || "popularity.desc";
  document.querySelectorAll(".sort-chip").forEach((chip) => {
    chip.classList.toggle("is-active", chip.dataset.value === currentVal);
  });
}

function initializeSortChips() {
  document.querySelectorAll(".sort-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const val = chip.dataset.value;
      if (elements.sortBy) {
        elements.sortBy.value = val;
        elements.sortBy.dispatchEvent(new Event("change", { bubbles: true }));
      }
      syncSortChips(val);
      updateFilterPillBadges();
      scheduleSearchStateSave();
      runDiscoverySearch();
    });
  });
  syncSortChips();
}

function setPickerValues(id, values = []) {
  const selected = new Set(values.map((value) => String(value)));
  const container = document.querySelector(`#${id}`);
  if (!container) return;

  container.querySelectorAll("input").forEach((input) => {
    input.checked = selected.has(input.value);
    input.closest(".filter-chip")?.classList.toggle("is-active", input.checked);
  });
  syncTriPickers();
}

const ENTITY_CONFIG = {
  actors: {
    queryId: "actor-query",
    resultsId: "actor-results",
    selectedId: "selected-actors",
    searchPath: "/people/search",
    detailPath: "/people/",
  },
  directors: {
    queryId: "director-query",
    resultsId: "director-results",
    selectedId: "selected-directors",
    searchPath: "/people/search",
    detailPath: "/people/",
  },
  keywords: {
    queryId: "keyword-query",
    resultsId: "keyword-results",
    selectedId: "selected-keywords",
    searchPath: "/tmdb-keywords/search",
    detailPath: "/tmdb-keywords/",
  },
  excludedKeywords: {
    queryId: "exclude-keyword-query",
    resultsId: "exclude-keyword-results",
    selectedId: "selected-excluded-keywords",
    searchPath: "/tmdb-keywords/search",
    detailPath: "/tmdb-keywords/",
  },
  companies: {
    queryId: "company-query",
    resultsId: "company-results",
    selectedId: "selected-companies",
    searchPath: "/companies/search",
    detailPath: "/companies/",
  },
  excludedCompanies: {
    queryId: "exclude-company-query",
    resultsId: "exclude-company-results",
    selectedId: "selected-excluded-companies",
    searchPath: "/companies/search",
    detailPath: "/companies/",
  },
  libKeywords: {
    queryId: "lib-keyword-query",
    resultsId: "lib-keyword-results",
    selectedId: "selected-lib-keywords",
    searchPath: "/movies/library/keywords",
    detailPath: "/tmdb-keywords/",
  },
  libDirectors: {
    queryId: "lib-director-query",
    resultsId: "lib-director-results",
    selectedId: "selected-lib-directors",
    searchPath: "/movies/library/people?type=director",
    detailPath: "/people/",
  },
  libActors: {
    queryId: "lib-actor-query",
    resultsId: "lib-actor-results",
    selectedId: "selected-lib-actors",
    searchPath: "/movies/library/people?type=actor",
    detailPath: "/people/",
  },
};

function renderSelectedEntities(key) {
  const config = ENTITY_CONFIG[key];
  const container = document.querySelector(`#${config.selectedId}`);
  if (!container) return;
  container.replaceChildren();

  // Deduplicate items in state to guarantee zero repeats
  const seen = new Set();
  state.selectedEntities[key] = (state.selectedEntities[key] || []).filter((entity) => {
    const idKey = Number(entity.id);
    const nameKey = (entity.name || "").trim().toLowerCase();
    const compound = `${idKey}:${nameKey}`;
    if (seen.has(compound)) return false;
    seen.add(compound);
    return true;
  });

  state.selectedEntities[key].forEach((entity) => {
    const chip = document.createElement("span");
    const name = document.createElement("span");
    const remove = document.createElement("button");
    chip.className = "selected-entity";

    if (key === "keywords") {
      const isExcluded = entity.mode === "exclude";
      chip.classList.add("is-clickable");
      chip.classList.toggle("is-excluded", isExcluded);

      const toggle = document.createElement("span");
      toggle.className = "entity-mode-toggle";
      toggle.textContent = isExcluded ? "− " : "+ ";
      toggle.title = isExcluded
        ? "Excluded theme (tap to switch to Include)"
        : "Included theme (tap to switch to Exclude)";
      chip.append(toggle);

      chip.addEventListener("click", (event) => {
        if (event.target === remove) return;
        entity.mode = entity.mode === "exclude" ? "include" : "exclude";
        renderSelectedEntities(key);
        updateFilterPillBadges();
        renderActiveFilterTags();
        scheduleSearchStateSave();
      });
    }

    name.textContent = entity.name;
    if (key === "actors" || key === "directors") {
      name.classList.add("is-filmography-link");
      name.title = `View full career filmography for ${entity.name}`;
      name.addEventListener("click", (event) => {
        event.stopPropagation();
        loadPersonFilmography(entity, key.includes("Actor") ? "actors" : "directors");
      });
    }
    remove.type = "button";
    remove.textContent = "×";
    remove.setAttribute("aria-label", `Remove ${entity.name}`);
    remove.addEventListener("click", (event) => {
      event.stopPropagation();
      state.selectedEntities[key] = state.selectedEntities[key].filter(
        (item) => item.id !== entity.id,
      );
      renderSelectedEntities(key);
      updateFilterPillBadges();
      renderActiveFilterTags();
      scheduleSearchStateSave();
      if (key.startsWith("lib")) searchPersonalLibrary();
    });
    chip.append(name, remove);
    container.append(chip);
  });

  if (state.selectedEntities[key].length > 1) {
    const clear = document.createElement("button");
    clear.type = "button";
    clear.className = "entity-clear";
    clear.textContent = "Clear all";
    clear.addEventListener("click", () => {
      state.selectedEntities[key] = [];
      renderSelectedEntities(key);
      updateFilterPillBadges();
      renderActiveFilterTags();
      scheduleSearchStateSave();
      if (key.startsWith("lib")) searchPersonalLibrary();
    });
    container.append(clear);
  }
}

function addSelectedEntity(key, entity) {
  if (key === "keywords" && !entity.mode) {
    entity.mode = "include";
  }
  const entityId = Number(entity.id);
  const rawEntityName = (entity.raw_name || entity.name || "").replace(/^[🏷️\s]+/, "").trim().toLowerCase();
  const alreadySelected = state.selectedEntities[key].some((item) => {
    const itemId = Number(item.id);
    const rawItemName = (item.raw_name || item.name || "").replace(/^[🏷️\s]+/, "").trim().toLowerCase();
    if (itemId === entityId && itemId > 0) return true;
    if (key.toLowerCase().includes("keyword") && rawEntityName && rawItemName === rawEntityName) return true;
    return false;
  });
  if (!alreadySelected) {
    state.selectedEntities[key].push(entity);
    renderSelectedEntities(key);
    updateFilterPillBadges();
    renderActiveFilterTags();
    if (key.startsWith("lib")) searchPersonalLibrary();
  }

  const config = ENTITY_CONFIG[key];
  document.querySelector(`#${config.queryId}`).value = "";
  document.querySelector(`#${config.resultsId}`).classList.add("is-hidden");
  scheduleSearchStateSave();
}

function renderEntityResults(key, results) {
  const config = ENTITY_CONFIG[key];
  const container = document.querySelector(`#${config.resultsId}`);
  container.replaceChildren();

  // Deduplicate results by ID and case-insensitive name
  const seenIds = new Set();
  const seenNames = new Set();
  const dedupedResults = [];
  for (const item of results) {
    const id = Number(item.id);
    const name = (item.name || "").trim().toLowerCase();
    if (seenIds.has(id)) continue;
    if (name && seenNames.has(name)) continue;
    seenIds.add(id);
    if (name) seenNames.add(name);
    dedupedResults.push(item);
  }

  if (!dedupedResults.length) {
    const empty = document.createElement("p");
    empty.textContent = "No matches found";
    container.append(empty);
  } else {
    dedupedResults.slice(0, 6).forEach((result) => {
      const button = document.createElement("button");
      const name = document.createElement("strong");
      const context = document.createElement("span");
      button.type = "button";
      name.textContent = result.name || "Unnamed result";
      context.textContent = result.known_for_department
        || result.origin_country
        || (result.known_for_titles || []).slice(0, 2).join(" · ")
        || (result.is_custom ? "Personal tag" : (key.startsWith("lib") ? "Library keyword" : "TMDB result"));
      button.append(name, context);
      button.addEventListener("click", () => {
        addSelectedEntity(key, {
          id: Number(result.id),
          name: result.name || `TMDB #${result.id}`,
          raw_name: result.raw_name || result.name || "",
          is_custom: Boolean(result.is_custom),
        });
      });
      container.append(button);
    });
  }

  container.classList.remove("is-hidden");
}

function initializeEntityPickers() {
  Object.entries(ENTITY_CONFIG).forEach(([key, config]) => {
    const input = document.querySelector(`#${config.queryId}`);
    if (!input) return;
    let timer = null;

    if (key === "keywords") {
      input.addEventListener("paste", async (event) => {
        const text = (event.clipboardData || window.clipboardData)?.getData("text") || "";
        if (text.includes(",") || text.includes(";")) {
          event.preventDefault();
          const terms = text.split(/[,;\n]+/).map((t) => t.trim()).filter((t) => t.length >= 2);
          if (!terms.length) return;
          input.value = "";
          const origPlaceholder = input.placeholder;
          input.placeholder = `Resolving ${terms.length} themes…`;
          for (const term of terms) {
            try {
              const response = await fetchJSON(
                `${config.searchPath}?query=${encodeURIComponent(term)}`,
              );
              if (response.results && response.results.length > 0) {
                const match = response.results[0];
                if (!state.selectedEntities.keywords.some((k) => k.id === match.id)) {
                  state.selectedEntities.keywords.push({
                    id: Number(match.id),
                    name: match.name || term,
                    mode: "include",
                  });
                }
              }
            } catch {
              // ignore single fetch error
            }
          }
          input.placeholder = origPlaceholder;
          renderSelectedEntities("keywords");
          updateFilterPillBadges();
          renderActiveFilterTags();
          scheduleSearchStateSave();
          return;
        }
      });
    }

    input.addEventListener("input", () => {
      window.clearTimeout(timer);
      const query = input.value.trim();
      const results = document.querySelector(`#${config.resultsId}`);
      if (!results) return;

      if (query.length < 2) {
        results.classList.add("is-hidden");
        return;
      }

      timer = window.setTimeout(async () => {
        try {
          const sep = config.searchPath.includes("?") ? "&" : "?";
          let searchUrl = `${config.searchPath}${sep}query=${encodeURIComponent(query)}`;
          if (key.startsWith("lib") && state.librarySearchScope === "shelf" && state.currentView && state.currentView !== "discover" && state.currentView !== "entries") {
            searchUrl += `&status=${encodeURIComponent(state.currentView)}`;
          }
          const response = await fetchJSON(searchUrl);
          renderEntityResults(key, response.results || []);
        } catch (error) {
          results.replaceChildren();
          const message = document.createElement("p");
          message.textContent = error.message;
          results.append(message);
          results.classList.remove("is-hidden");
        }
      }, 300);
    });
  });
}

async function hydrateEntitySelections(filters) {
  const incIds = [...new Set((filters.include_keyword_ids || []).map(Number))];
  const excIds = [...new Set((filters.exclude_keyword_ids || []).map(Number))];

  const incKeywords = await Promise.all(incIds.map(async (id) => {
    try {
      const result = await fetchJSON(`${ENTITY_CONFIG.keywords.detailPath}${id}`);
      return { id: Number(id), name: result.name || `TMDB #${id}`, mode: "include" };
    } catch {
      return { id: Number(id), name: `TMDB #${id}`, mode: "include" };
    }
  }));

  const excKeywords = await Promise.all(excIds.map(async (id) => {
    try {
      const result = await fetchJSON(`${ENTITY_CONFIG.keywords.detailPath}${id}`);
      return { id: Number(id), name: result.name || `TMDB #${id}`, mode: "exclude" };
    } catch {
      return { id: Number(id), name: `TMDB #${id}`, mode: "exclude" };
    }
  }));

  const allKeywords = [...incKeywords, ...excKeywords];
  const seenIds = new Set();
  const seenNames = new Set();
  state.selectedEntities.keywords = [];
  for (const k of allKeywords) {
    const id = Number(k.id);
    const name = (k.name || "").trim().toLowerCase();
    if (seenIds.has(id) || (name && seenNames.has(name))) continue;
    seenIds.add(id);
    if (name) seenNames.add(name);
    state.selectedEntities.keywords.push(k);
  }
  renderSelectedEntities("keywords");

  const otherGroups = {
    actors: [...new Set((filters.include_actor_ids || []).map(Number))],
    directors: [...new Set((filters.include_director_ids || []).map(Number))],
    companies: [...new Set((filters.include_company_ids || []).map(Number))],
    excludedCompanies: [...new Set((filters.exclude_company_ids || []).map(Number))],
  };

  await Promise.all(Object.entries(otherGroups).map(async ([key, ids]) => {
    const config = ENTITY_CONFIG[key];
    if (!config) return;
    state.selectedEntities[key] = await Promise.all(ids.map(async (id) => {
      try {
        const result = await fetchJSON(`${config.detailPath}${id}`);
        return { id: Number(id), name: result.name || `TMDB #${id}` };
      } catch {
        return { id: Number(id), name: `TMDB #${id}` };
      }
    }));
    renderSelectedEntities(key);
  }));
}

function readOptionalNumber(input) {
  const value = input.value.trim();

  if (!value) {
    return null;
  }

  return Number(value);
}

function collectAdvancedFilters() {
  return {
    ...state.profilePassthroughFilters,
    include_genre_ids: getPickerValues("include-genres", true),
    exclude_genre_ids: getPickerValues("exclude-genres", true),
    genre_logic: elements.genreLogic.value,
    include_original_languages: getPickerValues("include-languages"),
    exclude_original_languages: getPickerValues("exclude-languages"),
    include_origin_countries: getPickerValues("include-countries"),
    exclude_origin_countries: [
      ...new Set([
        ...(state.profilePassthroughFilters.exclude_origin_countries || DEFAULT_SYSTEM_FILTERS.exclude_origin_countries),
      ]),
    ],
    include_actor_ids: state.selectedEntities.actors.map((item) => item.id),
    include_director_ids: state.selectedEntities.directors.map((item) => item.id),
    include_keyword_ids: [
      ...new Set(
        state.selectedEntities.keywords
          .filter((item) => item.mode !== "exclude")
          .map((item) => Number(item.id))
      ),
    ],
    exclude_keyword_ids: [
      ...new Set(
        state.selectedEntities.keywords
          .filter((item) => item.mode === "exclude")
          .map((item) => Number(item.id))
      ),
    ],
    include_company_ids: state.selectedEntities.companies.map((item) => item.id),
    exclude_company_ids: state.selectedEntities.excludedCompanies.map((item) => item.id),
    minimum_rating: readOptionalNumber(elements.minimumRating),
    maximum_rating: readOptionalNumber(elements.maximumRating),
    minimum_vote_count: readOptionalNumber(elements.minimumVotes),
    release_year_from: readOptionalNumber(elements.releaseYearFrom),
    release_year_to: readOptionalNumber(elements.releaseYearTo),
    sort_by: elements.sortBy.value,
  };
}

function collectPersonalFilters() {
  const notes = elements.notesQuery.value.trim();

  return {
    included_statuses: [
      ...document.querySelectorAll('input[name="included-status"]:checked'),
    ].map((input) => input.value),
    include_untracked: elements.includeUntracked.checked,
    notes_query: notes || null,
    favorite_only: elements.favoriteOnly.checked,
  };
}

function setWorkspaceCollapsed(collapsed, persist = true) {
  state.filtersCollapsed = Boolean(collapsed);
  elements.workspaceControls.classList.toggle("is-hidden", state.filtersCollapsed);
  elements.workspaceCollapse.setAttribute(
    "aria-expanded",
    String(!state.filtersCollapsed),
  );
  elements.workspaceCollapseLabel.textContent = state.filtersCollapsed
    ? "Show filters"
    : "Hide filters";
  elements.workspaceSummary.textContent = state.filtersCollapsed
    ? `${state.discoveryMode === "super" ? "Super Advanced" : state.discoveryMode === "advanced" ? "Advanced Search" : "Simple Discovery"} controls`
    : "Discovery controls";
  if (persist) scheduleSearchStateSave();
}

async function saveSearchState() {
  const selectedPreferenceId = Number(elements.profileSelect.value) || null;
  await fetchJSON("/search-state", {
    method: "PUT",
    body: JSON.stringify({
      mode: state.discoveryMode,
      filters: collectAdvancedFilters(),
      personal_filters: collectPersonalFilters(),
      selected_preference_id: selectedPreferenceId,
      filters_collapsed: state.filtersCollapsed,
    }),
  });
}

function scheduleSearchStateSave() {
  window.clearTimeout(state.searchStateTimer);
  state.searchStateTimer = window.setTimeout(() => {
    saveSearchState().catch(() => {
      // The workspace remains usable even if state persistence fails.
    });
  }, 450);
}

async function restoreSearchState() {
  try {
    const saved = await fetchJSON("/search-state");
    const filters = saved.filters && Object.keys(saved.filters).length > 0
      ? saved.filters
      : DEFAULT_SYSTEM_FILTERS;
    await setAdvancedFilters(filters);
    setPersonalFilters(saved.personal_filters || {});
    if (saved.selected_preference_id) {
      elements.profileSelect.value = String(saved.selected_preference_id);
    }
    updateProfileButtons();
    state.discoveryMode = "super";
    setWorkspaceCollapsed(Boolean(saved.filters_collapsed), false);
    return "super";
  } catch {
    await setAdvancedFilters(DEFAULT_SYSTEM_FILTERS);
    setWorkspaceCollapsed(false, false);
    return "super";
  }
}

function initializeCollapsibleFilters() {
  // Legacy collapsible filter buttons eradicated in favor of direct accordion triggers
}

function initializeNotesCollapsibleSections() {
  const setupToggle = (toggleBtn, sectionEl, storageKey) => {
    if (!toggleBtn || !sectionEl) return;
    const isSavedCollapsed = localStorage.getItem(storageKey) === "1";
    if (isSavedCollapsed) {
      sectionEl.classList.add("is-collapsed");
      toggleBtn.setAttribute("aria-expanded", "false");
    }
    toggleBtn.addEventListener("click", () => {
      const isCurrentlyCollapsed = sectionEl.classList.toggle("is-collapsed");
      toggleBtn.setAttribute("aria-expanded", isCurrentlyCollapsed ? "false" : "true");
      try {
        localStorage.setItem(storageKey, isCurrentlyCollapsed ? "1" : "0");
      } catch {}
    });
  };

  setupToggle(elements.notesTagsToggle, elements.notesTagsSection, "nope_notes_tags_collapsed");
  setupToggle(elements.notesTimelineToggle, elements.notesTimelineSection, "nope_notes_timeline_collapsed");
}

function updateFilterPillStates() {
  document.querySelectorAll(".filter-pill").forEach((pill) => {
    const targetId = pill.dataset.target;
    const card = document.getElementById(targetId);
    if (card) {
      pill.classList.toggle("is-open", !card.classList.contains("is-collapsed"));
    }
  });
}

function updateFilterPillBadges() {
  // Genres badge
  const genres = getPickerValues("include-genres").length;
  const badgeGenres = document.querySelector("#badge-genres");
  if (badgeGenres) {
    badgeGenres.textContent = String(genres);
    badgeGenres.classList.toggle("is-hidden", genres === 0);
  }
  document.querySelector("#pill-genres")?.classList.toggle("has-filters", genres > 0);

  // Rating badge
  const minRating = elements.minimumRating?.value?.trim();
  const maxRating = elements.maximumRating?.value?.trim();
  const ratingCount = minRating || maxRating ? 1 : 0;
  const badgeRating = document.querySelector("#badge-rating") || document.querySelector("#badge-quality");
  if (badgeRating) {
    badgeRating.textContent = String(ratingCount);
    badgeRating.classList.toggle("is-hidden", ratingCount === 0);
  }
  document.querySelector("#pill-rating")?.classList.toggle("has-filters", ratingCount > 0);
  document.querySelector("#pill-quality")?.classList.toggle("has-filters", ratingCount > 0);

  // Votes badge
  const minVotes = elements.minimumVotes?.value?.trim();
  const votesCount = minVotes ? 1 : 0;
  const badgeVotes = document.querySelector("#badge-votes");
  if (badgeVotes) {
    badgeVotes.textContent = String(votesCount);
    badgeVotes.classList.toggle("is-hidden", votesCount === 0);
  }
  document.querySelector("#pill-votes")?.classList.toggle("has-filters", votesCount > 0);

  // Sort badge
  const sortBy = elements.sortBy?.value;
  const isCustomSort = sortBy && sortBy !== "popularity.desc";
  document.querySelector("#pill-sort")?.classList.toggle("has-filters", Boolean(isCustomSort));

  // Year badge
  const yearFrom = elements.releaseYearFrom?.value?.trim();
  const yearTo = elements.releaseYearTo?.value?.trim();
  const yearCount = yearFrom || yearTo ? 1 : 0;
  const badgeYear = document.querySelector("#badge-year");
  if (badgeYear) {
    badgeYear.textContent = String(yearCount);
    badgeYear.classList.toggle("is-hidden", yearCount === 0);
  }
  document.querySelector("#pill-year")?.classList.toggle("has-filters", yearCount > 0);

  // Keywords badge
  const keywords = state.selectedEntities?.keywords?.length || 0;
  const excKeywords = state.selectedEntities?.excludedKeywords?.length || 0;
  const keywordCount = keywords + excKeywords;
  const badgeKeywords = document.querySelector("#badge-keywords");
  if (badgeKeywords) {
    badgeKeywords.textContent = String(keywordCount);
    badgeKeywords.classList.toggle("is-hidden", keywordCount === 0);
  }
  document.querySelector("#pill-keywords")?.classList.toggle("has-filters", keywordCount > 0);

  // Languages badge (silent default exclusions are not counted — they are not shown as chips)
  const incLang = getPickerValues("include-languages").length;
  const excLang = getPickerValues("exclude-languages")
    .filter((code) => !BACKGROUND_EXCLUDED_LANGUAGES.has(code)).length;
  const langCount = incLang + excLang;
  const badgeLang = document.querySelector("#badge-languages") || document.querySelector("#badge-origin");
  if (badgeLang) {
    badgeLang.textContent = String(langCount);
    badgeLang.classList.toggle("is-hidden", langCount === 0);
  }
  document.querySelector("#pill-languages")?.classList.toggle("has-filters", langCount > 0);
  document.querySelector("#pill-origin")?.classList.toggle("has-filters", langCount > 0);

  // Countries badge
  const incCountry = getPickerValues("include-countries").length;
  const badgeCountry = document.querySelector("#badge-countries");
  if (badgeCountry) {
    badgeCountry.textContent = String(incCountry);
    badgeCountry.classList.toggle("is-hidden", incCountry === 0);
  }
  document.querySelector("#pill-countries")?.classList.toggle("has-filters", incCountry > 0);

  // Cast & Crew badge
  const actors = state.selectedEntities?.actors?.length || 0;
  const directors = state.selectedEntities?.directors?.length || 0;
  const peopleCount = actors + directors;
  const badgePeople = document.querySelector("#badge-people");
  if (badgePeople) {
    badgePeople.textContent = String(peopleCount);
    badgePeople.classList.toggle("is-hidden", peopleCount === 0);
  }
  document.querySelector("#pill-people")?.classList.toggle("has-filters", peopleCount > 0);

  // Studios badge
  const companies = state.selectedEntities?.companies?.length || 0;
  const excCompanies = state.selectedEntities?.excludedCompanies?.length || 0;
  const companyCount = companies + excCompanies;
  const badgeCompanies = document.querySelector("#badge-companies");
  if (badgeCompanies) {
    badgeCompanies.textContent = String(companyCount);
    badgeCompanies.classList.toggle("is-hidden", companyCount === 0);
  }
  document.querySelector("#pill-companies")?.classList.toggle("has-filters", companyCount > 0);

  // Library badge
  const checkedStatuses = document.querySelectorAll('input[name="included-status"]:checked').length;
  const includeUntracked = elements.includeUntracked?.checked ? 1 : 0;
  const libraryTotal = checkedStatuses + includeUntracked;
  const badgeLibrary = document.querySelector("#badge-library");
  if (badgeLibrary) {
    badgeLibrary.classList.add("is-hidden");
  }
  const watchedChecked = document.querySelector('input[name="included-status"][value="watched"]')?.checked;
  const rewatchChecked = document.querySelector('input[name="included-status"][value="rewatch"]')?.checked;
  const nopeChecked = document.querySelector('input[name="included-status"][value="excluded"]')?.checked;
  document.querySelector("#pill-library")?.classList.toggle("has-filters", Boolean(watchedChecked || rewatchChecked || nopeChecked));
}

function renderActiveFilterTags() {
  const container = document.querySelector("#active-filter-tags");
  if (!container) return;

  const chips = [];

  // Genres
  getPickerValues("include-genres", true).forEach((id) => {
    const pair = GENRE_OPTIONS.find((item) => item[0] === id);
    const name = pair ? pair[1] : `Genre ${id}`;
    chips.push({
      label: name,
      onRemove: () => {
        const input = document.querySelector(`#include-genres input[value="${id}"]`);
        if (input) input.checked = false;
        syncTriPickers();
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  });

  // Languages Include
  getPickerValues("include-languages").forEach((code) => {
    const pair = LANGUAGE_OPTIONS.find((item) => item[0] === code);
    const name = pair ? pair[1] : code;
    chips.push({
      label: name,
      onRemove: () => {
        const input = document.querySelector(`#include-languages input[value="${code}"]`);
        if (input) input.checked = false;
        syncTriPickers();
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  });

  // Countries
  getPickerValues("include-countries").forEach((code) => {
    const pair = COUNTRY_OPTIONS.find((item) => item[0] === code);
    const name = pair ? pair[1] : code;
    chips.push({
      label: name,
      onRemove: () => {
        const input = document.querySelector(`#include-countries input[value="${code}"]`);
        if (input) input.checked = false;
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  });

  // Rating
  const minRating = elements.minimumRating?.value?.trim();
  const maxRating = elements.maximumRating?.value?.trim();
  if (minRating || maxRating) {
    chips.push({
      label: `⭐ ${minRating || '0'}–${maxRating || '10'}`,
      onRemove: () => {
        if (elements.minimumRating) elements.minimumRating.value = "";
        if (elements.maximumRating) elements.maximumRating.value = "";
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  }

  // Year
  const yearFrom = elements.releaseYearFrom?.value?.trim();
  const yearTo = elements.releaseYearTo?.value?.trim();
  if (yearFrom || yearTo) {
    chips.push({
      label: `📅 ${yearFrom || '…'}–${yearTo || '…'}`,
      onRemove: () => {
        if (elements.releaseYearFrom) elements.releaseYearFrom.value = "";
        if (elements.releaseYearTo) elements.releaseYearTo.value = "";
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  }

  // Watched included
  const watchedInput = document.querySelector('input[name="included-status"][value="watched"]');
  if (watchedInput?.checked) {
    chips.push({
      label: `✓ Include Watched`,
      onRemove: () => {
        watchedInput.checked = false;
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  }

  // Rewatch included
  const rewatchInput = document.querySelector('input[name="included-status"][value="rewatch"]');
  if (rewatchInput?.checked) {
    chips.push({
      label: `↻ Include Rewatch`,
      onRemove: () => {
        rewatchInput.checked = false;
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  }

  // Nope included
  const nopeInput = document.querySelector('input[name="included-status"][value="excluded"]');
  if (nopeInput?.checked) {
    chips.push({
      label: `× Include Nope`,
      onRemove: () => {
        nopeInput.checked = false;
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  }

  // People
  (state.selectedEntities?.directors || []).forEach((d) => {
    chips.push({
      label: `Director: ${d.name}`,
      onRemove: () => {
        state.selectedEntities.directors = state.selectedEntities.directors.filter((item) => item.id !== d.id);
        renderSelectedEntities("directors");
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  });
  (state.selectedEntities?.actors || []).forEach((a) => {
    chips.push({
      label: `Actor: ${a.name}`,
      onRemove: () => {
        state.selectedEntities.actors = state.selectedEntities.actors.filter((item) => item.id !== a.id);
        renderSelectedEntities("actors");
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  });
  (state.selectedEntities?.keywords || []).forEach((k) => {
    const isExcluded = k.mode === "exclude";
    chips.push({
      label: `${isExcluded ? "− " : "+ "}${k.name}`,
      isExcluded: isExcluded,
      onRemove: () => {
        state.selectedEntities.keywords = state.selectedEntities.keywords.filter((item) => item.id !== k.id);
        renderSelectedEntities("keywords");
        updateFilterPillBadges();
        renderActiveFilterTags();
        runDiscoverySearch();
      },
    });
  });

  if (!chips.length) {
    container.replaceChildren();
    container.classList.add("is-hidden");
    return;
  }

  container.classList.remove("is-hidden");
  container.replaceChildren();

  chips.forEach((chip) => {
    const el = document.createElement("span");
    el.className = "active-filter-chip";
    if (chip.isExcluded) {
      el.classList.add("is-excluded");
    }
    el.textContent = chip.label;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "✕";
    btn.title = `Remove ${chip.label}`;
    btn.addEventListener("click", chip.onRemove);
    el.append(btn);
    container.append(el);
  });

  const clearBtn = document.createElement("button");
  clearBtn.type = "button";
  clearBtn.className = "active-filter-clear-all";
  clearBtn.textContent = "Clear all filters";
  clearBtn.addEventListener("click", () => {
    resetAdvancedFilters();
    updateFilterPillBadges();
    renderActiveFilterTags();
    runDiscoverySearch();
  });
  container.append(clearBtn);
}

function updateSidebarExpandedState() {
  // Static fixed sidebar width: zero dynamic expansion or layout shifting
}

function setupFilterPills() {
  const pills = document.querySelectorAll(".filter-pill");
  pills.forEach((pill) => {
    pill.addEventListener("click", (e) => {
      e.stopPropagation();
      const targetId = pill.dataset.target;
      const card = document.getElementById(targetId);
      if (!card) return;

      const willOpen = card.classList.contains("is-collapsed");

      // Independent drawer: toggle only this drawer
      if (willOpen) {
        card.classList.remove("is-collapsed");
        pill.classList.add("is-open");
        pill.setAttribute("aria-expanded", "true");
      } else {
        card.classList.add("is-collapsed");
        pill.classList.remove("is-open");
        pill.setAttribute("aria-expanded", "false");
      }

      updateSidebarExpandedState();
      setWorkspaceCollapsed(false);

      if (willOpen) {
        card.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    });
  });

  // Top Search button
  const topSearchBtn = document.querySelector("#run-advanced-search");
  if (topSearchBtn) {
    topSearchBtn.addEventListener("click", async (e) => {
      e.preventDefault();
      pills.forEach((p) => {
        p.classList.remove("is-open");
        p.setAttribute("aria-expanded", "false");
        const c = document.getElementById(p.dataset.target);
        if (c) c.classList.add("is-collapsed");
      });
      updateSidebarExpandedState();
      await runDiscoverySearch();
    });
  }

  // Top Reset button
  const topResetBtn = document.querySelector("#reset-filters");
  if (topResetBtn) {
    topResetBtn.addEventListener("click", () => {
      resetAdvancedFilters();
      pills.forEach((p) => {
        p.classList.remove("is-open");
        p.setAttribute("aria-expanded", "false");
        const c = document.getElementById(p.dataset.target);
        if (c) c.classList.add("is-collapsed");
      });
      updateSidebarExpandedState();
      updateFilterPillBadges();
      renderActiveFilterTags();
      runDiscoverySearch();
    });
  }

  elements.advancedForm?.addEventListener("change", () => {
    updateFilterPillBadges();
    renderActiveFilterTags();
  });

  updateFilterPillBadges();
  renderActiveFilterTags();
  updateFilterPillStates();
  updateSidebarExpandedState();
}

function setupSidebarMasterToggle() {
  const masterToggle = document.querySelector("#sidebar-master-toggle");
  const masterIcon = document.querySelector("#sidebar-master-toggle-icon");
  const appLayout = document.querySelector("#app-layout");
  const sidebar = document.querySelector("#app-sidebar");

  if (!masterToggle || !sidebar || !appLayout) return;

  masterToggle.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    const isNowCollapsed = !sidebar.classList.contains("is-collapsed");
    sidebar.classList.toggle("is-collapsed", isNowCollapsed);
    appLayout.classList.toggle("has-collapsed-sidebar", isNowCollapsed);
    if (masterIcon) {
      masterIcon.textContent = isNowCollapsed ? "▶" : "◀";
    }
    masterToggle.setAttribute("aria-label", isNowCollapsed ? "Expand sidebar" : "Collapse sidebar");
    masterToggle.setAttribute("title", isNowCollapsed ? "Expand sidebar" : "Collapse sidebar");
  });
}

function setupGenreModeToggle() {
  const excludeBtn = document.querySelector("#genre-mode-exclude");
  const includeBtn = document.querySelector("#genre-mode-include");
  if (!excludeBtn || !includeBtn) return;

  excludeBtn.addEventListener("click", () => {
    state.genreMode = "exclude";
    excludeBtn.classList.add("is-active");
    includeBtn.classList.remove("is-active");
  });

  includeBtn.addEventListener("click", () => {
    state.genreMode = "include";
    includeBtn.classList.add("is-active");
    excludeBtn.classList.remove("is-active");
  });
}

function initializeOutsideClosing() {
  document.addEventListener("click", (event) => {
    document.querySelectorAll(".multi-picker-menu[open]").forEach((menu) => {
      if (!menu.contains(event.target)) menu.open = false;
    });
    document.querySelectorAll(".entity-results:not(.is-hidden)").forEach((menu) => {
      if (!menu.parentElement.contains(event.target)) menu.classList.add("is-hidden");
    });
  });
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    document.querySelectorAll(".multi-picker-menu[open]").forEach((menu) => {
      menu.open = false;
    });
    document.querySelectorAll(".entity-results").forEach((menu) => {
      menu.classList.add("is-hidden");
    });
    document.querySelectorAll(".filter-pill.is-open").forEach((p) => {
      p.classList.remove("is-open");
      p.setAttribute("aria-expanded", "false");
      const c = document.getElementById(p.dataset.target);
      if (c) c.classList.add("is-collapsed");
    });
    updateSidebarExpandedState();
  });
}

async function setAdvancedFilters(filters = {}) {
  const mergedFilters = {
    ...DEFAULT_SYSTEM_FILTERS,
    ...filters,
    include_original_languages: (filters.include_original_languages && filters.include_original_languages.length > 0)
      ? filters.include_original_languages
      : DEFAULT_SYSTEM_FILTERS.include_original_languages,
    exclude_original_languages: (filters.exclude_original_languages && filters.exclude_original_languages.length > 0)
      ? filters.exclude_original_languages
      : DEFAULT_SYSTEM_FILTERS.exclude_original_languages,
    exclude_origin_countries: (filters.exclude_origin_countries && filters.exclude_origin_countries.length > 0)
      ? filters.exclude_origin_countries
      : DEFAULT_SYSTEM_FILTERS.exclude_origin_countries,
  };
  state.profilePassthroughFilters = { ...mergedFilters };
  setPickerValues("include-genres", mergedFilters.include_genre_ids);
  setPickerValues("exclude-genres", mergedFilters.exclude_genre_ids);
  setPickerValues("include-languages", mergedFilters.include_original_languages);
  setPickerValues("exclude-languages", mergedFilters.exclude_original_languages);
  setPickerValues("include-countries", mergedFilters.include_origin_countries);
  elements.genreLogic.value = mergedFilters.genre_logic || "or";
  elements.minimumRating.value = mergedFilters.minimum_rating ?? "";
  elements.maximumRating.value = mergedFilters.maximum_rating ?? "";
  elements.minimumVotes.value = mergedFilters.minimum_vote_count ?? "";
  elements.releaseYearFrom.value = mergedFilters.release_year_from ?? "";
  elements.releaseYearTo.value = mergedFilters.release_year_to ?? "";
  elements.sortBy.value = mergedFilters.sort_by || "popularity.desc";
  syncSortChips(elements.sortBy.value);
  await hydrateEntitySelections(mergedFilters);
  updateFilterPillBadges();
  renderActiveFilterTags();
}

function setPersonalFilters(filters = {}) {
  const included = new Set(
    filters.included_statuses || ["new_discovery", "watch_later"],
  );
  document.querySelectorAll('input[name="included-status"]').forEach((input) => {
    input.checked = included.has(input.value);
  });
  elements.includeUntracked.checked = filters.include_untracked ?? true;
  elements.notesQuery.value = filters.notes_query || "";
  if (elements.favoriteOnly) {
    elements.favoriteOnly.checked = false;
  }
  updateFilterPillBadges();
  renderActiveFilterTags();
}

function showLoadingCards() {
  elements.empty.classList.add("is-hidden");
  elements.grid.classList.remove("is-hidden");
  elements.grid.replaceChildren();

  for (let index = 0; index < 10; index += 1) {
    const card = document.createElement("div");
    card.className = "skeleton-card";

    const poster = document.createElement("div");
    poster.className = "skeleton-poster";

    const title = document.createElement("div");
    title.className = "skeleton-line";

    const meta = document.createElement("div");
    meta.className = "skeleton-line short";

    card.append(poster, title, meta);
    elements.grid.append(card);
  }
}

function getMovieId(movie) {
  return movie.tmdb_id ?? movie.id;
}

function getMovieYear(movie) {
  if (movie.release_year) {
    return movie.release_year;
  }

  if (movie.release_date) {
    return String(movie.release_date).slice(0, 4);
  }

  return "Year unknown";
}

function getMovieRating(movie) {
  const rating = movie.rating ?? movie.vote_average;

  if (rating === null || rating === undefined) {
    return null;
  }

  const numericRating = Number(rating);

  if (!Number.isFinite(numericRating) || numericRating <= 0) {
    return null;
  }

  return numericRating.toFixed(1);
}

function getMovieLanguage(movie) {
  const code = String(movie.original_language || "").toLowerCase();
  const match = LANGUAGE_OPTIONS.find(([value]) => value === code);
  return match ? match[1] : (code ? code.toUpperCase() : "Language unknown");
}

function getStatus(movie) {
  return movie.user_data?.status || null;
}

function getInitials(title) {
  const words = String(title || "Movie")
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 3);

  return words.map((word) => word[0]).join("").toUpperCase() || "ME";
}

function createPoster(movie, className = "") {
  const title = movie.title || movie.original_title || "Untitled movie";

  if (movie.poster_path) {
    const image = document.createElement("img");
    image.src = `${IMAGE_BASE_URL}${movie.poster_path}`;
    image.alt = `${title} poster`;
    image.loading = "lazy";
    image.decoding = "async";
    image.className = className;
    image.addEventListener(
      "error",
      () => {
        image.replaceWith(createPosterFallback(title));
      },
      { once: true },
    );
    return image;
  }

  return createPosterFallback(title);
}

function createPosterFallback(title) {
  const fallback = document.createElement("div");
  fallback.className = "poster-fallback";
  fallback.textContent = getInitials(title);
  fallback.setAttribute("aria-label", `${title} poster unavailable`);
  return fallback;
}

function createMovieCard(movie) {
  const movieId = getMovieId(movie);
  const title = movie.title || movie.original_title || "Untitled movie";
  const status = getStatus(movie);
  const article = document.createElement("article");
  article.className = "movie-card";
  article.dataset.movieId = movieId;

  const posterButton = document.createElement("button");
  posterButton.type = "button";
  posterButton.className = "poster-button";
  posterButton.setAttribute("aria-label", `Open details for ${title}`);
  const yearText = getMovieYear(movie);
  const isNotesView = state.mode === "movie-notes" || state.mode === "movie-notes-search";
  const notesText = isNotesView ? movie.user_data?.notes : null;
  posterButton.title = `${title}${yearText ? ` (${yearText})` : ""}${notesText ? `\n📝 ${notesText}` : ""}`;
  if (status === "excluded" && state.currentView === "discover") {
    article.classList.add("is-noped");
  }

  posterButton.append(createPoster(movie));
  posterButton.addEventListener("click", (event) => {
    if (state.nopeMode && state.currentView === "discover") {
      event.preventDefault();
      event.stopPropagation();
      handleQuickNope(movie, article);
      return;
    }
    openMovieDetails(movieId);
  });

  if (movie.user_data?.is_favorite) {
    const favorite = document.createElement("span");
    favorite.className = "favorite-mark";
    favorite.textContent = "♥";
    favorite.setAttribute("aria-label", "Favourite");
    posterButton.append(favorite);
  }

  if (notesText) {
    const noteMark = document.createElement("span");
    noteMark.className = "card-note-mark";
    noteMark.textContent = "📝";
    noteMark.setAttribute("aria-label", "Has note");
    posterButton.append(noteMark);
  }

  const statusBadge = document.createElement("span");
  statusBadge.className = "status-badge";
  statusBadge.dataset.status = status || "untracked";
  statusBadge.textContent = status ? STATUS_LABELS[status] : "Untracked";
  posterButton.append(statusBadge);

  const rating = getMovieRating(movie);

  if (rating) {
    const ratingElement = document.createElement("span");
    ratingElement.className = "card-rating";
    ratingElement.textContent = rating;
    posterButton.append(ratingElement);
  }

  const copy = document.createElement("div");
  copy.className = "card-copy";

  const heading = document.createElement("h3");
  heading.textContent = title;
  heading.title = title;

  const meta = document.createElement("p");
  const year = document.createElement("span");
  year.textContent = yearText;
  const language = document.createElement("span");
  language.textContent = getMovieLanguage(movie);
  meta.append(year, language);

  copy.append(heading, meta);

  if (isNotesView && movie.user_data?.notes) {
    article.classList.add("has-notes");
    const noteSnippet = document.createElement("p");
    noteSnippet.className = "card-note-snippet";
    noteSnippet.innerHTML = formatRichText(movie.user_data.notes);
    copy.append(noteSnippet);
  }

  article.append(posterButton, copy);
  return article;
}

function hasActiveShelfFilters() {
  const q = (elements.libraryFilterQuery?.value || "").trim();
  const yearFrom = parseInt(elements.libYearFrom?.value, 10);
  const yearTo = parseInt(elements.libYearTo?.value, 10);
  const selectedKw = state.selectedEntities?.libKeywords || [];
  const selectedPeople = [
    ...(state.selectedEntities?.libDirectors || []),
    ...(state.selectedEntities?.libActors || []),
  ];
  return Boolean(
    q ||
    state.libSelectedGenres?.size > 0 ||
    !isNaN(yearFrom) ||
    !isNaN(yearTo) ||
    state.libSelectedLanguages?.size > 0 ||
    selectedKw.length > 0 ||
    selectedPeople.length > 0
  );
}

function renderMovies(movies, emptyContext = "library", total = null) {
  clearNopeUndo();
  elements.grid.replaceChildren();
  const count = total ?? movies.length;
  elements.count.textContent = `${count} ${
    count === 1 ? "movie" : "movies"
  }`;
  if (elements.shelfCount) {
    elements.shelfCount.textContent = `${count} ${count === 1 ? "movie" : "movies"}`;
  }

  if (movies.length === 0) {
    elements.grid.classList.add("is-hidden");
    elements.empty.classList.remove("is-hidden");

    if (emptyContext === "search") {
      elements.emptyTitle.textContent = "No matching movies";
      elements.emptyCopy.textContent =
        "Try another title or use fewer words in your search.";
      if (elements.emptySearchButton) {
        elements.emptySearchButton.textContent = "Search movies";
        elements.emptySearchButton.classList.remove("is-hidden");
        elements.emptySearchButton.onclick = () => elements.query?.focus();
      }
    } else if (hasActiveShelfFilters() || state.isSearchingLibrary) {
      elements.emptyTitle.textContent = "No movies match your filters";
      elements.emptyCopy.textContent =
        "Try adjusting or clearing your active filters to see your movies.";
      if (elements.emptySearchButton) {
        elements.emptySearchButton.textContent = "Reset filters";
        elements.emptySearchButton.classList.remove("is-hidden");
        elements.emptySearchButton.onclick = () => {
          resetLibraryFilters();
        };
      }
    } else if (state.currentView === "movie-notes") {
      if (state.mode === "movie-notes-search") {
        elements.emptyTitle.textContent = "No matching notes";
        elements.emptyCopy.textContent =
          "No movies found with notes matching that search.";
        if (elements.emptySearchButton) {
          elements.emptySearchButton.textContent = "Clear notes search";
          elements.emptySearchButton.classList.remove("is-hidden");
          elements.emptySearchButton.onclick = () => {
            if (elements.notesSearchInput) elements.notesSearchInput.value = "";
            searchLocalNotes("");
          };
        }
      } else {
        elements.emptyTitle.textContent = "No movie notes yet";
        elements.emptyCopy.textContent =
          "Open any movie and write your personal thoughts or reflections to collect them here.";
        if (elements.emptySearchButton) {
          elements.emptySearchButton.textContent = "Search movies";
          elements.emptySearchButton.classList.remove("is-hidden");
          elements.emptySearchButton.onclick = () => elements.query?.focus();
        }
      }
    } else {
      const shelfEmptyInfo = {
        watched: { title: "No watched movies yet", copy: "Movies you mark as watched will appear here." },
        watch_later: { title: "Watch Later is empty", copy: "Add movies you plan to watch to keep track of them here." },
        rewatch: { title: "Rewatch list is empty", copy: "Mark movies for a rewatch to see them here." },
        favorites: { title: "No favourites yet", copy: "Star your favorite movies to keep them in this collection." },
        excluded: { title: "No excluded movies", copy: "Movies you NOPE will be safely stored here." },
        new_discovery: { title: "No new discoveries", copy: "Discover new movies to explore them here." },
      };
      const info = shelfEmptyInfo[state.currentView] || {
        title: "Nothing here yet",
        copy: "Search for a movie above and give it a personal status.",
      };
      elements.emptyTitle.textContent = info.title;
      elements.emptyCopy.textContent = info.copy;
      if (elements.emptySearchButton) {
        elements.emptySearchButton.textContent = "Search movies";
        elements.emptySearchButton.classList.remove("is-hidden");
        elements.emptySearchButton.onclick = () => elements.query?.focus();
      }
    }

    return;
  }

  elements.empty.classList.add("is-hidden");
  elements.grid.classList.remove("is-hidden");

  movies.forEach((movie) => {
    elements.grid.append(createMovieCard(movie));
  });
}

function renderPagination(
  container,
  page,
  totalPages,
  onPage,
  { exact = true, hasNext = page < totalPages } = {},
) {
  container.replaceChildren();
  if ((!exact && page <= 1 && !hasNext) || (exact && totalPages <= 1)) {
    container.classList.add("is-hidden");
    return;
  }
  container.classList.remove("is-hidden");
  const addButton = (label, target, disabled = false, current = false) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.disabled = disabled;
    button.classList.toggle("is-current", current);
    if (current) button.setAttribute("aria-current", "page");
    button.addEventListener("click", () => onPage(target));
    container.append(button);
  };
  addButton("← Previous", page - 1, page <= 1);
  if (!exact) {
    const current = document.createElement("span");
    current.className = "pagination-current-label";
    current.textContent = `Page ${page}`;
    container.append(current);
    addButton("Next →", page + 1, !hasNext);
    return;
  }
  const pages = new Set([1, totalPages]);
  for (let item = Math.max(1, page - 2); item <= Math.min(totalPages, page + 2); item += 1) {
    pages.add(item);
  }
  let previous = 0;
  [...pages].sort((a, b) => a - b).forEach((item) => {
    if (item - previous > 1) {
      const ellipsis = document.createElement("span");
      ellipsis.textContent = "…";
      container.append(ellipsis);
    }
    addButton(String(item), item, false, item === page);
    previous = item;
  });
  addButton("Next →", page + 1, page >= totalPages);
}

function scrollToResults() {
  document.querySelector(".section-heading").scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

function setSearchOriginMovie(movie = null) {
  state.searchOriginMovie = movie
    ? { id: Number(movie.id), title: movie.title || "movie" }
    : null;
  if (!state.searchOriginMovie) {
    elements.returnToOrigin.classList.add("is-hidden");
    elements.returnToOrigin.textContent = "";
    return;
  }
  elements.returnToOrigin.textContent = `← Return to ${state.searchOriginMovie.title}`;
  elements.returnToOrigin.classList.remove("is-hidden");
}

function setAuxiliaryView(view = null) {
  const sections = {
    entries: elements.entriesPage,
    "entry-reader": elements.entryReader,
    "looking-out": elements.lookingOutPage,
    storage: elements.storagePage,
  };
  Object.entries(sections).forEach(([name, section]) => {
    section.classList.toggle("is-hidden", view !== name);
  });
  const visible = Boolean(view);
  document.querySelector(".section-heading")?.classList.toggle("is-hidden", visible);
  elements.grid?.classList.toggle("force-hidden", visible);
  elements.empty?.classList.toggle("force-hidden", visible);
  const discoverHeader = document.querySelector("#discover-canvas-header");
  if (discoverHeader) {
    discoverHeader.classList.toggle("is-hidden", visible || state.currentView !== "discover");
    discoverHeader.classList.toggle("force-hidden", visible || state.currentView !== "discover");
  }
  if (elements.pagination) {
    elements.pagination.classList.toggle("force-hidden", visible);
    if (visible) elements.pagination.classList.add("is-hidden");
  }
  if (elements.discoverWorkspace) {
    elements.discoverWorkspace.classList.toggle("force-hidden", visible);
    if (visible) elements.discoverWorkspace.classList.add("is-hidden");
  }
  if (elements.notesSearchContainer) {
    elements.notesSearchContainer.classList.toggle("force-hidden", visible);
  }
  if (view && history.replaceState) {
    if (view === "entry-reader" && state.entryReaderEntry?.entry_id) {
      history.replaceState(null, "", `#entry-reader:${state.entryReaderEntry.entry_id}`);
    } else {
      history.replaceState(null, "", `#${view}`);
    }
  }
}

function setEntriesVisible(visible) {
  setAuxiliaryView(visible ? "entries" : null);
}

async function activateDiscoverView() {
  setSearchOriginMovie();
  setEntriesVisible(false);
  if (elements.discoverWorkspace) {
    elements.discoverWorkspace.classList.remove("is-hidden");
  }
  if (elements.notesSearchContainer) {
    elements.notesSearchContainer.classList.add("is-hidden");
  }
  setActiveView("discover");
  await setDiscoveryMode(state.discoveryMode || "simple", true);
}

function updateLibraryFilterBadges() {
  const setBadge = (el, count) => {
    if (!el) return;
    el.textContent = String(count);
    el.classList.toggle("is-hidden", count <= 0);
  };
  setBadge(elements.badgeLibGenres, state.libSelectedGenres.size);
  const yearCount = (elements.libYearFrom?.value ? 1 : 0) + (elements.libYearTo?.value ? 1 : 0);
  setBadge(elements.badgeLibYear, yearCount);
  setBadge(elements.badgeLibKeywords, (state.selectedEntities.libKeywords || []).length);
  const peopleCount = (state.selectedEntities.libDirectors || []).length + (state.selectedEntities.libActors || []).length;
  setBadge(elements.badgeLibPeople, peopleCount);
  setBadge(elements.badgeLibLanguages, state.libSelectedLanguages.size);
}

function applyLibraryFilters(targetPage = 1) {
  if (!state.unfilteredShelfMovies) {
    state.unfilteredShelfMovies = [...(state.movies || [])];
  }
  let list = [...state.unfilteredShelfMovies];

  // 1. Text filter
  const q = (elements.libraryFilterQuery?.value || "").trim().toLowerCase();
  if (q) {
    list = list.filter((m) => {
      const title = (m.title || "").toLowerCase();
      const overview = (m.overview || "").toLowerCase();
      const notes = (m.user_data?.notes || "").toLowerCase();
      return title.includes(q) || overview.includes(q) || notes.includes(q);
    });
  }

  // 2. Genres
  if (state.libSelectedGenres.size > 0) {
    list = list.filter((m) => {
      const movieGenreIds = (m.genres || [])
        .map((g) => Number(g.id || g.tmdb_genre_id))
        .concat((m.genre_ids || []).map(Number))
        .filter((id) => !isNaN(id) && id > 0);
      return [...state.libSelectedGenres].some((id) => movieGenreIds.includes(id));
    });
  }

  // 3. Release Year
  const yearFrom = parseInt(elements.libYearFrom?.value, 10);
  const yearTo = parseInt(elements.libYearTo?.value, 10);
  if (!isNaN(yearFrom)) {
    list = list.filter((m) => {
      const y = parseInt(getMovieYear(m), 10);
      return !isNaN(y) && y >= yearFrom;
    });
  }
  if (!isNaN(yearTo)) {
    list = list.filter((m) => {
      const y = parseInt(getMovieYear(m), 10);
      return !isNaN(y) && y <= yearTo;
    });
  }

  // 4. Languages
  if (state.libSelectedLanguages.size > 0) {
    list = list.filter((m) => {
      const code = String(m.original_language || "").toLowerCase();
      return state.libSelectedLanguages.has(code);
    });
  }

  // 5. Keywords
  const selectedKw = (state.selectedEntities.libKeywords || []).map((k) =>
    (k.raw_name || k.name || "").replace(/^[🏷️\s]+/, "").trim().toLowerCase()
  );
  if (selectedKw.length > 0) {
    list = list.filter((m) => {
      const overview = (m.overview || "").toLowerCase();
      const title = (m.title || "").toLowerCase();
      const notes = (m.user_data?.notes || "").toLowerCase();
      const movieKeywords = (m.keywords || []).map((k) => (k.name || "").toLowerCase());
      return selectedKw.some((kw) =>
        movieKeywords.some((mk) => mk.includes(kw) || kw.includes(mk)) ||
        overview.includes(kw) ||
        title.includes(kw) ||
        notes.includes(kw)
      );
    });
  }

  // 6. People (Actors / Directors)
  const selectedDirectors = (state.selectedEntities.libDirectors || []).map((p) => (p.name || "").trim().toLowerCase());
  if (selectedDirectors.length > 0) {
    list = list.filter((m) => {
      const movieDirs = (m.directors || []).map((d) => (typeof d === "string" ? d : d.name || "").toLowerCase());
      return selectedDirectors.some((name) => movieDirs.some((d) => d.includes(name) || name.includes(d)));
    });
  }

  const selectedActors = (state.selectedEntities.libActors || []).map((p) => (p.name || "").trim().toLowerCase());
  if (selectedActors.length > 0) {
    list = list.filter((m) => {
      const movieActors = (m.actors || []).map((a) => (typeof a === "string" ? a : a.name || "").toLowerCase());
      return selectedActors.some((name) => movieActors.some((a) => a.includes(name) || name.includes(a)));
    });
  }

  // 7. Sorting — applied across the ENTIRE collection before pagination
  const sortBy = elements.libSortCloud?.querySelector(".filter-chip.is-active")?.dataset.sort || "recent";
  if (sortBy === "title_asc") {
    list.sort((a, b) => (a.title || "").localeCompare(b.title || ""));
  } else if (sortBy === "year_desc") {
    list.sort((a, b) => {
      const dateA = a.release_date || (a.release_year ? `${a.release_year}-01-01` : "");
      const dateB = b.release_date || (b.release_year ? `${b.release_year}-01-01` : "");
      const comp = dateB.localeCompare(dateA);
      return comp !== 0 ? comp : (a.title || "").localeCompare(b.title || "");
    });
  } else if (sortBy === "year_asc") {
    list.sort((a, b) => {
      const dateA = a.release_date || (a.release_year ? `${a.release_year}-01-01` : "9999-99-99");
      const dateB = b.release_date || (b.release_year ? `${b.release_year}-01-01` : "9999-99-99");
      const comp = (dateA || "9999-99-99").localeCompare(dateB || "9999-99-99");
      return comp !== 0 ? comp : (a.title || "").localeCompare(b.title || "");
    });
  } else if (sortBy === "recent") {
    list.sort((a, b) => {
      const dateA = a.user_data?.updated_at || a.user_data?.created_at || "";
      const dateB = b.user_data?.updated_at || b.user_data?.created_at || "";
      const comp = dateB.localeCompare(dateA);
      return comp !== 0 ? comp : (a.title || "").localeCompare(b.title || "");
    });
  }

  updateLibraryFilterBadges();

  const hasActiveFilters = hasActiveLibraryFilters();
  state.allFilteredMovies = list;
  const totalMatches = list.length;
  const pageSize = 30;
  const totalPages = Math.max(1, Math.ceil(totalMatches / pageSize));
  const safePage = Math.min(Math.max(1, targetPage), totalPages);
  state.searchPage = safePage;
  state.searchTotalPages = totalPages;

  const pageResults = list.slice((safePage - 1) * pageSize, safePage * pageSize);
  state.movies = pageResults;

  renderMovies(state.movies, "library", totalMatches);

  if (hasActiveFilters || state.isSearchingLibrary) {
    if (state.totalResults && state.totalResults > totalMatches) {
      const text = `${totalMatches} of ${state.totalResults} ${state.totalResults === 1 ? "movie" : "movies"}`;
      elements.count.textContent = text;
      if (elements.shelfCount) elements.shelfCount.textContent = text;
    } else {
      const text = `${totalMatches} ${totalMatches === 1 ? "movie" : "movies"}`;
      elements.count.textContent = text;
      if (elements.shelfCount) elements.shelfCount.textContent = text;
    }
  } else {
    const text = `${totalMatches} ${totalMatches === 1 ? "movie" : "movies"}`;
    elements.count.textContent = text;
    if (elements.shelfCount) elements.shelfCount.textContent = text;
  }

  if (totalPages > 1) {
    elements.pagination.classList.remove("is-hidden");
    elements.pagination.classList.remove("force-hidden");
    renderPagination(
      elements.pagination,
      state.searchPage,
      state.searchTotalPages,
      (target) => {
        applyLibraryFilters(target);
        scrollToResults();
      }
    );
  } else {
    elements.pagination.classList.add("is-hidden");
  }
}

function hasActiveLibraryFilters() {
  const q = (elements.libraryFilterQuery?.value || "").trim();
  const yearFrom = parseInt(elements.libYearFrom?.value, 10);
  const yearTo = parseInt(elements.libYearTo?.value, 10);
  const hasGenres = Boolean(state.libSelectedGenres && state.libSelectedGenres.size > 0);
  const hasLangs = Boolean(state.libSelectedLanguages && state.libSelectedLanguages.size > 0);
  const hasKw = Boolean(state.selectedEntities.libKeywords && state.selectedEntities.libKeywords.length > 0);
  const hasDirs = Boolean(state.selectedEntities.libDirectors && state.selectedEntities.libDirectors.length > 0);
  const hasActors = Boolean(state.selectedEntities.libActors && state.selectedEntities.libActors.length > 0);
  return Boolean(
    q ||
    hasGenres ||
    !isNaN(yearFrom) ||
    !isNaN(yearTo) ||
    hasLangs ||
    hasKw ||
    hasDirs ||
    hasActors
  );
}

function reloadCurrentLibraryView() {
  if (state.currentView === "movie-notes") {
    return loadMovieNotes(1);
  }
  if (state.currentView && state.currentView !== "discover" && state.currentView in VIEW_COPY) {
    return loadShelf(state.currentView, 1);
  }
  return null;
}

function resetLibraryFilters({ silent = false } = {}) {
  const wasSearching = state.isSearchingLibrary;
  if (elements.libraryFilterQuery) elements.libraryFilterQuery.value = "";
  if (elements.libYearFrom) elements.libYearFrom.value = "";
  if (elements.libYearTo) elements.libYearTo.value = "";
  if (elements.libSortCloud) {
    elements.libSortCloud.querySelectorAll(".filter-chip").forEach((c) => c.classList.remove("is-active"));
    const defaultChip = elements.libSortCloud.querySelector('[data-sort="recent"]');
    if (defaultChip) defaultChip.classList.add("is-active");
  }
  state.libSelectedGenres.clear();
  state.libSelectedLanguages.clear();
  state.selectedEntities.libKeywords = [];
  state.selectedEntities.libDirectors = [];
  state.selectedEntities.libActors = [];
  renderSelectedEntities("libKeywords");
  renderSelectedEntities("libDirectors");
  renderSelectedEntities("libActors");
  if (elements.libGenresCloud) {
    elements.libGenresCloud.querySelectorAll(".filter-chip").forEach((c) => c.classList.remove("is-active"));
  }
  if (elements.libLanguagesCloud) {
    elements.libLanguagesCloud.querySelectorAll(".filter-chip").forEach((c) => c.classList.remove("is-active"));
  }
  state.isSearchingLibrary = false;
  refreshCompactClouds();
  if (silent) return;
  reloadCurrentLibraryView();
}

let librarySearchDebounce = null;

function onLibraryFilterChange() {
  if (hasActiveLibraryFilters()) {
    searchPersonalLibrary();
  } else {
    if (state.isSearchingLibrary) {
      state.isSearchingLibrary = false;
      reloadCurrentLibraryView();
    } else {
      applyLibraryFilters();
    }
  }
}

async function searchPersonalLibrary() {
  const query = (elements.libraryFilterQuery?.value || "").trim();
  const hasFilters = hasActiveLibraryFilters();

  if (!query && !hasFilters) {
    if (state.isSearchingLibrary) {
      state.isSearchingLibrary = false;
      await reloadCurrentLibraryView();
    } else {
      applyLibraryFilters();
    }
    return;
  }

  const scope = state.librarySearchScope || "all";
  const requestNumber = ++state.requestNumber;
  state.isSearchingLibrary = true;
  elements.pagination.classList.add("is-hidden");
  const shelfTitle = VIEW_COPY[state.currentView]?.title || "Current shelf";
  setSectionCopy({
    kicker: "Personal library search",
    title: scope === "all" ? "Personal Library" : shelfTitle,
    description: scope === "all" ? "Results from every shelf." : `Results from ${shelfTitle}.`,
  });
  showLoadingCards();
  elements.count.textContent = `Searching ${scope === "all" ? "personal library" : "current shelf"}…`;

  try {
    let url = `/movies/library/search?query=${encodeURIComponent(query)}`;
    if (scope === "shelf" && state.currentView && state.currentView !== "library" && state.currentView !== "entries") {
      url += `&status=${encodeURIComponent(state.currentView)}`;
    }
    const results = await fetchJSON(url);
    if (requestNumber !== state.requestNumber) return;

    const list = Array.isArray(results) ? results : (results.results || []);
    state.unfilteredShelfMovies = list;
    applyLibraryFilters();

    const count = state.movies.length;
    const scopeLabel = scope === "all" ? "all shelves" : shelfTitle;
    const filterDetail = query ? ` matching "${query}"` : " matching filters";
    const countText = `${count} ${count === 1 ? "movie" : "movies"}${filterDetail} (${scopeLabel})`;
    elements.count.textContent = countText;
    if (elements.shelfCount) elements.shelfCount.textContent = countText;
  } catch (error) {
    if (requestNumber !== state.requestNumber) return;
    state.movies = [];
    state.unfilteredShelfMovies = [];
    renderMovies([]);
    showNotice(error.message);
  }
}

function setupLibraryFilters() {
  if (!elements.libGenresCloud || !elements.libLanguagesCloud) return;

  elements.libGenresCloud.replaceChildren();
  GENRE_OPTIONS.forEach(([id, name]) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "filter-chip";
    chip.dataset.genreId = String(id);
    chip.dataset.genreName = name;
    chip.textContent = name;
    chip.addEventListener("click", () => {
      if (state.libSelectedGenres.has(Number(id))) {
        state.libSelectedGenres.delete(Number(id));
        chip.classList.remove("is-active");
      } else {
        state.libSelectedGenres.add(Number(id));
        chip.classList.add("is-active");
      }
      onLibraryFilterChange();
    });
    elements.libGenresCloud.append(chip);
  });

  elements.libLanguagesCloud.replaceChildren();
  LANGUAGE_OPTIONS.forEach(([code, name]) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "filter-chip";
    chip.dataset.langCode = code;
    chip.textContent = name;
    chip.addEventListener("click", () => {
      if (state.libSelectedLanguages.has(code)) {
        state.libSelectedLanguages.delete(code);
        chip.classList.remove("is-active");
      } else {
        state.libSelectedLanguages.add(code);
        chip.classList.add("is-active");
      }
      onLibraryFilterChange();
    });
    elements.libLanguagesCloud.append(chip);
  });

  // Sort chips — radio behaviour (one active at a time)
  if (elements.libSortCloud) {
    elements.libSortCloud.querySelectorAll(".filter-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        elements.libSortCloud.querySelectorAll(".filter-chip").forEach((c) => c.classList.remove("is-active"));
        chip.classList.add("is-active");
        applyLibraryFilters(1);
      });
    });
  }

  if (elements.libraryFilterQuery) {
    elements.libraryFilterQuery.addEventListener("input", () => {
      clearTimeout(librarySearchDebounce);
      librarySearchDebounce = setTimeout(searchPersonalLibrary, 250);
    });
  }

  if (elements.scopeBtnAll && elements.scopeBtnShelf) {
    elements.scopeBtnAll.addEventListener("click", () => {
      if (state.librarySearchScope === "all") return;
      state.librarySearchScope = "all";
      elements.scopeBtnAll.classList.add("is-active");
      elements.scopeBtnShelf.classList.remove("is-active");
      if (hasActiveLibraryFilters()) {
        searchPersonalLibrary();
      }
    });

    elements.scopeBtnShelf.addEventListener("click", () => {
      if (state.librarySearchScope === "shelf") return;
      state.librarySearchScope = "shelf";
      elements.scopeBtnShelf.classList.add("is-active");
      elements.scopeBtnAll.classList.remove("is-active");
      if (hasActiveLibraryFilters()) {
        searchPersonalLibrary();
      }
    });
  }

  if (elements.libYearFrom) {
    elements.libYearFrom.addEventListener("input", () => {
      clearTimeout(librarySearchDebounce);
      librarySearchDebounce = setTimeout(onLibraryFilterChange, 250);
    });
  }
  if (elements.libYearTo) {
    elements.libYearTo.addEventListener("input", () => {
      clearTimeout(librarySearchDebounce);
      librarySearchDebounce = setTimeout(onLibraryFilterChange, 250);
    });
  }
  if (elements.resetLibraryFilters) {
    elements.resetLibraryFilters.addEventListener("click", () => resetLibraryFilters());
  }
  refreshCompactClouds();
}

async function loadShelf(view, page = 1) {
  hideFilmographyToolbar();
  if (view === "entries") {
    await loadEntries(page);
    return;
  }
  if (view === "discover") {
    await activateDiscoverView();
    return;
  }
  if (view === "movie-notes") {
    await loadMovieNotes(page);
    return;
  }
  if (!(view in VIEW_COPY)) {
    return;
  }

  setSearchOriginMovie();
  setEntriesVisible(false);
  if (elements.discoverWorkspace) {
    elements.discoverWorkspace.classList.add("is-hidden");
  }
  if (elements.notesSearchContainer) {
    elements.notesSearchContainer.classList.add("is-hidden");
  }
  const requestNumber = ++state.requestNumber;
  state.mode = "shelf";
  state.currentView = view;
  setActiveView(view);
  setModeButton(null);
  elements.simpleControls.classList.add("is-hidden");
  elements.advancedControls.classList.add("is-hidden");
  elements.pagination.classList.add("is-hidden");
  setSectionCopy(VIEW_COPY[view]);
  clearNotice();

  if (hasActiveLibraryFilters()) {
    await searchPersonalLibrary();
    return;
  }

  showLoadingCards();
  elements.count.textContent = "Loading…";

  try {
    // Backend collection query (legacy endpoints: /movies/status/, /movies/notes?page=)
    const results = await fetchJSON(`/movies/library/search?status=${encodeURIComponent(view)}`);
    if (requestNumber !== state.requestNumber) {
      return;
    }

    const allFetched = Array.isArray(results) ? results : (results.results || []);
    state.unfilteredShelfMovies = allFetched;
    state.totalResults = allFetched.length;
    applyLibraryFilters(page);
  } catch (error) {
    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = [];
    state.unfilteredShelfMovies = [];
    renderMovies([]);
    showNotice(error.message);
  }
}

async function loadMovieNotes(page = 1) {
  const requestNumber = ++state.requestNumber;
  setSearchOriginMovie();
  setEntriesVisible(false);
  if (elements.discoverWorkspace) {
    elements.discoverWorkspace.classList.add("is-hidden");
  }
  if (elements.notesSearchContainer) {
    elements.notesSearchContainer.classList.remove("is-hidden");
  }
  hideFilmographyToolbar();
  state.mode = "shelf";
  state.currentView = "movie-notes";
  setActiveView("movie-notes");
  setModeButton(null);
  elements.simpleControls.classList.add("is-hidden");
  elements.advancedControls.classList.add("is-hidden");
  elements.pagination.classList.add("is-hidden");
  setSectionCopy(VIEW_COPY["movie-notes"]);
  clearNotice();

  if (hasActiveLibraryFilters()) {
    await searchPersonalLibrary();
    return;
  }

  showLoadingCards();
  elements.count.textContent = "Loading…";

  try {
    const results = await fetchJSON("/movies/library/search?status=movie-notes");
    if (requestNumber !== state.requestNumber) return;

    const allFetched = Array.isArray(results) ? results : (results.results || []);
    state.unfilteredShelfMovies = allFetched;
    state.totalResults = allFetched.length;
    applyLibraryFilters(page);
  } catch (error) {
    if (requestNumber !== state.requestNumber) return;

    state.movies = [];
    state.unfilteredShelfMovies = [];
    renderMovies([]);
    showNotice(error.message);
  }
}

let notesSearchTimeout = null;

async function searchLocalNotes(query) {
  const cleaned = query.trim();
  if (!cleaned) {
    if (elements.clearNotesSearch) elements.clearNotesSearch.classList.add("is-hidden");
    await loadMovieNotes(1);
    return;
  }

  if (elements.clearNotesSearch) elements.clearNotesSearch.classList.remove("is-hidden");
  const requestNumber = ++state.requestNumber;
  state.mode = "movie-notes-search";
  elements.pagination.classList.add("is-hidden");
  showLoadingCards();
  elements.count.textContent = "Searching notes…";

  try {
    const response = await fetchJSON(`/movies/notes/search?query=${encodeURIComponent(cleaned)}`);
    if (requestNumber !== state.requestNumber) return;
    const results = Array.isArray(response) ? response : (response.results || []);
    state.movies = results;
    state.totalResults = results.length;
    renderMovies(results, "library", results.length);
    elements.count.textContent = `${results.length} ${results.length === 1 ? "movie" : "movies"} matching "${cleaned}"`;
  } catch (error) {
    if (requestNumber !== state.requestNumber) return;
    state.movies = [];
    renderMovies([]);
    showNotice(error.message);
  }
}


async function searchMovies(query, page = 1) {
  const cleanedQuery = query.trim();

  if (!cleanedQuery) {
    elements.query.focus();
    return;
  }

  const requestNumber = ++state.requestNumber;
  hideFilmographyToolbar();
  setSearchOriginMovie();
  setEntriesVisible(false);
  if (elements.discoverWorkspace) {
    elements.discoverWorkspace.classList.add("is-hidden");
  }
  if (elements.notesSearchContainer) {
    elements.notesSearchContainer.classList.add("is-hidden");
  }
  state.mode = "search";
  state.currentView = null;
  setActiveView(null);
  setModeButton(null);
  elements.simpleControls.classList.add("is-hidden");
  elements.advancedControls.classList.add("is-hidden");
  elements.pagination.classList.add("is-hidden");
  setSectionCopy({
    kicker: "TMDB title search",
    title: `Results for “${cleanedQuery}”`,
    description: "Open a movie to view details and organise it.",
  });
  clearNotice();
  showLoadingCards();
  elements.count.textContent = "Searching…";
  document.querySelector(".library").scrollIntoView({
    behavior: "smooth",
    block: "start",
  });

  try {
    const response = await fetchJSON(
      `/movies/search?query=${encodeURIComponent(cleanedQuery)}&page=${page}`,
    );

    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = Array.isArray(response.results) ? response.results : [];
    state.searchPage = Number(response.page || page);
    state.searchTotalPages = Number(response.total_pages || 1);
    state.totalResults = Number(response.total_results || 0);
    state.pageLoader = (target) => searchMovies(cleanedQuery, target);
    renderMovies(state.movies, "search", state.totalResults);
    renderPagination(
      elements.pagination,
      state.searchPage,
      state.searchTotalPages,
      async (target) => { await searchMovies(cleanedQuery, target); scrollToResults(); },
    );
  } catch (error) {
    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = [];
    renderMovies([], "search");
    showNotice(error.message);
  }
}

const DISCOVERY_COPY = {
  simple: {
    kicker: "Open discovery",
    title: "Simple discoveries",
    description: "Popular TMDB movies without personal-library filtering.",
  },
  advanced: {
    kicker: "TMDB filters",
    title: "Advanced search results",
    description: "Shape the search with genres, origin, rating and people.",
  },
  super: {
    kicker: "Discover",
    title: "Movie discovery",
    description: "Explore movies from TMDB with your personal preferences and library rules.",
  },
};

function setModeButton(mode) {
  elements.modeButtons.forEach((button) => {
    button.classList.toggle(
      "is-active",
      button.dataset.discoveryMode === mode,
    );
  });
}

async function setDiscoveryMode(mode, runSearch = false) {
  if (!(mode in DISCOVERY_COPY)) {
    mode = "super";
  }

  state.discoveryMode = mode;
  setEntriesVisible(false);
  if (elements.discoverWorkspace) {
    elements.discoverWorkspace.classList.remove("is-hidden");
  }
  if (elements.notesSearchContainer) {
    elements.notesSearchContainer.classList.add("is-hidden");
  }
  state.mode = "discovery";
  state.currentView = "discover";
  setActiveView("discover");
  setModeButton(mode);
  setSectionCopy(DISCOVERY_COPY[mode]);
  elements.simpleControls.classList.add("is-hidden");
  elements.advancedControls.classList.remove("is-hidden");
  elements.personalFilters.classList.remove("is-hidden");
  elements.pagination.classList.add("is-hidden");
  updateFilterPillBadges();
  renderActiveFilterTags();
  updateFilterPillStates();
  scheduleSearchStateSave();

  if (runSearch || mode === "simple") {
    await runDiscoverySearch();
  }
}

function buildSearchSpec() {
  return {
    mode: "super",
    filters: collectAdvancedFilters(),
    personalFilters: collectPersonalFilters(),
  };
}

const discoveryCache = new Map();

function clearDiscoveryCache() {
  discoveryCache.clear();
}

function getDiscoveryCacheKey(spec, page) {
  return JSON.stringify({ spec, page });
}

async function prefetchDiscoveryPage(spec, page) {
  const nextKey = getDiscoveryCacheKey(spec, page);
  if (discoveryCache.has(nextKey)) return;

  const url = spec.mode === "advanced"
    ? "/movies/discover/advanced"
    : "/movies/discover/super-advanced";
  const body = {
    filters: spec.filters || {},
    ...spec.personalFilters,
  };

  const basePage = (page - 1) * 3;
  const fetchOne = (p) => fetchJSON(url, {
    method: "POST",
    body: JSON.stringify({ ...body, page: p }),
  });

  try {
    const [p1, p2, p3] = await Promise.all([
      fetchOne(basePage + 1),
      fetchOne(basePage + 2).catch(() => ({ results: [] })),
      fetchOne(basePage + 3).catch(() => ({ results: [] })),
    ]);

    const rawCombined = [
      ...(Array.isArray(p1.results) ? p1.results : []),
      ...(Array.isArray(p2.results) ? p2.results : []),
      ...(Array.isArray(p3.results) ? p3.results : []),
    ];
    // Always round down to complete rows of 6 so the last row is never mostly empty!
    let limit = 24;
    if (rawCombined.length < 24 && rawCombined.length >= 18) {
      limit = 18;
    } else if (rawCombined.length < 18 && rawCombined.length >= 12) {
      limit = 12;
    } else if (rawCombined.length >= 24) {
      limit = 24;
    } else {
      limit = rawCombined.length;
    }
    const combined = rawCombined.slice(0, limit);

    const response = {
      results: combined,
      page: page,
      tmdb_total_pages: Math.max(1, Math.ceil(Number(p1.tmdb_total_pages || 1) / 3)),
      tmdb_total_results: Number(p1.tmdb_total_results || rawCombined.length),
      has_next_page: Boolean(p3.has_next_page || (basePage + 3 < Number(p1.tmdb_total_pages || 1))),
      pagination_exact: p1.pagination_exact !== false,
    };

    discoveryCache.set(nextKey, response);
  } catch {
    // Background prefetch errors are safely ignored
  }
}

async function executeDiscoverySearch(spec, page = 1, { forceRefresh = false } = {}) {
  hideFilmographyToolbar();
  const requestNumber = ++state.requestNumber;
  state.mode = "discovery";
  state.currentView = "discover";
  setActiveView("discover");
  setModeButton("super");

  const hasActiveFilters = Boolean(
    (spec.filters?.include_genre_ids && spec.filters.include_genre_ids.length) ||
    (spec.filters?.exclude_genre_ids && spec.filters.exclude_genre_ids.length) ||
    spec.filters?.minimum_rating ||
    spec.filters?.release_year_from ||
    spec.filters?.release_year_to ||
    (spec.filters?.include_director_ids && spec.filters.include_director_ids.length) ||
    (spec.filters?.include_cast_ids && spec.filters.include_cast_ids.length) ||
    (spec.filters?.include_keyword_ids && spec.filters.include_keyword_ids.length)
  );

  setSectionCopy({
    kicker: "Discover",
    title: hasActiveFilters ? "Filtered discovery" : "Movie discovery",
    description: hasActiveFilters
      ? "Movies matching your chosen filters and library settings."
      : "Popular TMDB discoveries with your personal library rules applied.",
  });
  clearNotice();

  const cacheKey = getDiscoveryCacheKey(spec, page);

  const url = spec.mode === "advanced"
    ? "/movies/discover/advanced"
    : "/movies/discover/super-advanced";
  const body = {
    filters: spec.filters || {},
    force_refresh: Boolean(forceRefresh),
    ...spec.personalFilters,
  };

  const applyResponse = (response) => {
    state.movies = Array.isArray(response.results) ? response.results : [];

    state.currentSearchSpec = JSON.parse(JSON.stringify(spec));
    state.searchPage = Number(response.page || page);
    state.searchTotalPages = Number(response.tmdb_total_pages || 0);
    state.paginationExact = response.pagination_exact !== false;
    state.totalResults = state.paginationExact
      ? Number(response.tmdb_total_results || state.movies.length)
      : state.movies.length;
    state.pageLoader = (target) => executeDiscoverySearch(spec, target);
    renderMovies(state.movies, "search", state.totalResults);
    if (!state.paginationExact) {
      elements.count.textContent = `${state.movies.length} ${
        state.movies.length === 1 ? "movie" : "movies"
      } on this page`;
    }
    renderPagination(
      elements.pagination,
      state.searchPage,
      state.searchTotalPages,
      async (target) => { await executeDiscoverySearch(spec, target); scrollToResults(); },
      {
        exact: state.paginationExact,
        hasNext: Boolean(response.has_next_page),
      },
    );
    scheduleSearchStateSave();

    // Prefetch the next 60 movies in the background
    if (response.has_next_page || (state.searchPage < state.searchTotalPages)) {
      prefetchDiscoveryPage(spec, state.searchPage + 1);
    }
  };

  if (!forceRefresh && discoveryCache.has(cacheKey)) {
    applyResponse(discoveryCache.get(cacheKey));
    return;
  }

  elements.pagination.classList.add("is-hidden");
  showLoadingCards();
  elements.count.textContent = forceRefresh ? "Refreshing from TMDB…" : "Searching…";

  const basePage = (page - 1) * 3;
  const fetchOne = (p) => fetchJSON(url, {
    method: "POST",
    body: JSON.stringify({ ...body, page: p }),
  });

  try {
    const [p1, p2, p3] = await Promise.all([
      fetchOne(basePage + 1),
      fetchOne(basePage + 2).catch(() => ({ results: [] })),
      fetchOne(basePage + 3).catch(() => ({ results: [] })),
    ]);

    if (requestNumber !== state.requestNumber) {
      return;
    }

    const rawCombined = [
      ...(Array.isArray(p1.results) ? p1.results : []),
      ...(Array.isArray(p2.results) ? p2.results : []),
      ...(Array.isArray(p3.results) ? p3.results : []),
    ];

    // Always fill complete rows of 6 (24 for 4 full rows, or 18 for 3 full rows)
    let limit = 24;
    if (rawCombined.length < 24 && rawCombined.length >= 18) {
      limit = 18;
    } else if (rawCombined.length < 18 && rawCombined.length >= 12) {
      limit = 12;
    } else if (rawCombined.length >= 24) {
      limit = 24;
    } else {
      limit = rawCombined.length;
    }
    const combined = rawCombined.slice(0, limit);

    const response = {
      results: combined,
      page: page,
      tmdb_total_pages: Math.max(1, Math.ceil(Number(p1.tmdb_total_pages || 1) / 3)),
      tmdb_total_results: Number(p1.tmdb_total_results || rawCombined.length),
      has_next_page: Boolean(p3.has_next_page || (basePage + 3 < Number(p1.tmdb_total_pages || 1))),
      pagination_exact: p1.pagination_exact !== false,
    };

    discoveryCache.set(cacheKey, response);
    applyResponse(response);
    if (forceRefresh) {
      showNotice("Refreshed live results from TMDB.");
    }
  } catch (error) {
    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = [];
    renderMovies([], "search");
    showNotice(error.message);
  }
}

async function runDiscoverySearch({ forceRefresh = false } = {}) {
  await executeDiscoverySearch(buildSearchSpec(), 1, { forceRefresh });
}

function syncRibbonActiveState() {
  const activeId = elements.profileSelect?.value ? String(elements.profileSelect.value) : null;
  const ribbon = document.querySelector("#profile-ribbon");
  if (!ribbon) return;
  ribbon.querySelectorAll(".ribbon-chip").forEach((chip) => {
    chip.classList.toggle("is-active", Boolean(activeId && chip.dataset.profile === activeId));
  });
}

function updateProfileButtons() {
  const preferenceId = Number(elements.profileSelect.value);
  const preference = state.preferences.find(
    (item) => item.preference_id === preferenceId,
  );
  const hasPreference = Boolean(preference);
  elements.updateProfile.disabled = !hasPreference;
  elements.deleteProfile.disabled = !hasPreference;
  if (elements.quickUpdateProfile) {
    elements.quickUpdateProfile.classList.toggle("is-hidden", !hasPreference);
    if (hasPreference) {
      elements.quickUpdateProfile.title = `Update "${preference.name}" with current filters`;
    }
  }
  syncRibbonActiveState();
}

const DEFAULT_RIBBON_PROFILES = [];

function getRibbonProfiles() {
  const customIds = (state.preferences || []).map((p) => Number(p.preference_id));
  const saved = localStorage.getItem("nope_ribbon_profile_keys");
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      if (Array.isArray(parsed)) {
        const cleaned = parsed
          .map((k) => {
            if (typeof k === "string" && k.startsWith("custom_")) {
              return Number(k.replace("custom_", ""));
            }
            return Number(k);
          })
          .filter((k) => !isNaN(k) && customIds.includes(k));
        if (cleaned.length > 0) {
          state.ribbonProfileKeys = cleaned.slice(0, 6);
          return state.ribbonProfileKeys;
        }
      }
    } catch {}
  }
  state.ribbonProfileKeys = customIds.slice(0, 6);
  return state.ribbonProfileKeys;
}

function saveRibbonProfiles(keys) {
  const cleaned = keys
    .map((k) => {
      if (typeof k === "string" && k.startsWith("custom_")) {
        return Number(k.replace("custom_", ""));
      }
      return Number(k);
    })
    .filter((k) => !isNaN(k));
  state.ribbonProfileKeys = cleaned.slice(0, 6);
  localStorage.setItem("nope_ribbon_profile_keys", JSON.stringify(state.ribbonProfileKeys));
  renderProfileRibbon();
  renderProfileWorkshop();
}

function getAllProfilesList() {
  return (state.preferences || []).map((p) => ({
    id: p.preference_id,
    name: p.name,
    isPreset: false,
    preference: p,
  }));
}

function renderProfileRibbon() {
  const ribbon = document.querySelector("#profile-ribbon");
  if (!ribbon) return;

  const ribbonKeys = getRibbonProfiles();
  const allProfiles = getAllProfilesList();
  const activeProfiles = ribbonKeys
    .map((k) => allProfiles.find((p) => Number(p.id) === Number(k)))
    .filter(Boolean);

  ribbon.replaceChildren();
  activeProfiles.forEach((prof) => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "ribbon-chip";
    chip.dataset.profile = String(prof.id);
    chip.textContent = prof.name;
    chip.addEventListener("click", () => {
      elements.profileSelect.value = String(prof.id);
      applySelectedProfile();
      clearDiscoveryCache();
      runDiscoverySearch();
    });
    ribbon.append(chip);
  });
  syncRibbonActiveState();
}

function renderProfileWorkshop() {
  const ribbonCloud = document.querySelector("#ribbon-profiles-cloud");
  const reserveCloud = document.querySelector("#reserve-profiles-cloud");
  const countEl = document.querySelector("#ribbon-slots-count");
  if (!ribbonCloud || !reserveCloud) return;

  const ribbonKeys = new Set(getRibbonProfiles().map(Number));
  const allProfiles = getAllProfilesList();

  const ribbonList = [];
  const reserveList = [];

  allProfiles.forEach((p) => {
    if (ribbonKeys.has(Number(p.id))) {
      ribbonList.push(p);
    } else {
      reserveList.push(p);
    }
  });

  if (countEl) {
    countEl.textContent = `${ribbonList.length}/6`;
  }

  // Active Ribbon chips
  ribbonCloud.replaceChildren();
  ribbonList.forEach((prof) => {
    const chip = document.createElement("div");
    chip.className = "profile-workshop-chip is-pinned";

    const pinBtn = document.createElement("button");
    pinBtn.type = "button";
    pinBtn.className = "chip-pin-btn";
    pinBtn.textContent = "★";
    pinBtn.title = "Demote to Reserve";
    pinBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const updated = getRibbonProfiles().filter((k) => Number(k) !== Number(prof.id));
      saveRibbonProfiles(updated);
    });

    const nameSpan = document.createElement("span");
    nameSpan.className = "chip-name";
    nameSpan.textContent = prof.name;
    nameSpan.addEventListener("click", () => {
      elements.profileSelect.value = String(prof.id);
      applySelectedProfile();
      clearDiscoveryCache();
      runDiscoverySearch();
    });

    const delBtn = document.createElement("button");
    delBtn.type = "button";
    delBtn.className = "chip-del-btn";
    delBtn.textContent = "✕";
    delBtn.title = "Delete profile";
    delBtn.addEventListener("click", async (e) => {
      e.stopPropagation();
      elements.profileSelect.value = String(prof.id);
      await deleteSelectedProfile();
      const updated = getRibbonProfiles().filter((k) => Number(k) !== Number(prof.id));
      saveRibbonProfiles(updated);
    });

    chip.append(pinBtn, nameSpan, delBtn);
    ribbonCloud.append(chip);
  });

  // Reserve chips
  reserveCloud.replaceChildren();
  reserveList.forEach((prof) => {
    const chip = document.createElement("div");
    chip.className = "profile-workshop-chip";

    const pinBtn = document.createElement("button");
    pinBtn.type = "button";
    pinBtn.className = "chip-pin-btn";
    pinBtn.textContent = "☆";
    pinBtn.title = "Promote to Ribbon";
    pinBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const current = getRibbonProfiles();
      if (current.length >= 6) {
        showNotice("Ribbon is full (max 6). Unpin (★) a profile first.");
        return;
      }
      saveRibbonProfiles([...current, Number(prof.id)]);
    });

    const nameSpan = document.createElement("span");
    nameSpan.className = "chip-name";
    nameSpan.textContent = prof.name;
    nameSpan.addEventListener("click", () => {
      elements.profileSelect.value = String(prof.id);
      applySelectedProfile();
      clearDiscoveryCache();
      runDiscoverySearch();
    });

    const delBtn = document.createElement("button");
    delBtn.type = "button";
    delBtn.className = "chip-del-btn";
    delBtn.textContent = "✕";
    delBtn.title = "Delete profile";
    delBtn.addEventListener("click", async (e) => {
      e.stopPropagation();
      elements.profileSelect.value = String(prof.id);
      await deleteSelectedProfile();
      const updated = getRibbonProfiles().filter((k) => Number(k) !== Number(prof.id));
      saveRibbonProfiles(updated);
    });

    chip.append(pinBtn, nameSpan, delBtn);
    reserveCloud.append(chip);
  });
}

async function loadProfiles(selectedId = null) {
  try {
    state.preferences = await fetchJSON("/search-preferences");
    elements.profileSelect.replaceChildren();
    const emptyOption = document.createElement("option");
    emptyOption.value = "";
    emptyOption.textContent = "Unsaved search";
    elements.profileSelect.append(emptyOption);

    state.preferences.forEach((preference) => {
      const option = document.createElement("option");
      option.value = String(preference.preference_id);
      option.textContent = preference.name;
      elements.profileSelect.append(option);
    });

    if (selectedId !== null) {
      elements.profileSelect.value = String(selectedId);
    }
    updateProfileButtons();
    renderProfileRibbon();
    renderProfileWorkshop();
  } catch (error) {
    showNotice(`Could not load search profiles: ${error.message}`);
  }
}

async function applySelectedProfile() {
  const preferenceId = Number(elements.profileSelect.value);
  const preference = state.preferences.find(
    (item) => item.preference_id === preferenceId,
  );

  updateProfileButtons();

  if (!preference) {
    scheduleSearchStateSave();
    return;
  }

  await setAdvancedFilters(preference.filters || {});
  setPersonalFilters(preference.personal_filters || {});
  scheduleSearchStateSave();
}

function resetAdvancedFilters({ notify = true } = {}) {
  elements.advancedForm.reset();
  elements.profileSelect.value = "";
  state.profilePassthroughFilters = {};
  Object.keys(state.selectedEntities).forEach((key) => {
    state.selectedEntities[key] = [];
    renderSelectedEntities(key);
  });
  Object.keys(PICKER_CONFIG).forEach((id) => setPickerValues(id, []));
  setPersonalFilters();

  const defaultPref = state.preferences?.find((item) => item.is_default);
  const baseFilters = defaultPref?.filters || DEFAULT_SYSTEM_FILTERS;
  setAdvancedFilters(baseFilters);

  updateProfileButtons();
  if (notify) {
    showNotice("Reset to default filters.");
  }
  scheduleSearchStateSave();
}

function openProfileDialog(mode) {
  const preferenceId = Number(elements.profileSelect.value);
  const preference = state.preferences.find(
    (item) => item.preference_id === preferenceId,
  );

  if (mode === "edit" && !preference) {
    return;
  }

  state.profileDialogMode = mode;
  elements.profileNameForm.reset();
  elements.profileName.value = mode === "edit" ? preference.name : "";
  elements.profileDialogTitle.textContent = mode === "edit"
    ? "Update search profile"
    : "Save search profile";
  elements.profileDialogCopy.textContent = mode === "edit"
    ? "Rename this profile and replace its saved parameters with the filters currently on screen."
    : "Save the current filters so you can use them again.";
  elements.profileSubmit.textContent = mode === "edit"
    ? "Update profile"
    : "Save profile";
  elements.profileDialog.showModal();
  elements.profileName.focus();
  elements.profileName.select();
}

async function saveNewProfile(name) {
  const response = await fetchJSON("/search-preferences", {
    method: "POST",
    body: JSON.stringify({
      name,
      filters: collectAdvancedFilters(),
      personal_filters: collectPersonalFilters(),
      is_default: false,
    }),
  });
  await loadProfiles(response.preference.preference_id);
  elements.profileDialog.close();
  showNotice(`Saved “${response.preference.name}”.`);
}

async function updateSelectedProfile(name) {
  const preferenceId = Number(elements.profileSelect.value);
  const preference = state.preferences.find(
    (item) => item.preference_id === preferenceId,
  );

  if (!preference) {
    return;
  }

  const response = await fetchJSON(`/search-preferences/${preferenceId}`, {
    method: "PUT",
    body: JSON.stringify({
      name,
      filters: collectAdvancedFilters(),
      personal_filters: collectPersonalFilters(),
    }),
  });
  await loadProfiles(response.preference.preference_id);
  elements.profileDialog.close();
  showNotice(`Updated “${response.preference.name}”.`);
}

async function deleteSelectedProfile() {
  const preferenceId = Number(elements.profileSelect.value);
  const preference = state.preferences.find(
    (item) => item.preference_id === preferenceId,
  );

  if (!preference || !window.confirm(
    `Delete “${preference.name}”? This will not delete any movies.`,
  )) {
    return;
  }

  await fetchJSON(`/search-preferences/${preferenceId}`, {
    method: "DELETE",
  });
  resetAdvancedFilters();
  await loadProfiles();
  showNotice(`Deleted “${preference.name}”.`);
}

function markSelectedProfileModified() {
  const preferenceId = Number(elements.profileSelect.value);
  const option = elements.profileSelect.selectedOptions[0];
  const preference = state.preferences.find(
    (item) => item.preference_id === preferenceId,
  );
  if (option && preference && !option.textContent.endsWith(" • Modified")) {
    option.textContent = `${preference.name} • Modified`;
  }
  scheduleSearchStateSave();
}

function appendMetaItem(text) {
  if (!text) {
    return;
  }

  const item = document.createElement("span");
  item.textContent = text;
  elements.dialogMeta.append(item);
}

function renderTags(container, tags, customAware = false) {
  container.replaceChildren();

  if (!Array.isArray(tags) || tags.length === 0) {
    const empty = document.createElement("span");
    empty.className = "tag-empty";
    empty.textContent = "None saved";
    container.append(empty);
    return;
  }

  tags.forEach((tag) => {
    const element = document.createElement("span");
    element.className = "tag";

    if (customAware && tag.is_custom) {
      element.classList.add("is-custom");
      element.title = "Personal tag";
    }

    element.textContent = tag.name;
    container.append(element);
  });
}

function renderMovieKeywords(tags) {
  elements.dialogKeywords.replaceChildren();
  if (!Array.isArray(tags) || tags.length === 0) {
    const empty = document.createElement("span");
    empty.className = "tag-empty";
    empty.textContent = "No keywords saved";
    elements.dialogKeywords.append(empty);
    return;
  }

  // Deduplicate keywords by name, prioritizing custom keywords
  const seenNames = new Set();
  const sortedTags = [...tags].sort((a, b) => (b.is_custom ? 1 : 0) - (a.is_custom ? 1 : 0));
  const uniqueTags = [];
  for (const tag of sortedTags) {
    const norm = (tag.name || "").trim().toLowerCase();
    if (norm && !seenNames.has(norm)) {
      seenNames.add(norm);
      uniqueTags.push(tag);
    }
  }

  uniqueTags.forEach((tag) => {
    const chip = document.createElement("span");
    chip.className = `tag keyword-chip${tag.is_custom ? " is-custom" : ""}`;
    if (tag.is_custom) {
      const search = document.createElement("button");
      search.type = "button";
      search.textContent = tag.name;
      search.title = `Find local movies tagged “${tag.name}”`;
      search.addEventListener("click", () => {
        setSearchOriginMovie({
          id: state.selectedMovie.tmdb_id,
          title: state.selectedMovie.title || state.selectedMovie.original_title,
        });
        closeMovieDetails();
        searchKeywordMovies(tag.name, 1).catch((error) => showNotice(error.message));
      });
      chip.append(search);
      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "keyword-remove";
      remove.textContent = "×";
      remove.setAttribute("aria-label", `Remove ${tag.name} from this movie`);
      remove.addEventListener("click", () => removeSelectedKeyword(tag));
      chip.append(remove);
    } else {
      chip.textContent = tag.name;
    }
    elements.dialogKeywords.append(chip);
  });
}

function renderPeople(container, people, entityKey) {
  container.replaceChildren();
  const available = (people || []).filter(
    (person) => Number(person.tmdb_person_id || person.id) > 0 && person.name,
  );

  if (!available.length) {
    container.textContent = "Not available";
    return;
  }

  available.forEach((person, index) => {
    if (index > 0) {
      container.append(document.createTextNode(", "));
    }
    const button = document.createElement("button");
    button.type = "button";
    button.className = "credit-link";
    button.textContent = person.name;
    button.title = `Explore movies featuring ${person.name}`;
    button.addEventListener("click", () => {
      explorePerson(person, entityKey).catch((error) => showNotice(error.message));
    });
    container.append(button);
  });
}

function saveCurrentSearchSnapshot(originInfo = null) {
  let title = "Discover";
  if (state.currentView === "discover" || (!state.currentView && state.mode === "discovery")) {
    title = "Discover";
  } else if (state.currentView === "movie-notes") {
    title = "Movie Notes";
  } else if (state.currentView === "entries") {
    title = "Notes";
  } else if (state.currentView && STATUS_LABELS[state.currentView]) {
    title = STATUS_LABELS[state.currentView];
  } else if (elements.libraryTitle && !elements.sectionHeadingBlock?.classList.contains("is-hidden")) {
    title = elements.libraryTitle.textContent || "Library";
  } else {
    title = "Discover";
  }

  state.savedSearchSnapshot = {
    mode: state.mode,
    currentView: state.currentView,
    discoveryMode: state.discoveryMode,
    filters: collectAdvancedFilters(),
    personalFilters: collectPersonalFilters(),
    selectedEntities: JSON.parse(JSON.stringify(state.selectedEntities)),
    profileSelectValue: elements.profileSelect?.value || "",
    activeRibbonProfile: document.querySelector(".ribbon-chip.is-active")?.dataset.profile || null,
    movies: [...(state.movies || [])],
    searchPage: state.searchPage,
    searchTotalPages: state.searchTotalPages,
    totalResults: state.totalResults,
    originMovie: originInfo || state.searchOriginMovie || null,
    title: title,
    scrollPosition: window.scrollY || document.documentElement.scrollTop,
  };
}

async function restoreSearchSnapshot() {
  if (!state.savedSearchSnapshot) return;
  const snap = state.savedSearchSnapshot;
  state.savedSearchSnapshot = null;

  hideFilmographyToolbar();

  state.mode = snap.mode;
  state.currentView = snap.currentView;
  state.discoveryMode = snap.discoveryMode;
  state.selectedEntities = snap.selectedEntities;
  Object.keys(state.selectedEntities).forEach((key) => renderSelectedEntities(key));

  await setAdvancedFilters(snap.filters);
  setPersonalFilters(snap.personalFilters);

  if (snap.profileSelectValue) {
    elements.profileSelect.value = snap.profileSelectValue;
  }
  updateProfileButtons();

  if (snap.activeRibbonProfile) {
    document.querySelectorAll(".ribbon-chip").forEach((chip) => {
      chip.classList.toggle("is-active", chip.dataset.profile === snap.activeRibbonProfile);
    });
  }

  setActiveView(snap.currentView);
  const discoverHeader = document.querySelector("#discover-canvas-header");
  if (snap.currentView === "discover" || (!snap.currentView && snap.mode === "discovery")) {
    if (elements.discoverWorkspace) elements.discoverWorkspace.classList.remove("is-hidden");
    if (discoverHeader) discoverHeader.classList.remove("is-hidden");
    elements.sectionHeadingBlock?.classList.add("is-hidden");
  } else if (snap.currentView) {
    if (elements.discoverWorkspace) elements.discoverWorkspace.classList.add("is-hidden");
    if (discoverHeader) discoverHeader.classList.add("is-hidden");
    elements.sectionHeadingBlock?.classList.remove("is-hidden");
    if (elements.libraryTitle) elements.libraryTitle.textContent = snap.title;
  }

  state.movies = snap.movies;
  state.searchPage = snap.searchPage;
  state.searchTotalPages = snap.searchTotalPages;
  state.totalResults = snap.totalResults;

  renderMovies(state.movies, snap.currentView === "discover" ? "search" : "library", state.totalResults);
  if (snap.searchTotalPages > 1) {
    elements.pagination?.classList.remove("is-hidden");
  } else {
    elements.pagination?.classList.add("is-hidden");
  }

  window.scrollTo({ top: snap.scrollPosition || 0, behavior: "smooth" });
}

function hideFilmographyToolbar() {
  if (elements.filmographyToolbar) {
    elements.filmographyToolbar.classList.add("is-hidden");
  }
  if (elements.returnToOrigin) {
    elements.returnToOrigin.classList.add("is-hidden");
  }
  state.activeFilmographyPerson = null;
  state.activeFilmographyData = null;
}

async function loadPersonFilmography(person, entityKey = "directors", department = null) {
  const personId = Number(person.tmdb_person_id || person.id);
  if (!personId) return;

  const originInfo = state.selectedMovie ? {
    id: state.selectedMovie.tmdb_id,
    title: state.selectedMovie.title || state.selectedMovie.original_title,
    fromMovieDetails: true,
  } : null;

  if (state.mode !== "filmography") {
    saveCurrentSearchSnapshot(originInfo);
  }

  closeMovieDetails();

  state.mode = "filmography";

  // Sidebar must remain visible! Match the origin view pane:
  const originView = state.savedSearchSnapshot?.currentView || state.currentView || "discover";
  const isOriginDiscover = originView === "discover" || (!originView && state.savedSearchSnapshot?.mode === "discovery");
  const isOriginLibrary = ["favorites", "watched", "watch_later", "rewatch", "excluded", "new_discovery", "movie-notes"].includes(originView);
  const isOriginNotes = originView === "entries";

  if (elements.sidebarPaneDiscover) {
    elements.sidebarPaneDiscover.classList.toggle("is-hidden", !isOriginDiscover);
  }
  if (elements.discoverWorkspace) {
    elements.discoverWorkspace.classList.toggle("is-hidden", !isOriginDiscover);
  }
  if (elements.sidebarPaneLibrary) {
    elements.sidebarPaneLibrary.classList.toggle("is-hidden", !isOriginLibrary);
  }
  if (elements.sidebarPaneNotes) {
    elements.sidebarPaneNotes.classList.toggle("is-hidden", !isOriginNotes);
  }

  // Hide canvas headers so the filmography toolbar sits cleanly at the top of the canvas
  const discoverHeader = document.querySelector("#discover-canvas-header");
  if (discoverHeader) discoverHeader.classList.add("is-hidden");
  if (elements.notesSearchContainer) elements.notesSearchContainer.classList.add("is-hidden");
  const headingBlock = document.querySelector("#section-heading-block");
  if (headingBlock) headingBlock.classList.add("is-hidden");

  const previousTitle = state.savedSearchSnapshot?.title || "Discover";
  if (elements.returnToOrigin) {
    elements.returnToOrigin.textContent = `← Return to ${previousTitle}`;
    elements.returnToOrigin.classList.remove("is-hidden");
    elements.returnToOrigin.onclick = () => {
      restoreSearchSnapshot();
    };
  }

  showLoadingCards();
  elements.pagination?.classList.add("is-hidden");

  const deptParam = department ? `?department=${encodeURIComponent(department)}` : "?department=all";
  try {
    const data = await fetchJSON(`/people/${personId}/filmography${deptParam}`);
    state.activeFilmographyPerson = data.person;
    state.activeFilmographyData = data;

    if (elements.filmographyToolbar) {
      elements.filmographyToolbar.classList.remove("is-hidden");
      if (elements.filmographyName) elements.filmographyName.textContent = data.person.name;
      if (elements.filmographyKicker) {
        const roleDesc = data.person.known_for_department ? `${data.person.known_for_department} • Complete Filmography` : "Complete Career Filmography";
        elements.filmographyKicker.textContent = roleDesc;
      }
      if (elements.filmographyAvatar) {
        if (data.person.profile_path) {
          elements.filmographyAvatar.src = `${IMAGE_BASE_URL}${data.person.profile_path}`;
          elements.filmographyAvatar.alt = data.person.name;
          elements.filmographyAvatar.classList.remove("is-hidden");
        } else {
          elements.filmographyAvatar.classList.add("is-hidden");
        }
      }

      const currentDept = data.department || "all";
      if (elements.filmTabAll) {
        elements.filmTabAll.textContent = `All (${data.total_count})`;
        elements.filmTabAll.classList.toggle("is-active", currentDept === "all");
        elements.filmTabAll.onclick = () => loadPersonFilmography(person, entityKey, "all");
      }
      if (elements.filmTabDirecting) {
        elements.filmTabDirecting.textContent = `Directed (${data.directing_count})`;
        elements.filmTabDirecting.classList.toggle("is-active", currentDept === "directing");
        elements.filmTabDirecting.classList.toggle("is-hidden", data.directing_count === 0);
        elements.filmTabDirecting.onclick = () => loadPersonFilmography(person, entityKey, "directing");
      }
      if (elements.filmTabActing) {
        elements.filmTabActing.textContent = `Acted (${data.acting_count})`;
        elements.filmTabActing.classList.toggle("is-active", currentDept === "acting");
        elements.filmTabActing.classList.toggle("is-hidden", data.acting_count === 0);
        elements.filmTabActing.onclick = () => loadPersonFilmography(person, entityKey, "acting");
      }
    }

    state.movies = data.movies || [];
    state.totalResults = state.movies.length;
    renderMovies(state.movies, "search", state.movies.length);
    if (headingBlock) headingBlock.classList.add("is-hidden");

    if (elements.shelfCount) {
      elements.shelfCount.textContent = `${state.movies.length} ${state.movies.length === 1 ? "movie" : "movies"}`;
    }

    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (error) {
    showNotice(`Could not load filmography for ${person.name}: ${error.message}`);
  }
}

async function explorePerson(person, entityKey) {
  await loadPersonFilmography(person, entityKey);
}

function renderVerdict(value) {
  const selected = Number(value || 0);
  elements.verdictStars.replaceChildren();
  for (let rating = 1; rating <= 10; rating += 1) {
    const star = document.createElement("button");
    star.type = "button";
    star.className = "verdict-star";
    star.textContent = "★";
    star.classList.toggle("is-selected", rating <= selected);
    star.setAttribute("aria-label", `${rating} out of 10 stars`);
    star.setAttribute("aria-checked", String(rating === selected));
    star.addEventListener("click", () => saveSelectedVerdict(rating));
    elements.verdictStars.append(star);
  }
}

function feedback(element, message, kind = "success") {
  element.textContent = message;
  element.dataset.kind = kind;
}

async function searchKeywordMovies(query, page = 1) {
  const requestNumber = ++state.requestNumber;
  setEntriesVisible(false);
  state.mode = "keyword-search";
  state.currentView = null;
  setActiveView(null);
  setModeButton(null);
  setSectionCopy({
    kicker: "Your local keywords",
    title: `Movies tagged “${query}”`,
    description: "Official and personal keywords from your local database.",
  });
  showLoadingCards();
  const response = await fetchJSON(
    `/movies/keywords/search?query=${encodeURIComponent(query)}&page=${page}`,
  );
  if (requestNumber !== state.requestNumber) return;
  state.movies = response.results || response.movies || [];
  state.searchPage = Number(response.page || page);
  state.searchTotalPages = Number(response.total_pages || 1);
  state.totalResults = Number(response.total_results || state.movies.length);
  renderMovies(state.movies, "search", state.totalResults);
  renderPagination(
    elements.pagination,
    state.searchPage,
    state.searchTotalPages,
    async (target) => { await searchKeywordMovies(query, target); scrollToResults(); },
  );
}

function renderPersonalControls(movie) {
  const userData = movie.user_data || null;
  const status = userData?.status || "new_discovery";
  const canFavorite = status === "watched" || status === "rewatch";
  const isFavorite = Boolean(userData?.is_favorite);

  elements.statusSelect.value = status;
  elements.favoriteButton.disabled = !canFavorite;
  elements.favoriteButton.classList.toggle("is-favorite", isFavorite);
  const favoriteAction = isFavorite ? "Remove from favourites" : "Add to favourites";
  elements.favoriteButton.setAttribute("aria-label", favoriteAction);
  elements.favoriteButton.title = canFavorite
    ? favoriteAction
    : "Choose Watched or Rewatch before favouriting";
  renderVerdict(userData?.verdict ?? null);
}

function formatReleaseDate(value) {
  if (!value) return "Release date unavailable";
  // Midday UTC prevents the calendar date moving backward in western zones.
  const date = new Date(`${value}T12:00:00Z`);
  return Number.isNaN(date.getTime())
    ? String(value)
    : date.toLocaleDateString(undefined, {
      year: "numeric", month: "long", day: "numeric",
      timeZone: JOURNAL_TIME_ZONE,
    });
}

function renderLookingOutControl(movie) {
  const tracked = Boolean(movie.is_looking_out_for);
  const eligible = Boolean(movie.can_add_to_looking_out_for);
  elements.lookingOutControl.classList.toggle("is-hidden", !tracked && !eligible);
  if (!tracked && !eligible) return;
  elements.lookingOutToggle.textContent = tracked
    ? "✓ Looking Out For"
    : "＋ Looking Out For";
  elements.lookingOutToggle.classList.toggle("is-active", tracked);
  elements.lookingOutReleaseDate.textContent = formatReleaseDate(
    movie.looking_out_for?.release_date || movie.release_date,
  );
  elements.lookingOutToggle.title = tracked
    ? "Remove from Looking Out For"
    : "Remember this unreleased movie";
}

function formatVoteCount(count) {
  const num = Number(count);
  if (!num || isNaN(num) || num <= 0) return "";
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1).replace(/\.0$/, "")}M votes`;
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1).replace(/\.0$/, "")}k votes`;
  }
  return `${num} ${num === 1 ? "vote" : "votes"}`;
}

function renderMovieDetails(movie) {
  state.selectedMovie = movie;
  updateGreyContext();
  elements.dialogPoster.replaceChildren(createPoster(movie));
  elements.dialogKicker.textContent = getStatus(movie)
    ? STATUS_LABELS[getStatus(movie)]
    : "Untracked movie";
  elements.dialogTitle.textContent =
    movie.title || movie.original_title || "Untitled movie";
  elements.dialogMeta.replaceChildren();
  appendMetaItem(getMovieYear(movie));
  appendMetaItem(getMovieLanguage(movie));

  const rating = getMovieRating(movie);

  if (rating) {
    const voteCountStr = formatVoteCount(movie.vote_count);
    appendMetaItem(voteCountStr ? `★ ${rating} TMDB (${voteCountStr})` : `★ ${rating} TMDB`);
  }

  elements.dialogOverview.textContent =
    movie.overview || "No overview is currently available.";
  renderTags(elements.dialogGenres, movie.genres);
  renderMovieKeywords(movie.keywords);
  renderPeople(elements.dialogDirectors, movie.directors, "directors");
  renderPeople(elements.dialogActors, (movie.actors || []).slice(0, 5), "actors");
  renderPersonalControls(movie);
  renderLookingOutControl(movie);
  elements.notes.value = movie.user_data?.notes || "";
  elements.notesPanel.open = true;
  elements.customKeywordForm.classList.add("is-hidden");
  elements.showCustomKeyword.classList.remove("is-hidden");
  [elements.statusFeedback, elements.verdictFeedback, elements.notesFeedback,
    elements.keywordFeedback].forEach((item) => { item.textContent = ""; });
  updateDetailNavStepper(movie.tmdb_id);
}

function renderDetailTrail() {
  elements.detailTrail.replaceChildren();
  const trail = state.detailTrail;
  elements.detailBackLabel.textContent = trail.length > 1
    ? `Back to ${trail[trail.length - 2].title}`
    : state.detailReturnLabel;

  if (trail.length <= 1) return;
  const visibleIndexes = trail.length <= 4
    ? trail.map((_, index) => index)
    : [0, null, trail.length - 2, trail.length - 1];

  visibleIndexes.forEach((index, position) => {
    if (position > 0) {
      const separator = document.createElement("span");
      separator.className = "trail-separator";
      separator.textContent = "→";
      elements.detailTrail.append(separator);
    }
    if (index === null) {
      const ellipsis = document.createElement("span");
      ellipsis.textContent = "…";
      elements.detailTrail.append(ellipsis);
      return;
    }
    const item = trail[index];
    if (index === trail.length - 1) {
      const current = document.createElement("strong");
      current.textContent = item.title;
      current.setAttribute("aria-current", "page");
      elements.detailTrail.append(current);
      return;
    }
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = item.title;
    button.addEventListener("click", () => {
      openMovieDetails(item.id, { trailMode: "jump", trailIndex: index });
    });
    elements.detailTrail.append(button);
  });
}

function createRelatedMovieCard(movie) {
  const movieId = getMovieId(movie);
  const button = document.createElement("button");
  button.type = "button";
  button.className = "related-card";
  const title = movie.title || movie.original_title || "Untitled movie";
  const yearText = getMovieYear(movie);
  button.title = `${title}${yearText ? ` (${yearText})` : ""}`;
  button.setAttribute("aria-label", `Open details for ${title}`);
  button.append(createPoster(movie));

  const status = getStatus(movie);
  if (status) {
    const badge = document.createElement("span");
    badge.className = "status-badge";
    badge.dataset.status = status;
    badge.textContent = STATUS_LABELS[status];
    button.append(badge);
  }

  const rating = getMovieRating(movie);
  if (rating) {
    const ratingElement = document.createElement("span");
    ratingElement.className = "card-rating";
    ratingElement.textContent = rating;
    button.append(ratingElement);
  }

  button.addEventListener("click", () => {
    openMovieDetails(movieId, { trailMode: "push" });
  });
  return button;
}

async function loadRelatedMovies(movieId) {
  elements.relatedMovies.innerHTML = '<p class="related-message">Finding related movies…</p>';
  elements.relatedFamiliarToggle.classList.add("is-hidden");
  try {
    const parameters = new URLSearchParams({
      limit: "12",
      include_previously_watched: String(state.showRelatedFamiliar),
    });
    const response = await fetchJSON(`/movies/${movieId}/related?${parameters}`);
    if (state.selectedMovie?.tmdb_id !== movieId) return;
    const movies = Array.isArray(response.results) ? response.results : [];
    state.detailRelatedMovies = movies;
    const familiarCount = Number(response.hidden_familiar_count || 0);
    if (familiarCount > 0) {
      elements.relatedFamiliarToggle.textContent = state.showRelatedFamiliar
        ? "Hide watched movies"
        : `Show ${familiarCount} watched ${familiarCount === 1 ? "movie" : "movies"}`;
      elements.relatedFamiliarToggle.classList.remove("is-hidden");
    }
    elements.relatedMovies.replaceChildren();
    if (!movies.length) {
      const empty = document.createElement("p");
      empty.className = "related-message";
      empty.textContent = "No useful related movies found yet.";
      elements.relatedMovies.append(empty);
      return;
    }
    movies.forEach((movie) => {
      elements.relatedMovies.append(createRelatedMovieCard(movie));
    });
  } catch (error) {
    if (state.selectedMovie?.tmdb_id !== movieId) return;
    elements.relatedMovies.innerHTML = '<p class="related-message">Related movies could not be loaded.</p>';
  }
}

async function openMovieDetails(
  movieId,
  { trailMode = "root", trailIndex = null } = {},
) {
  const enteringDetails = elements.detailPage.classList.contains("is-hidden");
  if (enteringDetails) {
    state.previousScrollPosition = (elements.shell && elements.shell.scrollTop)
      ? elements.shell.scrollTop
      : window.scrollY;
    state.detailReturnLabel = state.mode === "shelf"
      ? "Back to movies"
      : (state.mode === "filmography"
        ? (state.activeFilmographyPerson ? `Back to ${state.activeFilmographyPerson.name}` : "Back to filmography")
        : (state.mode === "looking-out" ? "Back to Looking Out For" : "Back to results"));

    let activeList = [];
    if (state.currentView === "discover" || state.mode === "search" || state.mode === "discover") {
      activeList = Array.isArray(state.movies) ? state.movies : [];
    } else if (state.mode === "shelf" && Array.isArray(state.allFilteredMovies) && state.allFilteredMovies.length > 0) {
      activeList = state.allFilteredMovies;
    } else {
      activeList = Array.isArray(state.movies) && state.movies.length > 0 ? state.movies : (state.allFilteredMovies || []);
    }
    state.detailNavQueue = [...activeList];
  }
  state.selectedMovie = null;
  state.detailRelatedMovies = [];
  state.showRelatedFamiliar = false;
  elements.shell.classList.add("is-hidden");
  elements.detailPage.classList.remove("is-hidden");
  elements.dialogContent.classList.add("is-hidden");
  elements.dialogLoading.classList.remove("is-hidden");
  elements.dialogLoading.textContent = "Loading movie details…";
  window.scrollTo({ top: 0, behavior: "auto" });
  if (elements.detailPage) {
    elements.detailPage.scrollTop = 0;
  }

  try {
    const movie = await fetchJSON(`/movies/${movieId}`);
    const trailItem = {
      id: movie.tmdb_id,
      title: movie.title || movie.original_title || "Untitled movie",
    };
    if (trailMode === "push") {
      const lastItem = state.detailTrail[state.detailTrail.length - 1];
      if (!lastItem || lastItem.id !== trailItem.id) {
        state.detailTrail.push(trailItem);
      }
    } else if (trailMode === "jump" && Number.isInteger(trailIndex)) {
      state.detailTrail = state.detailTrail.slice(0, trailIndex + 1);
      state.detailTrail[state.detailTrail.length - 1] = trailItem;
    } else {
      state.detailTrail = [trailItem];
    }
    renderMovieDetails(movie);
    renderDetailTrail();
    elements.dialogLoading.classList.add("is-hidden");
    elements.dialogContent.classList.remove("is-hidden");
    loadRelatedMovies(movie.tmdb_id);
  } catch (error) {
    elements.dialogLoading.textContent = error.message;
  }
}

function closeMovieDetails() {
  elements.detailPage.classList.add("is-hidden");
  elements.shell.classList.remove("is-hidden");
  if (elements.shell && state.previousScrollPosition) {
    elements.shell.scrollTop = state.previousScrollPosition;
  }
  window.scrollTo({
    top: state.previousScrollPosition,
    behavior: "auto",
  });
  state.selectedMovie = null;
  state.detailRelatedMovies = [];
  state.detailTrail = [];
  state.detailNavQueue = [];
  if (elements.detailNavStepper) elements.detailNavStepper.classList.add("is-hidden");
  elements.detailTrail.replaceChildren();
  updateGreyContext();
}

function getMovieNavId(movie) {
  if (!movie) return null;
  return Number(movie.tmdb_id || movie.id);
}

function updateDetailNavStepper(currentMovieId) {
  if (!elements.detailPrevBtn || !elements.detailNextBtn) return;
  let queue = state.detailNavQueue || [];
  const numId = Number(currentMovieId);
  let idx = queue.findIndex((m) => getMovieNavId(m) === numId);

  if (idx === -1 && Array.isArray(state.movies)) {
    const moviesIdx = state.movies.findIndex((m) => getMovieNavId(m) === numId);
    if (moviesIdx !== -1) {
      state.detailNavQueue = [...state.movies];
      queue = state.detailNavQueue;
      idx = moviesIdx;
    }
  }

  if (!queue.length) {
    if (elements.detailNavStepper) elements.detailNavStepper.classList.add("is-hidden");
    return;
  }
  if (elements.detailNavStepper) elements.detailNavStepper.classList.remove("is-hidden");

  if (idx === -1) {
    elements.detailPrevBtn.disabled = true;
    elements.detailNextBtn.disabled = true;
    return;
  }

  elements.detailPrevBtn.disabled = idx <= 0;
  elements.detailNextBtn.disabled = idx >= queue.length - 1;
}

function navigatePrevMovie() {
  let queue = state.detailNavQueue || [];
  if (!queue.length || !state.selectedMovie) return;
  const currentId = Number(state.selectedMovie.tmdb_id);
  let idx = queue.findIndex((m) => getMovieNavId(m) === currentId);
  if (idx === -1 && Array.isArray(state.movies)) {
    const moviesIdx = state.movies.findIndex((m) => getMovieNavId(m) === currentId);
    if (moviesIdx !== -1) {
      state.detailNavQueue = [...state.movies];
      queue = state.detailNavQueue;
      idx = moviesIdx;
    }
  }
  if (idx > 0) {
    const prev = queue[idx - 1];
    openMovieDetails(getMovieNavId(prev), { trailMode: "nav" });
  }
}

function navigateNextMovie() {
  let queue = state.detailNavQueue || [];
  if (!queue.length || !state.selectedMovie) return;
  const currentId = Number(state.selectedMovie.tmdb_id);
  let idx = queue.findIndex((m) => getMovieNavId(m) === currentId);
  if (idx === -1 && Array.isArray(state.movies)) {
    const moviesIdx = state.movies.findIndex((m) => getMovieNavId(m) === currentId);
    if (moviesIdx !== -1) {
      state.detailNavQueue = [...state.movies];
      queue = state.detailNavQueue;
      idx = moviesIdx;
    }
  }
  if (idx !== -1 && idx < queue.length - 1) {
    const next = queue[idx + 1];
    openMovieDetails(getMovieNavId(next), { trailMode: "nav" });
  }
}

function navigateBackFromMovie() {
  if (state.detailTrail.length <= 1) {
    closeMovieDetails();
    return;
  }
  const previousIndex = state.detailTrail.length - 2;
  const previous = state.detailTrail[previousIndex];
  openMovieDetails(previous.id, {
    trailMode: "jump",
    trailIndex: previousIndex,
  });
}

function updateVisibleMovie(userData) {
  const movieId = state.selectedMovie?.tmdb_id;

  if (!movieId) {
    return;
  }

  const visibleMovie = state.movies.find(
    (movie) => getMovieId(movie) === movieId,
  );

  if (visibleMovie) {
    visibleMovie.user_data = userData;
  }

  state.selectedMovie.user_data = userData;
  updateMovieCardDOM(movieId, userData);
}

async function saveSelectedStatus() {
  if (!state.selectedMovie) {
    return;
  }

  const movieId = state.selectedMovie.tmdb_id;
  const status = elements.statusSelect.value;
  elements.saveStatus.disabled = true;
  elements.saveStatus.textContent = "Saving…";
  feedback(elements.statusFeedback, "Saving your choice…", "pending");

  try {
    const response = await fetchJSON(`/movies/${movieId}/status`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    });
    updateVisibleMovie(response.user_movie_data);
    clearDiscoveryCache();
    renderPersonalControls(state.selectedMovie);
    elements.dialogKicker.textContent = STATUS_LABELS[status];
    elements.saveStatus.textContent = "✓ Saved";
    elements.saveStatus.classList.add("save-success");
    feedback(elements.statusFeedback, `${STATUS_LABELS[status]} saved.`, "success");
    window.setTimeout(() => {
      elements.saveStatus.textContent = "Save";
      elements.saveStatus.classList.remove("save-success");
      elements.saveStatus.disabled = false;
    }, 1300);
  } catch (error) {
    elements.saveStatus.disabled = false;
    elements.saveStatus.textContent = "Save";
    feedback(elements.statusFeedback, error.message, "error");
  }
}

async function toggleSelectedFavorite() {
  if (!state.selectedMovie || elements.favoriteButton.disabled) {
    return;
  }

  const movieId = state.selectedMovie.tmdb_id;
  const shouldFavorite = !state.selectedMovie.user_data?.is_favorite;
  elements.favoriteButton.disabled = true;

  try {
    const response = await fetchJSON(`/movies/${movieId}/favorite`, {
      method: "PUT",
      body: JSON.stringify({ is_favorite: shouldFavorite }),
    });
    updateVisibleMovie(response.user_movie_data);
    clearDiscoveryCache();
    renderPersonalControls(state.selectedMovie);
    elements.favoriteButton.classList.remove("heart-pop");
    void elements.favoriteButton.offsetWidth;
    elements.favoriteButton.classList.add("heart-pop");
    feedback(
      elements.statusFeedback,
      shouldFavorite ? "Added to favourites." : "Removed from favourites.",
    );
  } catch (error) {
    feedback(elements.statusFeedback, error.message, "error");
    renderPersonalControls(state.selectedMovie);
  }
}

async function toggleLookingOutFor() {
  if (!state.selectedMovie) return;
  const movieId = state.selectedMovie.tmdb_id;
  const removing = Boolean(state.selectedMovie.is_looking_out_for);
  elements.lookingOutToggle.disabled = true;
  try {
    const response = await fetchJSON(`/movies/${movieId}/looking-out-for`, {
      method: removing ? "DELETE" : "POST",
    });
    state.selectedMovie.is_looking_out_for = !removing;
    state.selectedMovie.looking_out_for = removing ? null : response.tracking;
    renderLookingOutControl(state.selectedMovie);
    feedback(
      elements.statusFeedback,
      removing
        ? "Removed from Looking Out For."
        : "Added to Looking Out For.",
    );
    await refreshReleaseAlertBadge();
  } catch (error) {
    feedback(elements.statusFeedback, error.message, "error");
  } finally {
    elements.lookingOutToggle.disabled = false;
  }
}

async function saveSelectedNotes() {
  if (!state.selectedMovie) {
    return;
  }

  const movieId = state.selectedMovie.tmdb_id;
  const notes = elements.notes.value.trim() || null;
  elements.saveNotes.disabled = true;
  elements.saveNotes.textContent = "Saving…";
  feedback(elements.notesFeedback, "Saving…", "pending");

  try {
    const response = await fetchJSON(`/movies/${movieId}/notes`, {
      method: "PUT",
      body: JSON.stringify({ notes }),
    });
    updateVisibleMovie(response.user_movie_data);
    clearDiscoveryCache();
    elements.saveNotes.textContent = "✓ Saved";
    elements.saveNotes.classList.add("save-success");
    feedback(elements.notesFeedback, "Personal memory saved.");

    window.setTimeout(() => {
      elements.saveNotes.textContent = "Save notes";
      elements.saveNotes.classList.remove("save-success");
    }, 1200);
  } catch (error) {
    feedback(elements.notesFeedback, error.message, "error");
    elements.saveNotes.textContent = "Save notes";
  } finally {
    elements.saveNotes.disabled = false;
  }
}

async function saveSelectedVerdict(verdict) {
  if (!state.selectedMovie) return;
  elements.verdictStars.querySelectorAll("button").forEach((button) => {
    button.disabled = true;
  });
  feedback(elements.verdictFeedback, "Saving…", "pending");
  try {
    const response = await fetchJSON(
      `/movies/${state.selectedMovie.tmdb_id}/verdict`,
      { method: "PUT", body: JSON.stringify({ verdict }) },
    );
    updateVisibleMovie(response.user_movie_data);
    renderVerdict(response.user_movie_data.verdict);
    feedback(
      elements.verdictFeedback,
      verdict ? `✓ ${verdict}/10 saved.` : "Verdict cleared.",
    );
  } catch (error) {
    renderVerdict(state.selectedMovie.user_data?.verdict);
    feedback(elements.verdictFeedback, error.message, "error");
  }
}

async function addSelectedKeyword(event) {
  event.preventDefault();
  if (!state.selectedMovie) return;
  const name = elements.customKeyword.value.trim();
  if (!name) {
    elements.customKeyword.focus();
    return;
  }
  const button = elements.customKeywordForm.querySelector("button");
  button.disabled = true;
  button.textContent = "Adding…";
  feedback(elements.keywordFeedback, "Saving personal keyword…", "pending");
  try {
    await fetchJSON(`/movies/${state.selectedMovie.tmdb_id}/keywords/custom`, {
      method: "POST",
      body: JSON.stringify({ name }),
    });
    const movie = await fetchJSON(`/movies/${state.selectedMovie.tmdb_id}`);
    state.selectedMovie = movie;
    renderMovieKeywords(movie.keywords);
    elements.customKeyword.value = "";
    elements.customKeywordForm.classList.add("is-hidden");
    elements.showCustomKeyword.classList.remove("is-hidden");
    feedback(elements.keywordFeedback, `✓ “${name}” added.`);
  } catch (error) {
    feedback(elements.keywordFeedback, error.message, "error");
  } finally {
    button.disabled = false;
    button.textContent = "Add";
  }
}

async function removeSelectedKeyword(tag) {
  if (!state.selectedMovie) return;
  feedback(elements.keywordFeedback, `Removing “${tag.name}”…`, "pending");
  try {
    await fetchJSON(
      `/movies/${state.selectedMovie.tmdb_id}/keywords/custom/${tag.keyword_id}`,
      { method: "DELETE" },
    );
    state.selectedMovie.keywords = state.selectedMovie.keywords.filter(
      (item) => item.keyword_id !== tag.keyword_id,
    );
    renderMovieKeywords(state.selectedMovie.keywords);
    feedback(elements.keywordFeedback, `“${tag.name}” removed.`);
  } catch (error) {
    feedback(elements.keywordFeedback, error.message, "error");
  }
}

function formatRichText(text) {
  if (!text) return "";
  let formatted = String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

  // Markdown links: [Title](https://...)
  formatted = formatted.replace(
    /\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g,
    '<a href="$2" target="_blank" rel="noreferrer noopener" class="note-link">$1</a>',
  );

  // Bold: **text**
  formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // Italics: *text* or _text_
  formatted = formatted.replace(/(^|[^*])\*([^*]+)\*([^*]|$)/g, '$1<em>$2</em>$3');
  formatted = formatted.replace(/(^|[^_])_([^_]+)_([^_]|$)/g, '$1<em>$2</em>$3');

  // Autolink bare URLs: https://...
  return formatted.replace(
    /(^|[\s(])(https?:\/\/[^\s<)]+)/g,
    '$1<a href="$2" target="_blank" rel="noreferrer noopener" class="note-link">$2</a>',
  );
}

function appendEntryBody(container, body) {
  const lines = String(body || "").split(/\r?\n/);
  let ulList = null;
  let olList = null;
  let blockquote = null;
  let activeDetails = null;
  let activeToggleContent = null;
  let activeDetailsIsTag = false;
  let consecutiveEmptyLines = 0;

  function closeToggle() {
    activeDetails = null;
    activeToggleContent = null;
    activeDetailsIsTag = false;
    consecutiveEmptyLines = 0;
    ulList = null;
    olList = null;
    blockquote = null;
  }

  function getTarget() {
    return activeToggleContent || container;
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // 1. Explicit HTML </details> closing tag
    if (trimmed.toLowerCase() === "</details>") {
      closeToggle();
      continue;
    }

    // 2. Explicit HTML <details> opening tag (e.g. <details>, <details open>, or <details><summary>...</summary>)
    if (/^<details\b/i.test(trimmed)) {
      closeToggle();
      activeDetails = document.createElement("details");
      activeDetails.className = "note-toggle";
      if (/\bopen\b/i.test(trimmed)) {
        activeDetails.open = true;
      }
      activeDetailsIsTag = true;
      consecutiveEmptyLines = 0;

      const sameLineSummary = trimmed.match(/<summary\b[^>]*>(.*?)<\/summary>/i);
      let summaryText = "";
      if (sameLineSummary) {
        summaryText = sameLineSummary[1];
      }

      const summaryEl = document.createElement("summary");
      summaryEl.className = "note-toggle-summary";
      if (summaryText) {
        summaryEl.innerHTML = formatRichText(summaryText);
      }
      activeDetails.append(summaryEl);

      activeToggleContent = document.createElement("div");
      activeToggleContent.className = "note-toggle-content";
      activeDetails.append(activeToggleContent);

      container.append(activeDetails);

      if (/<\/details>/i.test(trimmed)) {
        const afterSummary = trimmed.replace(/<details\b[^>]*>/i, "").replace(/<summary\b[^>]*>.*?<\/summary>/i, "").replace(/<\/details>/i, "").trim();
        if (afterSummary) {
          const p = document.createElement("p");
          p.innerHTML = formatRichText(afterSummary);
          activeToggleContent.append(p);
        }
        closeToggle();
      }
      continue;
    }

    // 3. Explicit HTML <summary> tag on its own line
    if (activeDetails && activeDetailsIsTag && /^<summary\b/i.test(trimmed)) {
      const summaryMatch = trimmed.match(/^<summary\b[^>]*>(.*?)<\/summary>$/i) || trimmed.match(/^<summary\b[^>]*>(.*)$/i);
      const summaryText = summaryMatch ? summaryMatch[1].replace(/<\/summary>$/i, "").trim() : "";
      const existingSummary = activeDetails.querySelector(".note-toggle-summary");
      if (existingSummary) {
        existingSummary.innerHTML = formatRichText(summaryText);
      }
      continue;
    }

    // 4. Notion-style toggle prefix (e.g. >> Title, -> Title, ▸ Title, or ▶ Title)
    const toggleMatch = line.match(/^\s*(?:[▸▶]|>>|->)\s*(.+)/);
    if (toggleMatch) {
      closeToggle();
      activeDetails = document.createElement("details");
      activeDetails.className = "note-toggle";
      activeDetailsIsTag = false;
      consecutiveEmptyLines = 0;

      const summaryEl = document.createElement("summary");
      summaryEl.className = "note-toggle-summary";
      summaryEl.innerHTML = formatRichText(toggleMatch[1]);
      activeDetails.append(summaryEl);

      activeToggleContent = document.createElement("div");
      activeToggleContent.className = "note-toggle-content";
      activeDetails.append(activeToggleContent);

      container.append(activeDetails);
      continue;
    }

    // 5. Two blank lines inside a >> toggle exit back to the main note
    if (activeDetails && !activeDetailsIsTag && consecutiveEmptyLines >= 2) {
      const isIndented = /^\s{2,}/.test(line);
      if (!isIndented) {
        closeToggle();
      }
    }
    consecutiveEmptyLines = 0;

    // If an active toggle is open and we hit an unindented top-level heading, close it
    if (activeDetails && !activeDetailsIsTag) {
      if (/^\s*#{1,6}\s+/.test(line)) {
        closeToggle();
      }
    }

    // Heading 3: ### Heading
    const h3Match = line.match(/^\s*###\s+(.+)/);
    if (h3Match) {
      ulList = null; olList = null; blockquote = null;
      const h3 = document.createElement("h3");
      h3.innerHTML = formatRichText(h3Match[1]);
      getTarget().append(h3);
      continue;
    }

    // Heading 2: ## Heading
    const h2Match = line.match(/^\s*##\s+(.+)/);
    if (h2Match) {
      ulList = null; olList = null; blockquote = null;
      const h2 = document.createElement("h2");
      h2.innerHTML = formatRichText(h2Match[1]);
      getTarget().append(h2);
      continue;
    }

    // Blockquote: > text
    const quoteMatch = line.match(/^\s*>\s*(.+)/);
    if (quoteMatch) {
      ulList = null; olList = null;
      const target = getTarget();
      if (!blockquote || blockquote.parentElement !== target) {
        blockquote = document.createElement("blockquote");
        target.append(blockquote);
      }
      const p = document.createElement("p");
      p.innerHTML = formatRichText(quoteMatch[1]);
      blockquote.append(p);
      continue;
    }
    blockquote = null;

    // Numbered list: 1. Item
    const olMatch = line.match(/^\s*\d+\.\s+(.+)/);
    if (olMatch) {
      ulList = null;
      const target = getTarget();
      if (!olList || olList.parentElement !== target) {
        olList = document.createElement("ol");
        target.append(olList);
      }
      const item = document.createElement("li");
      item.innerHTML = formatRichText(olMatch[1]);
      olList.append(item);
      continue;
    }
    olList = null;

    // Bullet list: - Item or * Item
    const ulMatch = line.match(/^\s*[-*]\s+(.+)/);
    if (ulMatch) {
      const target = getTarget();
      if (!ulList || ulList.parentElement !== target) {
        ulList = document.createElement("ul");
        target.append(ulList);
      }
      const item = document.createElement("li");
      item.innerHTML = formatRichText(ulMatch[1]);
      ulList.append(item);
      continue;
    }
    ulList = null;

    if (!trimmed) {
      ulList = null;
      olList = null;
      blockquote = null;
      if (activeDetails && !activeDetailsIsTag) {
        consecutiveEmptyLines += 1;
      }
      continue;
    }

    const paragraph = document.createElement("p");
    paragraph.innerHTML = formatRichText(line);
    getTarget().append(paragraph);
  }
}

function getJournalNow() {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: JOURNAL_TIME_ZONE,
    year: "numeric",
    month: "numeric",
    day: "numeric",
  }).formatToParts(new Date());
  const values = Object.fromEntries(
    parts.filter((part) => part.type !== "literal")
      .map((part) => [part.type, Number(part.value)]),
  );
  return { year: values.year, month: values.month, day: values.day };
}

function populateJournalYears() {
  const { year: currentYear } = getJournalNow();
  elements.entryYearFilter.replaceChildren();
  const anyYear = document.createElement("option");
  anyYear.value = "";
  anyYear.textContent = "Any year";
  elements.entryYearFilter.append(anyYear);
  for (let year = currentYear; year >= JOURNAL_START_YEAR; year -= 1) {
    const option = document.createElement("option");
    option.value = String(year);
    option.textContent = String(year);
    elements.entryYearFilter.append(option);
  }
}

function populateJournalMonths(year = "", selectedMonth = "") {
  const selectedYear = Number(year || 0);
  const firstMonth = selectedYear === JOURNAL_START_YEAR
    ? JOURNAL_START_MONTH
    : 1;
  elements.entryMonthFilter.replaceChildren();
  const anyMonth = document.createElement("option");
  anyMonth.value = "";
  anyMonth.textContent = "Any month";
  elements.entryMonthFilter.append(anyMonth);
  for (let month = firstMonth; month <= 12; month += 1) {
    const option = document.createElement("option");
    option.value = String(month);
    option.textContent = MONTH_NAMES[month - 1];
    elements.entryMonthFilter.append(option);
  }
  if ([...elements.entryMonthFilter.options].some(
    (option) => option.value === String(selectedMonth),
  )) {
    elements.entryMonthFilter.value = String(selectedMonth);
  }
}

function resetEntryFiltersToCurrent(entryType = "") {
  elements.entryQuery.value = "";
  elements.entryTypeFilter.value = entryType;
  state.entryTagFilter = "";
  state.notesTimelineFilter = null;
  state.notesCurrentView = "all";
  if (elements.entryYearFilter) elements.entryYearFilter.value = "";
  if (elements.entryMonthFilter) elements.entryMonthFilter.value = "";
  updateNotesNavActive();
}

function formatEntryDate(value) {
  const date = new Date(`${String(value).replace(" ", "T")}Z`);
  return Number.isNaN(date.getTime())
    ? String(value || "")
    : date.toLocaleDateString(undefined, {
      year: "numeric", month: "short", day: "numeric",
      timeZone: JOURNAL_TIME_ZONE,
    });
}

function formatEntryDateTime(value) {
  const date = new Date(`${String(value).replace(" ", "T")}Z`);
  return Number.isNaN(date.getTime())
    ? String(value || "")
    : date.toLocaleString(undefined, {
      year: "numeric", month: "short", day: "numeric",
      hour: "numeric", minute: "2-digit",
      timeZone: JOURNAL_TIME_ZONE,
    });
}

function entryWasEdited(entry) {
  return String(entry.updated_at || "") !== String(entry.created_at || "");
}

function applyEntryTagFilter(name) {
  state.notesCurrentView = "all";
  state.notesTimelineFilter = null;
  state.entryTagFilter = name;
  elements.entryTypeFilter.value = "";
  if (elements.entryYearFilter) elements.entryYearFilter.value = "";
  if (elements.entryMonthFilter) elements.entryMonthFilter.value = "";
  setAuxiliaryView("entries");
  updateNotesNavActive();
  loadEntries(1);
}

function createEntryTag(tag, clickable = true) {
  const chip = document.createElement(clickable ? "button" : "span");
  if (clickable) chip.type = "button";
  chip.className = "entry-tag";
  chip.textContent = tag.name;
  if (clickable) {
    chip.addEventListener("click", (event) => {
      event.stopPropagation();
      applyEntryTagFilter(tag.name);
    });
  }
  return chip;
}

function renderActiveEntryTag() {
  let button = document.querySelector("#active-entry-tag");
  if (!state.entryTagFilter) {
    button?.remove();
    return;
  }
  if (!button) {
    button = document.createElement("button");
    button.id = "active-entry-tag";
    button.type = "button";
    button.className = "active-entry-tag";
    elements.entryList.before(button);
    button.addEventListener("click", () => {
      state.entryTagFilter = "";
      updateNotesNavActive();
      loadEntries(1);
    });
  }
  const label = state.entryTagFilter === "__untagged__" ? "Untagged" : state.entryTagFilter;
  button.textContent = `Tag: ${label} ×`;
}

function appendEntryLinks(container, value, onRemove = null) {
  container.replaceChildren();
  const urls = String(value || "")
    .split(/[\r\n,]+/)
    .map((url) => url.trim())
    .filter(Boolean);
  if (!urls.length) return;

  const heading = document.createElement("div");
  heading.className = "entry-links-heading";
  heading.textContent = "Attached Links";
  container.append(heading);

  urls.forEach((raw) => {
    const row = document.createElement("div");
    row.className = "entry-link-row";

    const anchor = document.createElement("a");
    anchor.href = /^https?:\/\//i.test(raw) ? raw : `https://${raw}`;
    anchor.textContent = raw;
    anchor.target = "_blank";
    anchor.rel = "noreferrer noopener";
    row.append(anchor);

    if (onRemove) {
      const deleteBtn = document.createElement("button");
      deleteBtn.type = "button";
      deleteBtn.className = "entry-link-remove";
      deleteBtn.title = "Remove this link";
      deleteBtn.setAttribute("aria-label", `Remove ${raw}`);
      deleteBtn.innerHTML = "&times;";
      deleteBtn.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        onRemove(raw);
      });
      row.append(deleteBtn);
    }

    container.append(row);
  });
}

function createExcerptText(body, maxWords = 85) {
  if (!body) return "";
  const paragraphs = String(body)
    .replace(/\r\n/g, "\n")
    .split(/\n\s*\n/)
    .map((p) => p.trim())
    .filter(Boolean);

  const firstPara = paragraphs[0] || "";
  if (!firstPara) return "";

  const text = firstPara
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[#*_~>]/g, "")
    .replace(/\s+/g, " ")
    .trim();

  const words = text.split(/\s+/);
  if (words.length <= maxWords) {
    return text;
  }
  return words.slice(0, maxWords).join(" ") + "…";
}

function updateNotesNavActive() {
  if (elements.notesViewAll) {
    elements.notesViewAll.classList.toggle(
      "is-active",
      state.notesCurrentView === "all" && !state.entryTagFilter && !state.notesTimelineFilter
    );
  }
  if (elements.notesViewArchive) {
    elements.notesViewArchive.classList.toggle(
      "is-active",
      state.notesCurrentView === "archive"
    );
  }
  if (elements.notesViewDrafts) {
    elements.notesViewDrafts.classList.toggle(
      "is-active",
      state.notesCurrentView === "drafts"
    );
  }
  if (elements.notesTagList) {
    elements.notesTagList.querySelectorAll(".notes-tag-link").forEach((btn) => {
      const bTag = (btn.dataset.tag || "").toLowerCase();
      btn.classList.toggle(
        "is-active",
        state.notesCurrentView === "all" && Boolean(state.entryTagFilter) && bTag === state.entryTagFilter.toLowerCase()
      );
    });
  }
  if (elements.notesTimelineList) {
    elements.notesTimelineList.querySelectorAll(".notes-tag-link").forEach((btn) => {
      if (!state.notesTimelineFilter) {
        btn.classList.remove("is-active");
      } else {
        const btnYear = btn.dataset.year;
        const btnMonth = btn.dataset.month;
        const isActive =
          String(state.notesTimelineFilter.year) === String(btnYear) &&
          String(state.notesTimelineFilter.month).padStart(2, "0") === String(btnMonth).padStart(2, "0");
        btn.classList.toggle("is-active", isActive);
      }
    });
  }
}

async function renderNotesTags() {
  if (!elements.notesTagList) return;
  try {
    const data = await fetchJSON("/entries/tags");
    const totalEntries = data.total_entries || 0;
    const archivedEntries = data.archived_entries || 0;
    const draftEntries = data.draft_entries || 0;
    const tags = data.tags || [];

    if (elements.notesTotalCount) {
      elements.notesTotalCount.textContent = String(totalEntries);
    }
    if (elements.notesDraftsCount) {
      elements.notesDraftsCount.textContent = String(draftEntries);
    }
    if (elements.notesArchiveCount) {
      elements.notesArchiveCount.textContent = String(archivedEntries);
    }

    updateNotesNavActive();

    elements.notesTagList.replaceChildren();

    const untaggedEntries = data.untagged_entries || 0;

    tags.forEach((t) => {
      const tagBtn = document.createElement("button");
      tagBtn.type = "button";
      const isTagActive =
        state.notesCurrentView === "all" &&
        Boolean(state.entryTagFilter) &&
        state.entryTagFilter.toLowerCase() === t.name.toLowerCase();
      tagBtn.className = `notes-tag-link ${isTagActive ? "is-active" : ""}`;
      tagBtn.dataset.tag = t.name;

      const tagLabel = document.createElement("span");
      tagLabel.textContent = t.name;
      const tagCount = document.createElement("span");
      tagCount.className = "notes-tag-count";
      tagCount.textContent = String(t.count);
      tagBtn.append(tagLabel, tagCount);

      tagBtn.addEventListener("click", () => {
        state.notesCurrentView = "all";
        state.notesTimelineFilter = null;
        if (state.entryTagFilter.toLowerCase() === t.name.toLowerCase()) {
          state.entryTagFilter = "";
        } else {
          state.entryTagFilter = t.name;
        }
        updateNotesNavActive();
        loadEntries(1);
      });
      elements.notesTagList.append(tagBtn);
    });

    if (untaggedEntries > 0 || state.entryTagFilter === "__untagged__") {
      const untaggedBtn = document.createElement("button");
      untaggedBtn.type = "button";
      const isUntaggedActive =
        state.notesCurrentView === "all" &&
        state.entryTagFilter === "__untagged__";
      untaggedBtn.className = `notes-tag-link notes-tag-untagged ${isUntaggedActive ? "is-active" : ""}`;
      untaggedBtn.dataset.tag = "__untagged__";

      const untaggedLabel = document.createElement("span");
      untaggedLabel.textContent = "Untagged";
      const untaggedCount = document.createElement("span");
      untaggedCount.className = "notes-tag-count";
      untaggedCount.textContent = String(untaggedEntries);
      untaggedBtn.append(untaggedLabel, untaggedCount);

      untaggedBtn.addEventListener("click", () => {
        state.notesCurrentView = "all";
        state.notesTimelineFilter = null;
        if (state.entryTagFilter === "__untagged__") {
          state.entryTagFilter = "";
        } else {
          state.entryTagFilter = "__untagged__";
        }
        updateNotesNavActive();
        loadEntries(1);
      });
      elements.notesTagList.append(untaggedBtn);
    }
  } catch {
    // ignore fetch error
  }
}

async function renderNotesTimeline() {
  if (!elements.notesTimelineList) return;
  try {
    const items = await fetchJSON("/entries/timeline");
    if (!Array.isArray(items) || items.length === 0) {
      if (elements.notesTimelineSection) {
        elements.notesTimelineSection.classList.add("is-hidden");
      }
      elements.notesTimelineList.replaceChildren();
      return;
    }

    if (elements.notesTimelineSection) {
      elements.notesTimelineSection.classList.remove("is-hidden");
    }
    elements.notesTimelineList.replaceChildren();

    const monthNames = [
      "", "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];

    items.forEach((item) => {
      const year = item.year;
      const monthNum = parseInt(item.month, 10);
      const monthName = monthNames[monthNum] || `Month ${item.month}`;
      const count = item.count;

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "notes-tag-link";
      btn.dataset.year = String(year);
      btn.dataset.month = String(item.month);

      const isActive =
        state.notesTimelineFilter &&
        String(state.notesTimelineFilter.year) === String(year) &&
        String(state.notesTimelineFilter.month).padStart(2, "0") === String(item.month).padStart(2, "0");
      if (isActive) btn.classList.add("is-active");

      const label = document.createElement("span");
      label.textContent = `${monthName} ${year}`;
      const countBadge = document.createElement("span");
      countBadge.className = "notes-tag-count";
      countBadge.textContent = String(count);

      btn.append(label, countBadge);
      btn.addEventListener("click", () => {
        state.notesCurrentView = "all";
        state.entryTagFilter = "";
        if (
          state.notesTimelineFilter &&
          String(state.notesTimelineFilter.year) === String(year) &&
          String(state.notesTimelineFilter.month).padStart(2, "0") === String(item.month).padStart(2, "0")
        ) {
          state.notesTimelineFilter = null;
        } else {
          state.notesTimelineFilter = { year: Number(year), month: monthNum };
        }
        updateNotesNavActive();
        loadEntries(1);
      });
      elements.notesTimelineList.append(btn);
    });
  } catch {
    // ignore timeline fetch error
  }
}

async function toggleEntryPin(entryId) {
  try {
    await fetchJSON(`/entries/${entryId}/pin`, { method: "PUT" });
    await loadEntries(state.entryPage);
  } catch (error) {
    showNotice(error.message);
  }
}

async function toggleEntryArchive(entryId, title = "", isCurrentlyArchived = false) {
  try {
    await fetchJSON(`/entries/${entryId}/archive`, { method: "PUT" });
    const actionWord = isCurrentlyArchived ? "restored to active notes" : "moved to archive";
    showNotice(`"${title || "Note"}" ${actionWord}.`);
    await loadEntries(state.entryPage);
    await Promise.all([renderNotesTags(), renderNotesTimeline()]);
  } catch (error) {
    showNotice(error.message);
  }
}

function renderEntries(entries) {
  elements.entryList.replaceChildren();
  renderActiveEntryTag();
  if (!entries.length) {
    const empty = document.createElement("div");
    empty.className = "entry-empty";
    empty.textContent = state.notesCurrentView === "archive"
      ? "No archived notes."
      : state.notesCurrentView === "drafts"
      ? "No drafts in your notebook. Start writing or ask Grey to draft one for you!"
      : "No notes or links match this view.";
    elements.entryList.append(empty);
    return;
  }
  entries.forEach((entry, index) => {
    const article = document.createElement("article");
    article.className = `entry-card ${entry.is_pinned ? "is-pinned" : ""}`;
    article.dataset.entryId = entry.entry_id;

    const header = document.createElement("header");
    const metaRow = document.createElement("div");
    metaRow.className = "entry-card-meta";

    if (entry.status === "draft") {
      const draftBadge = document.createElement("span");
      draftBadge.className = "entry-draft-badge";
      draftBadge.textContent = "📝 Draft";
      metaRow.append(draftBadge);
    }

    const date = document.createElement("time");
    date.className = "entry-card-time";
    date.textContent = entryWasEdited(entry)
      ? `Updated ${formatEntryDate(entry.updated_at)}`
      : formatEntryDate(entry.created_at);

    const actions = document.createElement("div");
    actions.className = "entry-card-actions";

    const pinBtn = document.createElement("button");
    pinBtn.type = "button";
    pinBtn.className = `card-action-btn ${entry.is_pinned ? "is-active" : ""}`;
    pinBtn.title = entry.is_pinned ? "Unpin note" : "Pin note to top";
    pinBtn.innerHTML = "📌";
    pinBtn.addEventListener("click", async (event) => {
      event.stopPropagation();
      await toggleEntryPin(entry.entry_id);
    });

    const archiveBtn = document.createElement("button");
    archiveBtn.type = "button";
    archiveBtn.className = `card-action-btn ${entry.is_archived ? "is-active" : ""}`;
    archiveBtn.title = entry.is_archived ? "Restore to active notes" : "Archive note";
    archiveBtn.innerHTML = entry.is_archived ? "📤" : "📥";
    archiveBtn.addEventListener("click", async (event) => {
      event.stopPropagation();
      await toggleEntryArchive(entry.entry_id, entry.title, entry.is_archived);
    });

    actions.append(pinBtn, archiveBtn);
    metaRow.append(date, actions);

    const title = document.createElement("h3");
    title.textContent = entry.title;
    header.append(metaRow, title);

    let tagsRow = null;
    const entryTags = entry.tags || [];
    if (entryTags.length) {
      tagsRow = document.createElement("div");
      tagsRow.className = "entry-card-tags";
      entryTags.slice(0, 3).forEach((tag) => {
        const pill = createEntryTag(tag);
        pill.addEventListener("click", (event) => {
          event.stopPropagation();
        });
        tagsRow.append(pill);
      });
    }

    const content = document.createElement("div");
    content.className = "entry-card-content";

    const excerpt = document.createElement("p");
    excerpt.className = "entry-card-excerpt";
    excerpt.textContent = createExcerptText(entry.body, 85);
    content.append(excerpt);

    article.addEventListener("click", (event) => {
      if (!event.target.closest("button, a")) {
        openEntryReader(entry, index);
      }
    });

    if (entry.image_url) {
      const bannerThumb = document.createElement("div");
      bannerThumb.className = "entry-card-banner";
      const bannerImg = document.createElement("img");
      bannerImg.src = entry.image_url;
      bannerImg.alt = entry.title || "Note banner";
      bannerImg.loading = "lazy";
      bannerThumb.append(bannerImg);
      article.append(bannerThumb);
    }

    article.append(header);
    if (tagsRow) article.append(tagsRow);
    article.append(content);

    elements.entryList.append(article);
  });
}

function buildEntryParameters(page) {
  const parameters = new URLSearchParams({ page: String(page) });
  const query = elements.entryQuery ? elements.entryQuery.value.trim() : "";
  if (query) parameters.set("query", query);
  if (elements.entryTypeFilter && elements.entryTypeFilter.value) {
    parameters.set("entry_type", elements.entryTypeFilter.value);
  }
  if (state.entryTagFilter) parameters.set("tag", state.entryTagFilter);
  if (state.notesCurrentView === "archive") {
    parameters.set("archived", "true");
  } else if (state.notesCurrentView === "drafts") {
    parameters.set("status", "draft");
  } else {
    parameters.set("status", "published");
  }
  if (state.notesTimelineFilter) {
    if (state.notesTimelineFilter.year) parameters.set("year", String(state.notesTimelineFilter.year));
    if (state.notesTimelineFilter.month) parameters.set("month", String(state.notesTimelineFilter.month));
  } else {
    if (elements.entryYearFilter && elements.entryYearFilter.value) parameters.set("year", elements.entryYearFilter.value);
    if (elements.entryMonthFilter && elements.entryMonthFilter.value) parameters.set("month", elements.entryMonthFilter.value);
  }
  return parameters;
}

async function fetchEntriesPage(page) {
  return fetchJSON(`/entries?${buildEntryParameters(page)}`);
}

async function loadEntries(page = 1) {
  setSearchOriginMovie();
  state.mode = "entries";
  state.currentView = "entries";
  state.entryPage = page;
  setActiveView("entries");
  elements.mobileView.value = "entries";
  setEntriesVisible(true);
  clearNotice();
  elements.entryList.innerHTML = '<div class="entry-empty">Loading your notebook…</div>';
  try {
    const response = await fetchEntriesPage(page);
    state.entryResults = response.results || [];
    state.entryPage = Number(response.page || page);
    state.entryTotalPages = Number(response.total_pages || 1);
    if (page > 1 && state.entryResults.length === 0 && state.entryTotalPages < page) {
      await loadEntries(Math.max(1, state.entryTotalPages));
      return;
    }
    renderEntries(state.entryResults);
    renderNotesTags().catch(() => {});
    renderNotesTimeline().catch(() => {});
    renderPagination(
      elements.entryPagination,
      Number(response.page || page),
      Number(response.total_pages || 1),
      async (target) => { await loadEntries(target); elements.entriesPage.scrollIntoView({ behavior: "smooth" }); },
    );
  } catch (error) {
    elements.entryList.replaceChildren();
    showNotice(error.message);
  }
}

function openEntryReader(entry, index = null, { preserveScroll = false } = {}) {
  if (!preserveScroll) state.entryReturnScroll = window.scrollY;
  state.readerEditing = false;
  elements.entryReader.classList.remove("is-editing");
  state.entryReaderEntry = entry;
  state.entryReaderIndex = index ?? state.entryResults.findIndex(
    (item) => item.entry_id === entry.entry_id,
  );
  try {
    sessionStorage.setItem("nope_open_entry_id", String(entry.entry_id));
  } catch (_) {}
  setAuxiliaryView("entry-reader");
  elements.entryReaderBack.textContent = entry.entry_type === "link"
    ? "← Links"
    : "← Notes";
  const isDraft = entry.status === "draft";
  elements.entryReaderType.textContent = isDraft
    ? `Draft ${entry.entry_type === "link" ? "Link" : "Note"}`
    : entry.entry_type;
  if (elements.entryReaderPublish) {
    elements.entryReaderPublish.classList.toggle("is-hidden", !isDraft);
  }
  elements.entryReaderTitle.textContent = entry.title;
  elements.entryReaderDate.textContent = entryWasEdited(entry)
    ? `Updated ${formatEntryDateTime(entry.updated_at)}`
    : formatEntryDateTime(entry.created_at);
  elements.entryReaderTags.replaceChildren();
  (entry.tags || []).forEach((tag) => {
    elements.entryReaderTags.append(createEntryTag(tag));
  });

  // 16:9 Banner Image (matched to reading text width)
  if (entry.image_url) {
    elements.entryBannerImg.src = entry.image_url;
    elements.entryBannerImg.alt = entry.title || "Note banner";
    elements.entryBannerView.classList.remove("is-hidden");
    elements.entryBannerWrapper?.classList.add("has-banner");
  } else {
    elements.entryBannerView.classList.add("is-hidden");
    elements.entryBannerImg.src = "";
    elements.entryBannerWrapper?.classList.remove("has-banner");
  }

  elements.entryReaderBody.replaceChildren();
  appendEntryBody(elements.entryReaderBody, entry.body);
  appendEntryLinks(elements.entryReaderLinks, entry.url, async (removedUrl) => {
    const currentUrls = String(entry.url || "").split(/[\r\n,]+/).map((u) => u.trim()).filter(Boolean);
    const remainingUrls = currentUrls.filter((u) => u !== removedUrl);
    const newUrlValue = remainingUrls.join("\n") || null;
    const newType = newUrlValue && !entry.body ? "link" : "note";
    try {
      const response = await fetchJSON(`/entries/${entry.entry_id}`, {
        method: "PUT",
        body: JSON.stringify({
          entry_type: newType,
          title: entry.title,
          body: entry.body || null,
          url: newUrlValue,
          tags: (entry.tags || []).map((t) => t.name),
          image_url: entry.image_url || null,
        }),
      });
      const updated = response.entry;
      state.entryReaderEntry = updated;
      const idx = state.entryResults.findIndex((e) => e.entry_id === updated.entry_id);
      if (idx >= 0) state.entryResults[idx] = updated;
      openEntryReader(updated, idx, { preserveScroll: true });
      showNotice("Link removed.");
    } catch (err) {
      showNotice(err.message);
    }
  });
  elements.entryReaderLinks.classList.toggle("is-hidden", !entry.url);
  elements.entryReaderCreated.classList.toggle("is-hidden", !entryWasEdited(entry));
  elements.entryReaderCreated.textContent = entryWasEdited(entry)
    ? `Originally created ${formatEntryDate(entry.created_at)}`
    : "";
  elements.entryReaderPrevious.disabled = state.entryPage === 1 && state.entryReaderIndex <= 0;
  elements.entryReaderNext.disabled = (
    state.entryPage >= state.entryTotalPages
    && state.entryReaderIndex >= state.entryResults.length - 1
  );
  window.scrollTo({ top: 0, behavior: "auto" });
  updateGreyContext();
}

function closeEntryReader() {
  state.entryReaderEntry = null;
  try {
    sessionStorage.removeItem("nope_open_entry_id");
  } catch (_) {}
  setAuxiliaryView("entries");
  renderEntries(state.entryResults);
  window.scrollTo({ top: state.entryReturnScroll, behavior: "auto" });
  updateGreyContext();
}

async function navigateEntryReader(direction) {
  let targetIndex = state.entryReaderIndex + direction;
  if (targetIndex >= 0 && targetIndex < state.entryResults.length) {
    openEntryReader(state.entryResults[targetIndex], targetIndex, { preserveScroll: true });
    return;
  }
  const targetPage = state.entryPage + (direction > 0 ? 1 : -1);
  if (targetPage < 1 || targetPage > state.entryTotalPages) return;
  const response = await fetchEntriesPage(targetPage);
  state.entryPage = Number(response.page || targetPage);
  state.entryTotalPages = Number(response.total_pages || 1);
  state.entryResults = response.results || [];
  targetIndex = direction > 0 ? 0 : state.entryResults.length - 1;
  if (state.entryResults[targetIndex]) {
    openEntryReader(state.entryResults[targetIndex], targetIndex, { preserveScroll: true });
  }
}

async function deleteEntry(entry) {
  if (!entry || !window.confirm(`Delete “${entry.title}”?`)) return;
  await fetchJSON(`/entries/${entry.entry_id}`, { method: "DELETE" });
  showNotice(`Moved “${entry.title}” to trash.`);
  state.entryReaderEntry = null;
  await loadEntries(state.entryPage);
}

function releaseStateCopy(movie) {
  const date = formatReleaseDate(
    movie.looking_out_release_date || movie.release_date,
  );
  if (movie.release_state === "released") return `Now released · ${date}`;
  if (movie.release_state === "today") return `Releases today · ${date}`;
  if (movie.release_state === "soon") {
    return `Releases in ${movie.days_until_release} days · ${date}`;
  }
  return `Releases ${date}`;
}

function createLookingOutCard(movie) {
  const article = document.createElement("article");
  article.className = "looking-out-card";
  const poster = document.createElement("button");
  poster.type = "button";
  poster.className = "looking-out-poster";
  poster.append(createPoster(movie));
  poster.addEventListener("click", () => openMovieDetails(getMovieId(movie)));
  const copy = document.createElement("div");
  copy.className = "looking-out-copy";
  const title = document.createElement("h3");
  title.textContent = movie.title || movie.original_title || "Untitled movie";
  const release = document.createElement("span");
  release.className = "release-state";
  release.dataset.state = movie.release_state;
  release.textContent = releaseStateCopy(movie);
  const actions = document.createElement("div");
  actions.className = "looking-out-actions";
  if (["released", "today"].includes(movie.release_state)) {
    const watchLater = document.createElement("button");
    watchLater.type = "button";
    watchLater.textContent = "Move to Watch Later";
    watchLater.addEventListener("click", async () => {
      watchLater.disabled = true;
      try {
        await fetchJSON(`/movies/${movie.tmdb_id}/looking-out-for/watch-later`, {
          method: "PUT",
        });
        showNotice(`Moved “${title.textContent}” to Watch Later.`);
        await loadLookingOutFor(state.lookingOutPage);
      } catch (error) {
        showNotice(error.message);
      } finally {
        watchLater.disabled = false;
      }
    });
    actions.append(watchLater);
  }
  const remove = document.createElement("button");
  remove.type = "button";
  remove.textContent = "Remove";
  remove.addEventListener("click", async () => {
    if (!window.confirm(`Remove “${title.textContent}” from Looking Out For?`)) return;
    remove.disabled = true;
    try {
      await fetchJSON(`/movies/${movie.tmdb_id}/looking-out-for`, { method: "DELETE" });
      showNotice(`Removed “${title.textContent}” from Looking Out For.`);
      await loadLookingOutFor(state.lookingOutPage);
    } catch (error) {
      showNotice(error.message);
    } finally {
      remove.disabled = false;
    }
  });
  actions.append(remove);
  copy.append(title, release, actions);
  article.append(poster, copy);
  return article;
}

function updateReleaseAlerts(response) {
  const enabled = Boolean(response.release_alerts_enabled);
  const count = Number(response.alert_count || 0);
  elements.releaseAlertsToggle.checked = enabled;
  elements.releaseAlertBadge.textContent = String(count);
  elements.releaseAlertBadge.classList.toggle("is-hidden", !enabled || count < 1);
  elements.releaseAlertSummary.classList.toggle("is-hidden", !enabled || count < 1);
  if (enabled && count > 0) {
    const counts = response.alert_counts || {};
    const parts = [];
    if (counts.released) parts.push(`${counts.released} now released`);
    if (counts.today) parts.push(`${counts.today} releasing today`);
    if (counts.soon) parts.push(`${counts.soon} releasing within 7 days`);
    elements.releaseAlertSummary.textContent = parts.join(" · ");
  }
}

async function loadLookingOutFor(page = 1) {
  setSearchOriginMovie();
  state.mode = "looking-out";
  state.currentView = "looking-out";
  state.lookingOutPage = page;
  setActiveView(null);
  setAuxiliaryView("looking-out");
  elements.lookingOutGrid.innerHTML = '<div class="entry-empty">Checking release dates…</div>';
  try {
    const response = await fetchJSON(`/movies/looking-out-for?page=${page}`);
    const movies = response.results || [];
    elements.lookingOutGrid.replaceChildren();
    if (!movies.length) {
      const empty = document.createElement("div");
      empty.className = "entry-empty";
      empty.textContent = "No upcoming movies are being tracked yet.";
      elements.lookingOutGrid.append(empty);
    } else {
      movies.forEach((movie) => elements.lookingOutGrid.append(createLookingOutCard(movie)));
    }
    updateReleaseAlerts(response);
    renderPagination(
      elements.lookingOutPagination,
      Number(response.page || page),
      Number(response.total_pages || 1),
      async (target) => { await loadLookingOutFor(target); elements.lookingOutPage.scrollIntoView(); },
    );
  } catch (error) {
    const message = document.createElement("div");
    message.className = "entry-empty";
    message.textContent = error.message;
    elements.lookingOutGrid.replaceChildren(message);
  }
}

async function refreshReleaseAlertBadge() {
  try {
    const response = await fetchJSON("/movies/looking-out-for?page=1");
    updateReleaseAlerts(response);
  } catch {
    elements.releaseAlertBadge.classList.add("is-hidden");
  }
}

function formatBytes(value) {
  const bytes = Number(value || 0);
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

async function loadStorage() {
  state.mode = "storage";
  state.currentView = "storage";
  setActiveView(null);
  setAuxiliaryView("storage");
  elements.storageSummary.innerHTML = '<div class="entry-empty">Reading local storage…</div>';
  try {
    const summary = await fetchJSON("/storage");
    const stats = [
      [formatBytes(summary.size_bytes), "SQLite database size"],
      [summary.cached_movies, "Cached movie records"],
      [summary.personal_movies, "Movies with personal status/data"],
      [summary.looking_out_for_movies, "Looking Out For"],
      [summary.old_unprotected_cache_movies, "Disposable cache older than 90 days"],
      [summary.soft_deleted_entries, "Deleted Notes & Links retained"],
    ];
    elements.storageSummary.replaceChildren();
    stats.forEach(([value, label]) => {
      const card = document.createElement("div");
      card.className = "storage-stat";
      const strong = document.createElement("strong");
      const span = document.createElement("span");
      strong.textContent = String(value);
      span.textContent = label;
      card.append(strong, span);
      elements.storageSummary.append(card);
    });
  } catch (error) {
    feedback(elements.storageFeedback, error.message, "error");
  }
}

function updateReaderBlogStats() {
  const bodyText = elements.readerBodyInput?.value || "";
  const words = bodyText.trim().split(/\s+/).filter(Boolean).length;
  if (elements.readerWordCount) {
    elements.readerWordCount.textContent = `${words} ${words === 1 ? "word" : "words"}`;
  }
  if (elements.readerReadTime) {
    const minutes = Math.max(1, Math.ceil(words / 200));
    elements.readerReadTime.textContent = `${minutes} min read`;
  }
}

function renderReaderTagChips() {
  if (!elements.readerTagsChips) return;
  elements.readerTagsChips.replaceChildren();
  state.readerTags.forEach((tagName, idx) => {
    const chip = document.createElement("span");
    chip.className = "reader-tag-chip";
    const text = document.createElement("span");
    text.textContent = tagName;
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "reader-tag-chip-remove";
    removeBtn.setAttribute("aria-label", `Remove tag ${tagName}`);
    removeBtn.textContent = "×";
    removeBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      state.readerTags.splice(idx, 1);
      renderReaderTagChips();
    });
    chip.append(text, removeBtn);
    elements.readerTagsChips.append(chip);
  });
}

function addReaderTagFromInput() {
  if (!elements.readerTagInput) return;
  const raw = elements.readerTagInput.value.replace(/,/g, " ").trim();
  if (raw) {
    const parts = raw.split(/\s+/).filter(Boolean);
    parts.forEach((tag) => {
      if (!state.readerTags.some((t) => t.toLowerCase() === tag.toLowerCase())) {
        state.readerTags.push(tag);
      }
    });
    elements.readerTagInput.value = "";
    renderReaderTagChips();
  }
}

function renderReaderBannerEditor() {
  if (!elements.entryBannerPreviewBox) return;
  const hasBanner = Boolean(state.readerBannerUrl);
  elements.entryBannerWrapper?.classList.toggle("has-banner", hasBanner);
  if (hasBanner) {
    elements.entryBannerPreviewBox.classList.remove("is-hidden");
    elements.entryBannerPreviewImg.src = state.readerBannerUrl;
    elements.entryBannerPickerBar?.classList.add("is-hidden");
    elements.readerAddBannerBtn?.classList.add("is-hidden");
  } else {
    elements.entryBannerPreviewBox.classList.add("is-hidden");
    elements.entryBannerPreviewImg.src = "";
    elements.entryBannerPickerBar?.classList.add("is-hidden");
    elements.readerAddBannerBtn?.classList.remove("is-hidden");
  }
}

let lastBodyInputLength = 0;
function autoResizeReaderBody() {
  const el = elements.readerBodyInput;
  if (!el) return;

  // Modern browsers (Chrome / Edge): native field-sizing without reflow or scroll jumps
  if (window.CSS && CSS.supports && CSS.supports("field-sizing", "content")) {
    el.style.height = "";
    return;
  }

  const currentLength = el.value.length;
  // When typing or pressing Enter, text is growing: expand directly without collapsing height
  if (currentLength >= lastBodyInputLength) {
    lastBodyInputLength = currentLength;
    if (el.scrollHeight > el.clientHeight) {
      el.style.height = `${Math.max(360, el.scrollHeight)}px`;
    }
    return;
  }

  // Text was deleted: adjust height while preserving exact scroll position
  lastBodyInputLength = currentLength;
  const prevScrollY = window.scrollY || document.documentElement.scrollTop;
  el.style.height = "auto";
  const newHeight = Math.max(360, el.scrollHeight);
  el.style.height = `${newHeight}px`;
  window.scrollTo({ top: prevScrollY, behavior: "instant" });
}

async function uploadBannerFile(file) {
  if (!file) return;
  try {
    showNotice("Uploading 16:9 banner…");
    const response = await fetch("/entries/upload-banner", {
      method: "POST",
      headers: {
        "Content-Type": file.type || "application/octet-stream",
        "X-Filename": encodeURIComponent(file.name || "banner.jpg"),
      },
      body: file,
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: "Upload failed." }));
      throw new Error(err.detail || "Upload failed.");
    }
    const data = await response.json();
    state.readerBannerUrl = data.url;
    renderReaderBannerEditor();
    showNotice("Banner image uploaded.");
  } catch (err) {
    showNotice(err.message);
  }
}

function openEntryReaderForNew() {
  state.entryReaderEntry = null;
  state.entryReaderIndex = -1;
  setAuxiliaryView("entry-reader");
  setReaderEditMode(true, true);
  window.scrollTo({ top: 0, behavior: "auto" });
  updateGreyContext();
}

function setReaderEditMode(isEditing, isNew = false) {
  state.readerEditing = isEditing;
  const savedScroll = window.scrollY;
  elements.entryReader.classList.toggle("is-editing", isEditing);

  if (isEditing) {
    state.editingEntryId = isNew ? null : (state.entryReaderEntry?.entry_id || null);
    state.editingEntryStatus = isNew ? "draft" : (state.entryReaderEntry?.status || "published");
    state.readerBannerUrl = isNew ? null : (state.entryReaderEntry?.image_url || null);
    elements.readerTitleInput.value = isNew ? "" : (state.entryReaderEntry?.title || "");
    elements.readerBodyInput.value = isNew ? "" : (state.entryReaderEntry?.body || "");
    elements.readerEditDate.textContent = isNew
      ? "New Draft"
      : (state.entryReaderEntry?.status === "draft"
        ? "Draft"
        : (entryWasEdited(state.entryReaderEntry)
          ? `Updated ${formatEntryDateTime(state.entryReaderEntry.updated_at)}`
          : formatEntryDateTime(state.entryReaderEntry.created_at)));

    state.readerTags = (state.entryReaderEntry?.tags || []).map((t) => typeof t === "string" ? t : t.name);
    renderReaderTagChips();
    renderReaderBannerEditor();
    updateReaderBlogStats();
    autoResizeReaderBody();

    if (elements.readerSaveDraft) {
      elements.readerSaveDraft.textContent = (!isNew && state.editingEntryStatus === "published")
        ? "Save as draft"
        : "Save draft";
    }
    if (elements.readerSavePublish) {
      elements.readerSavePublish.textContent = (!isNew && state.editingEntryStatus === "published")
        ? "Save changes"
        : "Publish to Journal";
    }

    if (isNew) {
      setTimeout(() => {
        autoResizeReaderBody();
        if (!elements.readerTitleInput.value) {
          elements.readerTitleInput.focus({ preventScroll: true });
        } else {
          elements.readerBodyInput.focus({ preventScroll: true });
        }
      }, 60);
    } else {
      setTimeout(() => {
        autoResizeReaderBody();
        elements.readerBodyInput.focus({ preventScroll: true });
        window.scrollTo({ top: savedScroll, behavior: "instant" });
      }, 60);
    }
  } else {
    if (state.entryReaderEntry) {
      openEntryReader(state.entryReaderEntry, state.entryReaderIndex, { preserveScroll: true });
      window.scrollTo({ top: savedScroll, behavior: "instant" });
    } else {
      closeEntryReader();
    }
  }
  updateGreyContext();
}

async function saveReaderEntry(targetStatus = "published") {
  const title = elements.readerTitleInput.value.trim();
  if (!title) {
    showNotice("Please enter a title for your note.");
    elements.readerTitleInput.focus();
    return;
  }
  const body = elements.readerBodyInput.value.trim();
  const editing = Boolean(state.editingEntryId);
  const isSavingDraft = targetStatus === "draft";
  const activeBtn = isSavingDraft ? elements.readerSaveDraft : elements.readerSavePublish;
  const originalText = activeBtn ? activeBtn.textContent : "";
  if (activeBtn) {
    activeBtn.disabled = true;
    activeBtn.textContent = isSavingDraft ? "Saving draft…" : "Publishing…";
  }
  try {
    const existingUrl = state.editingEntryId && state.entryReaderEntry ? (state.entryReaderEntry.url || null) : null;
    const entryType = existingUrl && !body ? "link" : "note";
    const payload = {
      entry_type: entryType,
      title: title,
      body: body || null,
      url: existingUrl,
      tags: state.readerTags,
      status: targetStatus,
      image_url: state.readerBannerUrl || null,
    };
    const response = await fetchJSON(
      editing ? `/entries/${state.editingEntryId}` : "/entries",
      {
        method: editing ? "PUT" : "POST",
        body: JSON.stringify(payload),
      },
    );
    const updated = response.entry;
    state.entryReaderEntry = updated;
    state.editingEntryId = updated.entry_id;
    state.editingEntryStatus = updated.status;
    state.readerBannerUrl = updated.image_url || null;
    showNotice(isSavingDraft ? "Draft saved." : (editing ? "Note updated." : "Note published to Journal."));
    renderNotesTags().catch(() => {});
    renderNotesTimeline().catch(() => {});
    if (editing) {
      const idx = state.entryResults.findIndex((e) => e.entry_id === updated.entry_id);
      if (idx >= 0) state.entryResults[idx] = updated;
    } else {
      await loadEntries(1);
    }
    setReaderEditMode(false);
    updateGreyContext();
  } catch (error) {
    showNotice(error.message);
  } finally {
    if (activeBtn) {
      activeBtn.disabled = false;
      activeBtn.textContent = originalText;
    }
  }
}

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (elements.discoverWorkspace) {
    elements.discoverWorkspace.classList.add("is-hidden");
  }
  if (elements.notesSearchContainer) {
    elements.notesSearchContainer.classList.add("is-hidden");
  }
  searchMovies(elements.query.value);
});

if (elements.nopeModeToggle) {
  elements.nopeModeToggle.addEventListener("click", () => toggleNopeMode());
}

if (elements.nopeUndoCounter) {
  elements.nopeUndoCounter.addEventListener("click", (event) => {
    event.stopPropagation();
    handleNopeUndo();
  });
}

window.addEventListener("keydown", (event) => {
  const activeTag = document.activeElement?.tagName?.toLowerCase();
  const isInput = activeTag === "input" || activeTag === "textarea" || activeTag === "select" || document.activeElement?.isContentEditable;
  const isModalOpen = Boolean(elements.profileDialog?.open || !elements.detailPage?.classList.contains("is-hidden") || state.readerEditing);

  if (!isInput && !isModalOpen && (event.key === "n" || event.key === "N") && !event.ctrlKey && !event.metaKey && !event.altKey) {
    if (state.currentView === "discover") {
      event.preventDefault();
      toggleNopeMode();
    }
    return;
  }

  if (state.nopeMode && state.currentView === "discover" && !isInput && (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "z") {
    event.preventDefault();
    handleNopeUndo();
    return;
  }
});

if (elements.notesSearchInput) {
  elements.notesSearchInput.addEventListener("input", () => {
    window.clearTimeout(notesSearchTimeout);
    notesSearchTimeout = window.setTimeout(() => {
      searchLocalNotes(elements.notesSearchInput.value);
    }, 250);
  });
}

if (elements.clearNotesSearch) {
  elements.clearNotesSearch.addEventListener("click", () => {
    if (elements.notesSearchInput) {
      elements.notesSearchInput.value = "";
      elements.notesSearchInput.focus();
    }
    searchLocalNotes("");
  });
}

if (elements.refreshFeed) {
  elements.refreshFeed.addEventListener("click", () => {
    clearDiscoveryCache();
    runDiscoverySearch({ forceRefresh: true });
  });
}

elements.navLinks.forEach((button) => {
  button.addEventListener("click", () => {
    if (button.dataset.view === "entries") {
      resetEntryFiltersToCurrent();
    }
    loadShelf(button.dataset.view);
  });
});

elements.masterTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    const tabType = tab.dataset.masterTab;
    if (tabType === "discover") {
      loadShelf("discover");
    } else if (tabType === "library") {
      let target = "new_discovery";
      try {
        target = localStorage.getItem("nope_last_library_shelf") || "new_discovery";
      } catch {}
      loadShelf(target);
    } else if (tabType === "notes") {
      resetEntryFiltersToCurrent();
      loadShelf("entries");
    }
  });
});

elements.mobileView.addEventListener("change", () => {
  if (elements.mobileView.value === "entries") {
    resetEntryFiltersToCurrent();
  }
  loadShelf(elements.mobileView.value);
});

elements.modeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    clearDiscoveryCache();
    setSearchOriginMovie();
    setDiscoveryMode(button.dataset.discoveryMode).catch((error) => {
      showNotice(error.message);
    });
  });
});

elements.refreshDiscovery.addEventListener("click", () => {
  clearDiscoveryCache();
  runDiscoverySearch({ forceRefresh: true });
});

elements.advancedForm.addEventListener("submit", (event) => {
  event.preventDefault();
  runDiscoverySearch({ forceRefresh: false });
});

elements.resetFilters.addEventListener("click", () => {
  clearDiscoveryCache();
  resetAdvancedFilters();
});

elements.advancedForm.addEventListener("input", markSelectedProfileModified);
elements.advancedForm.addEventListener("change", markSelectedProfileModified);

elements.profileSelect.addEventListener("change", () => {
  applySelectedProfile().catch((error) => showNotice(error.message));
});

elements.saveProfile.addEventListener("click", () => {
  openProfileDialog("create");
});

elements.cancelProfile.addEventListener("click", () => {
  elements.profileDialog.close();
});

elements.profileNameForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const name = elements.profileName.value.trim();

  if (!name) {
    elements.profileName.focus();
    return;
  }

  const action = state.profileDialogMode === "edit"
    ? updateSelectedProfile(name)
    : saveNewProfile(name);
  action.catch((error) => {
    showNotice(error.message);
    elements.profileDialog.close();
  });
});

elements.updateProfile.addEventListener("click", () => {
  openProfileDialog("edit");
});

if (elements.quickUpdateProfile) {
  elements.quickUpdateProfile.addEventListener("click", () => {
    openProfileDialog("edit");
  });
}

elements.deleteProfile.addEventListener("click", () => {
  deleteSelectedProfile().catch((error) => showNotice(error.message));
});

elements.emptySearchButton.addEventListener("click", () => {
  elements.query.focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

elements.dialogClose.addEventListener("click", () => {
  navigateBackFromMovie();
});

elements.detailPrevBtn?.addEventListener("click", () => {
  navigatePrevMovie();
});

elements.detailNextBtn?.addEventListener("click", () => {
  navigateNextMovie();
});

elements.returnToOrigin.addEventListener("click", () => {
  if (state.savedSearchSnapshot) {
    restoreSearchSnapshot();
    return;
  }
  if (!state.searchOriginMovie) return;
  const originMovieId = state.searchOriginMovie.id;
  setSearchOriginMovie();
  openMovieDetails(originMovieId);
});

elements.saveStatus.addEventListener("click", saveSelectedStatus);
elements.favoriteButton.addEventListener("click", toggleSelectedFavorite);
elements.lookingOutToggle.addEventListener("click", toggleLookingOutFor);
elements.relatedFamiliarToggle.addEventListener("click", () => {
  if (!state.selectedMovie) return;
  state.showRelatedFamiliar = !state.showRelatedFamiliar;
  loadRelatedMovies(state.selectedMovie.tmdb_id);
});
elements.saveNotes.addEventListener("click", saveSelectedNotes);
elements.clearVerdict.addEventListener("click", () => saveSelectedVerdict(null));
elements.customKeywordForm.addEventListener("submit", addSelectedKeyword);
elements.showCustomKeyword.addEventListener("click", () => {
  elements.showCustomKeyword.classList.add("is-hidden");
  elements.customKeywordForm.classList.remove("is-hidden");
  elements.customKeyword.focus();
});
elements.workspaceCollapse.addEventListener("click", () => {
  setWorkspaceCollapsed(!state.filtersCollapsed);
});
elements.notes.addEventListener("focus", () => {
  elements.notes.placeholder = "";
});
elements.notes.addEventListener("blur", () => {
  if (!elements.notes.value) {
    elements.notes.placeholder = "Private thoughts, observations, or anything worth remembering...";
  }
});
elements.notesPanel.addEventListener("toggle", () => {
  const label = elements.notesPanel.querySelector(".summary-action");
  label.textContent = elements.notesPanel.open ? "Minimize" : "Open";
});

elements.newEntry.addEventListener("click", () => openEntryReaderForNew());
elements.entryReaderBack.addEventListener("click", () => closeEntryReader());
elements.readerCancel.addEventListener("click", () => {
  if (!state.editingEntryId) {
    closeEntryReader();
  } else {
    setReaderEditMode(false);
  }
});
elements.readerSaveDraft.addEventListener("click", () => saveReaderEntry("draft"));
elements.readerSavePublish.addEventListener("click", () => saveReaderEntry("published"));
elements.readerBodyInput.addEventListener("input", () => {
  autoResizeReaderBody();
  updateReaderBlogStats();
});
window.addEventListener("resize", autoResizeReaderBody);

elements.readerTagInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === ",") {
    event.preventDefault();
    addReaderTagFromInput();
  }
});
elements.readerTagInput.addEventListener("blur", addReaderTagFromInput);

elements.readerAddBannerBtn?.addEventListener("click", () => {
  elements.entryBannerPickerBar?.classList.toggle("is-hidden");
});
elements.readerCloseBannerPickerBtn?.addEventListener("click", () => {
  elements.entryBannerPickerBar?.classList.add("is-hidden");
});

elements.readerUploadBannerBtn?.addEventListener("click", () => {
  elements.readerBannerFileInput?.click();
});
elements.readerBannerFileInput?.addEventListener("change", (e) => {
  if (e.target.files && e.target.files[0]) {
    uploadBannerFile(e.target.files[0]);
  }
});
elements.readerUrlBannerBtn?.addEventListener("click", () => {
  const current = state.readerBannerUrl || "";
  const input = window.prompt("Enter 16:9 banner image URL:", current);
  if (input !== null) {
    const trimmed = input.trim();
    state.readerBannerUrl = trimmed || null;
    renderReaderBannerEditor();
  }
});
elements.readerChangeBannerBtn?.addEventListener("click", () => {
  elements.readerBannerFileInput?.click();
});
elements.readerRemoveBannerBtn?.addEventListener("click", () => {
  state.readerBannerUrl = null;
  renderReaderBannerEditor();
});

[elements.readerTitleInput, elements.readerBodyInput].forEach((el) => {
  el?.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      event.preventDefault();
      saveReaderEntry("published");
    }
  });
});
elements.entryFilters.addEventListener("submit", (event) => {
  event.preventDefault();
  loadEntries(1);
});
if (elements.entryQuery) {
  let entrySearchTimer = null;
  elements.entryQuery.addEventListener("input", () => {
    clearTimeout(entrySearchTimer);
    entrySearchTimer = setTimeout(() => loadEntries(1), 220);
  });
}
elements.entryYearFilter.addEventListener("change", () => {
  populateJournalMonths(elements.entryYearFilter.value);
});
elements.clearEntryFilters.addEventListener("click", () => {
  elements.entryFilters.reset();
  state.entryTagFilter = "";
  state.notesTimelineFilter = null;
  state.notesCurrentView = "all";
  updateNotesNavActive();
  populateJournalMonths();
  loadEntries(1);
});

if (elements.notesViewAll) {
  elements.notesViewAll.addEventListener("click", () => {
    state.notesCurrentView = "all";
    state.entryTagFilter = "";
    state.notesTimelineFilter = null;
    updateNotesNavActive();
    loadEntries(1);
  });
}

if (elements.notesViewDrafts) {
  elements.notesViewDrafts.addEventListener("click", () => {
    state.notesCurrentView = "drafts";
    state.entryTagFilter = "";
    state.notesTimelineFilter = null;
    updateNotesNavActive();
    loadEntries(1);
  });
}

if (elements.notesViewArchive) {
  elements.notesViewArchive.addEventListener("click", () => {
    state.notesCurrentView = "archive";
    state.entryTagFilter = "";
    state.notesTimelineFilter = null;
    updateNotesNavActive();
    loadEntries(1);
  });
}

elements.entryReaderBack.addEventListener("click", closeEntryReader);
if (elements.entryReaderPublish) {
  elements.entryReaderPublish.addEventListener("click", async () => {
    if (!state.entryReaderEntry || state.entryReaderEntry.status !== "draft") return;
    try {
      elements.entryReaderPublish.disabled = true;
      elements.entryReaderPublish.textContent = "Publishing…";
      const response = await fetchJSON(`/entries/${state.entryReaderEntry.entry_id}/publish`, {
        method: "PUT",
      });
      const published = response.entry;
      state.entryReaderEntry = published;
      showNotice("Published note to Journal!");
      renderNotesTags().catch(() => {});
      openEntryReader(published, state.entryReaderIndex, { preserveScroll: true });
    } catch (err) {
      showNotice(err.message);
    } finally {
      elements.entryReaderPublish.disabled = false;
      elements.entryReaderPublish.textContent = "Publish to Journal";
    }
  });
}
elements.entryReaderEdit.addEventListener("click", () => {
  if (state.entryReaderEntry) setReaderEditMode(true);
});
elements.entryReaderPrevious.addEventListener("click", () => {
  navigateEntryReader(-1).catch((error) => showNotice(error.message));
});
elements.entryReaderNext.addEventListener("click", () => {
  navigateEntryReader(1).catch((error) => showNotice(error.message));
});
elements.entryReaderDelete.addEventListener("click", () => {
  deleteEntry(state.entryReaderEntry).catch((error) => showNotice(error.message));
});

elements.releaseAlertsToggle.addEventListener("change", async () => {
  try {
    await fetchJSON("/settings/release-alerts", {
      method: "PUT",
      body: JSON.stringify({ enabled: elements.releaseAlertsToggle.checked }),
    });
    await loadLookingOutFor(state.lookingOutPage);
  } catch (error) {
    elements.releaseAlertsToggle.checked = !elements.releaseAlertsToggle.checked;
    showNotice(error.message);
  }
});

elements.cleanupCache.addEventListener("click", async () => {
  if (!window.confirm("Remove TMDB-only cache that has been untouched for at least 90 days? Your personal movie data will be preserved.")) return;
  elements.cleanupCache.disabled = true;
  try {
    const result = await fetchJSON("/storage/cleanup-cache?days=90", { method: "POST" });
    feedback(elements.storageFeedback, `${result.removed_movies} disposable movie records removed.`);
    await loadStorage();
  } catch (error) {
    feedback(elements.storageFeedback, error.message, "error");
  } finally {
    elements.cleanupCache.disabled = false;
  }
});

elements.purgeDeletedEntries.addEventListener("click", async () => {
  if (!window.confirm("Permanently remove deleted Notes & Links? This cannot be undone.")) return;
  elements.purgeDeletedEntries.disabled = true;
  try {
    const result = await fetchJSON("/storage/deleted-entries", { method: "DELETE" });
    feedback(elements.storageFeedback, `${result.removed_entries} deleted entries permanently removed.`);
    await loadStorage();
  } catch (error) {
    feedback(elements.storageFeedback, error.message, "error");
  } finally {
    elements.purgeDeletedEntries.disabled = false;
  }
});

elements.footerViews.forEach((button) => {
  button.addEventListener("click", () => {
    const view = button.dataset.footerView;
    if (view === "movie-notes") {
      loadMovieNotes(1);
      return;
    }
    if (view === "looking-out") {
      loadLookingOutFor(1);
      return;
    }
    if (view === "storage") {
      loadStorage();
      return;
    }
    resetEntryFiltersToCurrent(view === "links" ? "link" : "note");
    loadEntries(1);
  });
});

// ============================================================================
// Grey: In-App Cinema Companion
// ============================================================================

function updateGreyContext() {
  if (!elements.greyContextView || !elements.greyContextDetail) return;

  if (state.readerEditing && !elements.entryReader?.classList.contains("is-hidden")) {
    const isDraft = state.editingEntryStatus === "draft";
    elements.greyContextView.textContent = isDraft ? "Draft" : "Journal";
    const title = elements.readerTitleInput?.value?.trim() || "Untitled Note";
    elements.greyContextDetail.textContent = title;
    if (elements.greyStatusText) elements.greyStatusText.textContent = isDraft ? "Writing draft note" : "Writing journal note";
    return;
  }

  if (state.entryReaderEntry && !elements.entryReader?.classList.contains("is-hidden")) {
    const isDraft = state.entryReaderEntry.status === "draft";
    elements.greyContextView.textContent = isDraft ? "Draft" : "Journal";
    elements.greyContextDetail.textContent = state.entryReaderEntry.title || "Untitled";
    if (elements.greyStatusText) elements.greyStatusText.textContent = isDraft ? "Reading draft note" : "Reading journal entry";
    return;
  }

  if (state.selectedMovie) {
    elements.greyContextView.textContent = "Movie";
    const year = state.selectedMovie.release_date ? ` (${state.selectedMovie.release_date.slice(0, 4)})` : "";
    elements.greyContextDetail.textContent = `${state.selectedMovie.title || state.selectedMovie.original_title || "Selected"}${year}`;
    if (elements.greyStatusText) elements.greyStatusText.textContent = "Inspecting movie details";
    return;
  }

  const view = state.currentView || "discover";
  if (view === "discover") {
    elements.greyContextView.textContent = "Discover";
    elements.greyContextDetail.textContent = "Browsing new titles";
    if (elements.greyStatusText) elements.greyStatusText.textContent = "Perched in Discovery";
  } else if (view === "entries" || view === "movie-notes") {
    elements.greyContextView.textContent = "Notes";
    elements.greyContextDetail.textContent = state.entryTagFilter ? `Tag: ${state.entryTagFilter}` : "Personal observations";
    if (elements.greyStatusText) elements.greyStatusText.textContent = "Reading your notes";
  } else {
    elements.greyContextView.textContent = "Library";
    const shelfName = view.replace(/_/g, " ");
    elements.greyContextDetail.textContent = `Shelf: ${shelfName}`;
    if (elements.greyStatusText) elements.greyStatusText.textContent = `Browsing ${shelfName}`;
  }
}

function toggleGreyDrawer(forceOpen) {
  if (!elements.greyDrawer) return;
  const isCurrentlyCollapsed = elements.greyDrawer.classList.contains("is-collapsed");
  const shouldOpen = typeof forceOpen === "boolean" ? forceOpen : isCurrentlyCollapsed;

  if (shouldOpen) {
    document.documentElement.classList.add("grey-docked-open");
    document.body.classList.add("grey-docked-open");
    elements.greyDrawer.classList.remove("is-collapsed");
    elements.greyDrawer.setAttribute("aria-hidden", "false");
    elements.greyToggle?.setAttribute("aria-expanded", "true");
    updateGreyContext();
    elements.greyInput?.focus();
    if (elements.greyMessages) {
      elements.greyMessages.scrollTop = elements.greyMessages.scrollHeight;
    }
  } else {
    document.documentElement.classList.remove("grey-docked-open");
    document.body.classList.remove("grey-docked-open");
    elements.greyDrawer.classList.add("is-collapsed");
    elements.greyDrawer.setAttribute("aria-hidden", "true");
    elements.greyToggle?.setAttribute("aria-expanded", "false");
  }
}

let greyChatHistory = [];

function getTodaySessionDate() {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: JOURNAL_TIME_ZONE,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date());
}

function saveGreyDailySession() {
  try {
    const sessionData = {
      date: getTodaySessionDate(),
      history: greyChatHistory,
      messages: [],
    };
    if (elements.greyMessages) {
      elements.greyMessages.querySelectorAll(".grey-msg").forEach((msgEl) => {
        const isBot = msgEl.classList.contains("grey-msg-bot");
        const p = msgEl.querySelector(".grey-bubble > p");
        const sub = msgEl.querySelector(".grey-subtext");
        if (p) {
          sessionData.messages.push({
            role: isBot ? "bot" : "user",
            text: p.textContent,
            subtext: sub ? sub.textContent : null,
          });
        }
      });
    }
    localStorage.setItem("nope_grey_daily_session", JSON.stringify(sessionData));
  } catch (_) {}
}

function loadGreyDailySession() {
  try {
    const raw = localStorage.getItem("nope_grey_daily_session");
    if (!raw) return false;
    const sessionData = JSON.parse(raw);
    const today = getTodaySessionDate();
    if (sessionData.date !== today || !Array.isArray(sessionData.messages) || sessionData.messages.length <= 1) {
      localStorage.removeItem("nope_grey_daily_session");
      return false;
    }
    greyChatHistory = Array.isArray(sessionData.history) ? sessionData.history : [];
    if (elements.greyMessages && sessionData.messages.length > 0) {
      elements.greyMessages.replaceChildren();
      sessionData.messages.forEach((m) => {
        appendGreyMessage(m.role, m.text, m.subtext, null, { skipSave: true });
      });
      return true;
    }
  } catch (_) {}
  return false;
}

function appendGreyMessage(role, text, subtext, pills, { skipSave = false, skillTag = null } = {}) {
  if (!elements.greyMessages) return;
  const msgEl = document.createElement("div");
  msgEl.className = `grey-msg grey-msg-${role}`;

  const bubble = document.createElement("div");
  bubble.className = "grey-bubble";

  if (skillTag) {
    const badge = document.createElement("span");
    badge.className = "grey-skill-badge";
    badge.textContent = skillTag;
    bubble.append(badge);
  }

  const rawText = String(text || "").trim();
  const paragraphs = rawText.split(/\n\s*\n+/);
  if (paragraphs.length === 0 || !rawText) {
    const p = document.createElement("p");
    p.textContent = rawText;
    bubble.append(p);
  } else {
    paragraphs.forEach((para) => {
      const trimmedPara = para.trim();
      if (!trimmedPara) return;
      const p = document.createElement("p");
      const formattedLines = trimmedPara.split(/\r?\n/).map((line) => {
        let formatted = formatRichText(line);
        formatted = formatted.replace(/\bVerdict:\s*<strong>NOPE<\/strong>/gi, 'Verdict: <strong class="grey-verdict-nope">NOPE</strong>');
        formatted = formatted.replace(/\bVerdict:\s*<strong>YES<\/strong>/gi, 'Verdict: <strong class="grey-verdict-yes">YES</strong>');
        return formatted;
      });
      p.innerHTML = formattedLines.join("<br>");
      bubble.append(p);
    });
  }

  if (subtext) {
    const sub = document.createElement("p");
    sub.className = "grey-subtext";
    sub.textContent = subtext;
    bubble.append(sub);
  }

  msgEl.append(bubble);

  if (Array.isArray(pills) && pills.length > 0) {
    const pillsWrap = document.createElement("div");
    pillsWrap.className = "grey-quick-prompts";
    pills.forEach((pill) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "grey-quick-btn";
      btn.textContent = pill.label;
      btn.addEventListener("click", () => {
        if (pill.action === "prompt" && pill.payload?.prompt) {
          sendGreyMessage(pill.payload.prompt);
        } else if (pill.action === "open_movie" && pill.payload?.tmdb_id) {
          openMovieDetails(pill.payload.tmdb_id);
        } else if (pill.action === "save_shelf" && pill.payload?.name) {
          handleGreySaveShelf(pill.payload.name);
        } else if (pill.action === "open_entry" && pill.payload?.entry_id) {
          fetchJSON(`/entries/${pill.payload.entry_id}`).then((res) => {
            if (res && res.entry) {
              openEntryReader(res.entry);
            }
          }).catch((err) => showNotice(err.message));
        } else if (pill.payload?.prompt) {
          sendGreyMessage(pill.payload.prompt);
        }
      });
      pillsWrap.append(btn);
    });
    msgEl.append(pillsWrap);
  }

  elements.greyMessages.append(msgEl);
  elements.greyMessages.scrollTop = elements.greyMessages.scrollHeight;

  if (!skipSave) {
    saveGreyDailySession();
  }
}

function handleGreyFilterAction(params) {
  if (!params) return;

  // 1. Genres
  if (Array.isArray(params.genres) && params.genres.length > 0) {
    const matchedGenreIds = GENRE_OPTIONS
      .filter(([id, name]) => params.genres.some((g) => g.toLowerCase() === name.toLowerCase()))
      .map(([id]) => Number(id));

    if (matchedGenreIds.length > 0) {
      state.libSelectedGenres = new Set(matchedGenreIds);
      if (elements.libGenresCloud) {
        elements.libGenresCloud.querySelectorAll(".filter-chip").forEach((chip) => {
          const gId = Number(chip.dataset.genreId);
          chip.classList.toggle("is-active", state.libSelectedGenres.has(gId));
        });
      }
    }
  }

  // 2. Languages
  if (Array.isArray(params.languages) && params.languages.length > 0) {
    const langs = params.languages.map((l) => l.toLowerCase());
    state.libSelectedLanguages = new Set(langs);
    if (elements.libLanguagesCloud) {
      elements.libLanguagesCloud.querySelectorAll(".filter-chip").forEach((chip) => {
        const langCode = (chip.dataset.languageCode || chip.textContent || "").toLowerCase();
        chip.classList.toggle("is-active", state.libSelectedLanguages.has(langCode));
      });
    }
  }

  // 3. Years
  if (params.min_year && elements.libYearFrom) {
    elements.libYearFrom.value = String(params.min_year);
  }
  if (params.max_year && elements.libYearTo) {
    elements.libYearTo.value = String(params.max_year);
  }

  // 4. Trigger library filtering
  applyLibraryFilters(1);
}

async function handleGreySaveShelf(shelfName) {
  try {
    const genreIds = [...state.libSelectedGenres];
    const languages = [...state.libSelectedLanguages];
    const payload = {
      name: shelfName || "Grey Curated Shelf",
      is_default: false,
      filters: {
        include_genre_ids: genreIds,
        include_original_languages: languages,
        release_year_from: elements.libYearFrom?.value ? parseInt(elements.libYearFrom.value, 10) : null,
        release_year_to: elements.libYearTo?.value ? parseInt(elements.libYearTo.value, 10) : null,
      },
    };

    await fetchJSON("/search-preferences", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    showNotice(`Shelf "${shelfName}" saved to your ribbon!`);
    await loadProfiles();
  } catch (err) {
    showNotice(`Could not save shelf: ${err.message}`);
  }
}

function updateGreyModelUI(activeModelUsed) {
  if (!elements.greyModelName) return;
  if (activeModelUsed && state.greyModelMode === "auto") {
    elements.greyModelName.textContent = activeModelUsed;
    return;
  }
  if (state.greyModelMode === "flash") {
    elements.greyModelName.textContent = "Flash";
    elements.greyModelTag?.setAttribute("title", "Active Model: Gemini 3.8 Flash. Click to switch to Pro.");
  } else if (state.greyModelMode === "pro") {
    elements.greyModelName.textContent = "Pro";
    elements.greyModelTag?.setAttribute("title", "Active Model: Gemini Pro (Deep Research). Click to switch to Auto.");
  } else {
    elements.greyModelName.textContent = "Auto";
    elements.greyModelTag?.setAttribute("title", "Model Mode: Auto (Flash for speed, Pro for research). Click to switch to Flash.");
  }
}

async function sendGreyMessage(query) {
  if (!query) return;

  appendGreyMessage("user", query);
  if (elements.greyInput) elements.greyInput.value = "";

  const lowerQ = query.toLowerCase();
  let loadingText = "Grey is thinking…";
  if (lowerQ.includes("imdb") || lowerQ.includes("imbd") || lowerQ.includes("link") || lowerQ.includes("url")) {
    loadingText = "Grey is researching links & formatting…";
  } else if (lowerQ.includes("draft") || lowerQ.includes("save this") || lowerQ.includes("summarize") || lowerQ.includes("essay") || lowerQ.includes("compare")) {
    loadingText = "Grey is preparing your note…";
  } else if (lowerQ.includes("rating") || lowerQ.includes("rotten tomatoes") || lowerQ.includes("score") || lowerQ.includes("box office") || lowerQ.includes("trivia")) {
    loadingText = "Grey is researching film data…";
  } else if (lowerQ.includes("recommend") || lowerQ.includes("watch") || lowerQ.includes("suggest") || lowerQ.includes("find me") || lowerQ.includes("what should")) {
    loadingText = "Grey is consulting your library…";
  } else if (state.entryReaderEntry || state.readerEditing) {
    loadingText = "Grey is reading your note…";
  }

  const thinkingEl = document.createElement("div");
  thinkingEl.className = "grey-msg grey-msg-bot";
  thinkingEl.innerHTML = `<div class="grey-bubble" style="color: #9c9aa5; font-style: italic;"><p>${loadingText}</p></div>`;
  elements.greyMessages.append(thinkingEl);
  elements.greyMessages.scrollTop = elements.greyMessages.scrollHeight;

  try {
    let inspectedNote = null;
    if (state.readerEditing && !elements.entryReader?.classList.contains("is-hidden")) {
      inspectedNote = {
        id: state.editingEntryId || null,
        title: elements.readerTitleInput?.value?.trim() || "Untitled Note",
        body: elements.readerBodyInput?.value || "",
        tags: state.readerTags || [],
        status: state.editingEntryStatus || "draft",
      };
    } else if (state.entryReaderEntry && !elements.entryReader?.classList.contains("is-hidden")) {
      inspectedNote = {
        id: state.entryReaderEntry.entry_id,
        title: state.entryReaderEntry.title || "",
        body: state.entryReaderEntry.body || "",
        tags: (state.entryReaderEntry.tags || []).map((t) => typeof t === "string" ? t : t.name),
        status: state.entryReaderEntry.status || "published",
      };
    }

    const payload = {
      message: query,
      current_view: state.currentView || "library",
      inspected_movie_id: state.selectedMovie?.tmdb_id || null,
      inspected_note: inspectedNote,
      related_movies: state.selectedMovie ? (state.detailRelatedMovies || []).map((m) => ({
        id: m.tmdb_id,
        title: m.title || m.original_title,
        year: (m.release_date || "").slice(0, 4),
        rating: m.vote_average,
        status: m.user_data?.status || "unseen",
        verdict: m.user_data?.verdict || null,
      })) : null,
      history: greyChatHistory.slice(-6),
      model_mode: state.greyModelMode || "auto",
    };

    const res = await fetchJSON("/grey/chat", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    thinkingEl.remove();

    if (res.model_used) {
      updateGreyModelUI(res.model_used);
    }

    const skillBadge = res.active_skill ? `⚡ /${res.active_skill}` : null;
    appendGreyMessage("bot", res.text, null, res.pills, { skillTag: skillBadge });

    greyChatHistory.push({ role: "user", text: query });
    greyChatHistory.push({ role: "model", text: res.text });

    if (res.action && res.action.type === "set_movie_status") {
      const { tmdb_id, status } = res.action.params || {};
      if (tmdb_id) {
        if (state.selectedMovie && state.selectedMovie.tmdb_id === tmdb_id) {
          if (status && elements.statusSelect) {
            elements.statusSelect.value = status;
            if (!state.selectedMovie.user_data) state.selectedMovie.user_data = {};
            state.selectedMovie.user_data.status = status;
            elements.dialogKicker.textContent = STATUS_LABELS[status] || status;
            feedback(elements.statusFeedback, `${STATUS_LABELS[status] || status} saved.`, "success");
          }
          renderPersonalControls(state.selectedMovie);
        }
        clearDiscoveryCache();
        updateGreyContext();
      }
    } else if (res.action && res.action.type === "batch_set_movie_status") {
      const { status, movies } = res.action.params || {};
      const movieList = Array.isArray(movies) ? movies : [];
      movieList.forEach((m) => {
        const mId = typeof m === "object" ? (m.tmdb_id || m.id) : m;
        if (mId && state.selectedMovie && state.selectedMovie.tmdb_id === Number(mId)) {
          if (status && elements.statusSelect) {
            elements.statusSelect.value = status;
            if (!state.selectedMovie.user_data) state.selectedMovie.user_data = {};
            state.selectedMovie.user_data.status = status;
            elements.dialogKicker.textContent = STATUS_LABELS[status] || status;
          }
          renderPersonalControls(state.selectedMovie);
        }
        if (mId && state.detailRelatedMovies && Array.isArray(state.detailRelatedMovies)) {
          const relMatch = state.detailRelatedMovies.find((rm) => (rm.tmdb_id || rm.id) === Number(mId));
          if (relMatch) {
            if (!relMatch.user_data) relMatch.user_data = {};
            relMatch.user_data.status = status;
          }
        }
      });
      if (state.selectedMovie && elements.relatedMovies && Array.isArray(state.detailRelatedMovies)) {
        elements.relatedMovies.replaceChildren();
        state.detailRelatedMovies.forEach((rm) => {
          elements.relatedMovies.append(createRelatedMovieCard(rm));
        });
      }
      clearDiscoveryCache();
      updateGreyContext();
      if (status && movieList.length > 0) {
        const label = STATUS_LABELS[status] || status;
        showNotice(`Batch added ${movieList.length} movies to ${label}.`);
      }
    } else if (res.action && res.action.type === "apply_filter") {
      handleGreyFilterAction(res.action.params);
    } else if (res.action && res.action.type === "open_movie" && res.action.params?.tmdb_id) {
      openMovieDetails(res.action.params.tmdb_id);
    } else if (res.action && res.action.type === "create_draft") {
      renderNotesTags().catch(() => {});
    } else if (res.action && res.action.type === "update_entry") {
      const updatedId = res.action.params?.entry_id;
      if (updatedId) {
        if (state.entryReaderEntry && state.entryReaderEntry.entry_id === updatedId) {
          fetchJSON(`/entries/${updatedId}`).then((r) => {
            if (r && r.entry) {
              openEntryReader(r.entry, null, { preserveScroll: true });
            }
          }).catch(() => {});
        }
        if (state.readerEditing && state.editingEntryId === updatedId) {
          fetchJSON(`/entries/${updatedId}`).then((r) => {
            if (r && r.entry) {
              elements.readerTitleInput.value = r.entry.title || "";
              elements.readerBodyInput.value = r.entry.body || "";
              state.readerTags = (r.entry.tags || []).map((t) => typeof t === "string" ? t : t.name);
              state.readerBannerUrl = r.entry.image_url || null;
              renderReaderTagChips();
              renderReaderBannerEditor();
              updateReaderBlogStats();
            }
          }).catch(() => {});
        }
      }
      renderNotesTags().catch(() => {});
    }
  } catch (err) {
    thinkingEl.remove();
    appendGreyMessage("bot", `Connection error: ${err.message}`, "Please ensure the local NOPE backend is running.");
  }
}

function initGreyCompanion() {
  if (!elements.greyToggle) return;

  loadGreyDailySession();

  try {
    state.greyModelMode = localStorage.getItem("nope_grey_model_mode") || "auto";
  } catch (_) {
    state.greyModelMode = "auto";
  }
  updateGreyModelUI();

  elements.greyModelTag?.addEventListener("click", () => {
    const modes = ["auto", "flash", "pro"];
    const nextIdx = (modes.indexOf(state.greyModelMode) + 1) % modes.length;
    state.greyModelMode = modes[nextIdx];
    try {
      localStorage.setItem("nope_grey_model_mode", state.greyModelMode);
    } catch (_) {}
    updateGreyModelUI();
  });

  elements.greyToggle.addEventListener("click", () => toggleGreyDrawer());
  elements.greyCloseBtn?.addEventListener("click", () => toggleGreyDrawer(false));

  elements.greyClearBtn?.addEventListener("click", () => {
    if (!elements.greyMessages) return;
    elements.greyMessages.replaceChildren();
    greyChatHistory = [];
    try {
      localStorage.removeItem("nope_grey_daily_session");
    } catch (_) {}
    appendGreyMessage("bot", "I'm Grey. Conversation cleared and listening to your library.", "Ask me for sharp watchlist picks, instant mood shelves, or film breakdowns.");
  });

  elements.greyDrawer?.addEventListener("click", (e) => {
    const quickBtn = e.target.closest(".grey-quick-btn");
    if (quickBtn && quickBtn.dataset.prompt) {
      sendGreyMessage(quickBtn.dataset.prompt);
    }
  });

  // Slash Commands Autocomplete Menu and Quick Skills Chips
  function hideSlashMenu() {
    if (elements.greySlashMenu) {
      elements.greySlashMenu.classList.add("is-hidden");
      elements.greySlashMenu.querySelectorAll(".grey-slash-item").forEach((it) => it.classList.remove("is-selected"));
    }
  }

  function handleSlashSelection(cmd) {
    if (!cmd) return;
    hideSlashMenu();
    if (cmd === "/related") {
      sendGreyMessage("/related");
    } else if (cmd === "/tonight") {
      sendGreyMessage("/tonight");
    } else {
      if (elements.greyInput) {
        elements.greyInput.value = `${cmd} `;
        elements.greyInput.focus();
        elements.greyInput.selectionStart = elements.greyInput.selectionEnd = elements.greyInput.value.length;
      }
    }
  }

  elements.greySkillsBar?.addEventListener("click", (e) => {
    const chip = e.target.closest(".grey-skill-chip");
    if (chip && chip.dataset.cmd) {
      handleSlashSelection(chip.dataset.cmd);
    }
  });

  elements.greySlashMenu?.addEventListener("click", (e) => {
    const item = e.target.closest(".grey-slash-item");
    if (item && item.dataset.cmd) {
      handleSlashSelection(item.dataset.cmd);
    }
  });

  document.addEventListener("click", (e) => {
    if (!e.target.closest("#grey-slash-menu") && !e.target.closest("#grey-input")) {
      hideSlashMenu();
    }
  });

  elements.greyInput?.addEventListener("input", () => {
    const val = elements.greyInput.value;
    if (val.startsWith("/")) {
      const query = val.toLowerCase().trim();
      const items = elements.greySlashMenu?.querySelectorAll(".grey-slash-item") || [];
      let visibleCount = 0;
      items.forEach((item) => {
        const cmd = (item.dataset.cmd || "").toLowerCase();
        const matches = cmd.startsWith(query) || query === "/";
        item.classList.toggle("is-hidden", !matches);
        if (matches) visibleCount += 1;
      });
      if (visibleCount > 0 && elements.greySlashMenu) {
        elements.greySlashMenu.classList.remove("is-hidden");
      } else {
        hideSlashMenu();
      }
    } else {
      hideSlashMenu();
    }
  });

  // Keyboard navigation: Enter to submit, Shift+Enter for newline, Esc to unfocus
  elements.greyInput?.addEventListener("keydown", (e) => {
    if (elements.greySlashMenu && !elements.greySlashMenu.classList.contains("is-hidden")) {
      const visibleItems = [...elements.greySlashMenu.querySelectorAll(".grey-slash-item:not(.is-hidden)")];
      if (visibleItems.length > 0) {
        let selectedIdx = visibleItems.findIndex((it) => it.classList.contains("is-selected"));
        if (e.key === "ArrowDown") {
          e.preventDefault();
          if (selectedIdx >= 0) visibleItems[selectedIdx].classList.remove("is-selected");
          const nextIdx = (selectedIdx + 1) % visibleItems.length;
          visibleItems[nextIdx].classList.add("is-selected");
          visibleItems[nextIdx].scrollIntoView({ block: "nearest" });
          return;
        } else if (e.key === "ArrowUp") {
          e.preventDefault();
          if (selectedIdx >= 0) visibleItems[selectedIdx].classList.remove("is-selected");
          const prevIdx = (selectedIdx - 1 + visibleItems.length) % visibleItems.length;
          visibleItems[prevIdx].classList.add("is-selected");
          visibleItems[prevIdx].scrollIntoView({ block: "nearest" });
          return;
        } else if (e.key === "Enter" || e.key === "Tab") {
          if (selectedIdx >= 0 && visibleItems[selectedIdx]) {
            e.preventDefault();
            handleSlashSelection(visibleItems[selectedIdx].dataset.cmd);
            return;
          }
        } else if (e.key === "Escape") {
          e.preventDefault();
          hideSlashMenu();
          return;
        }
      }
    }

    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      hideSlashMenu();
      elements.greyForm?.dispatchEvent(new Event("submit", { cancelable: true }));
    } else if (e.key === "Escape") {
      e.preventDefault();
      hideSlashMenu();
      elements.greyInput.blur();
    }
  });

  window.addEventListener("keydown", (e) => {
    const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : "";
    const isInputFocused = activeTag === "input" || activeTag === "textarea" || activeTag === "select" || document.activeElement?.isContentEditable;

    // Left / Right Arrow keys for Prev / Next movie when details page is open
    if (elements.detailPage && !elements.detailPage.classList.contains("is-hidden")) {
      if (!isInputFocused) {
        if (e.key === "ArrowLeft") {
          e.preventDefault();
          navigatePrevMovie();
          return;
        } else if (e.key === "ArrowRight") {
          e.preventDefault();
          navigateNextMovie();
          return;
        }
      }
    }

    // Press 'G' to jump directly into Grey chat input (when not typing in another input)
    if ((e.key === "g" || e.key === "G") && !isInputFocused && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      toggleGreyDrawer(true);
      elements.greyInput?.focus();
      return;
    }

    if (e.key === "Escape") {
      if (document.activeElement === elements.greyInput) {
        e.preventDefault();
        elements.greyInput.blur();
        return;
      }
    } else if ((e.ctrlKey || e.metaKey) && e.code === "Space") {
      e.preventDefault();
      toggleGreyDrawer();
    }
  });

  elements.greyForm?.addEventListener("submit", (e) => {
    e.preventDefault();
    const query = elements.greyInput?.value?.trim();
    if (!query) return;
    sendGreyMessage(query);
  });
}

async function initializeApp() {
  initGreyCompanion();
  if (elements.grid) {
    elements.grid.classList.add("is-compact");
  }

  let hashView = (window.location.hash || "").replace(/^#/, "").trim();
  let openEntryIdFromHash = null;
  if (hashView.startsWith("entry-reader")) {
    const parts = hashView.split(":");
    if (parts.length > 1 && parts[1]) {
      openEntryIdFromHash = parts[1];
    }
    try {
      if (!openEntryIdFromHash) openEntryIdFromHash = sessionStorage.getItem("nope_open_entry_id");
    } catch (_) {}
    hashView = "entry-reader";
  } else if (hashView === "library") {
    try {
      hashView = localStorage.getItem("nope_last_library_shelf") || "new_discovery";
    } catch {
      hashView = "new_discovery";
    }
  } else if (hashView === "notes") {
    hashView = "entries";
  }

  let initialView = hashView;
  if (!initialView) {
    try {
      initialView = localStorage.getItem("nope_current_view") || "discover";
    } catch {
      initialView = "discover";
    }
  }

  const validLibraryViews = ["favorites", "watched", "watch_later", "rewatch", "excluded", "new_discovery", "movie-notes"];
  const validNotesViews = ["entries", "entry-reader"];
  const validAuxViews = ["looking-out", "storage"];

  // Immediately apply view state to DOM BEFORE any async operations so discovery NEVER flashes
  if (validLibraryViews.includes(initialView)) {
    setActiveView(initialView);
    if (elements.discoverWorkspace) elements.discoverWorkspace.classList.add("is-hidden");
    if (elements.notesSearchContainer) elements.notesSearchContainer.classList.add("is-hidden");
    setEntriesVisible(false);
  } else if (validNotesViews.includes(initialView)) {
    setActiveView("entries");
    if (elements.discoverWorkspace) {
      elements.discoverWorkspace.classList.add("is-hidden");
      elements.discoverWorkspace.classList.add("force-hidden");
    }
    if (elements.pagination) {
      elements.pagination.classList.add("is-hidden");
      elements.pagination.classList.add("force-hidden");
    }
    const discoverHeader = document.querySelector("#discover-canvas-header");
    if (discoverHeader) {
      discoverHeader.classList.add("is-hidden");
      discoverHeader.classList.add("force-hidden");
    }
    if (initialView === "entry-reader") {
      setAuxiliaryView("entry-reader");
    } else {
      setEntriesVisible(true);
    }
  } else if (validAuxViews.includes(initialView)) {
    setActiveView(null);
    if (elements.discoverWorkspace) elements.discoverWorkspace.classList.add("is-hidden");
    setEntriesVisible(false);
  } else {
    setActiveView("discover");
    if (elements.discoverWorkspace) elements.discoverWorkspace.classList.remove("is-hidden");
    if (elements.notesSearchContainer) elements.notesSearchContainer.classList.add("is-hidden");
    setEntriesVisible(false);
  }

  initializePickers();
  initializeSortChips();
  initializeEntityPickers();
  initializeCollapsibleFilters();
  initializeNotesCollapsibleSections();
  setupSidebarMasterToggle();
  setupFilterPills();
  setupLibraryFilters();
  setupGenreModeToggle();
  initializeOutsideClosing();
  populateJournalYears();
  resetEntryFiltersToCurrent();

  if (validLibraryViews.includes(initialView)) {
    await Promise.all([
      loadProfiles().catch(() => {}),
      restoreSearchState().catch(() => {}),
      loadShelf(initialView),
    ]);
  } else if (validNotesViews.includes(initialView)) {
    resetEntryFiltersToCurrent();
    await Promise.all([
      loadProfiles().catch(() => {}),
      restoreSearchState().catch(() => {}),
      loadShelf("entries"),
    ]);
    if (initialView === "entry-reader" && openEntryIdFromHash) {
      let entry = (state.entryResults || []).find((e) => String(e.entry_id) === String(openEntryIdFromHash));
      if (!entry) {
        try {
          const fetched = await fetchJSON(`/entries/${openEntryIdFromHash}`);
          if (fetched && fetched.entry) {
            entry = fetched.entry;
          }
        } catch (_) {}
      }
      if (entry) {
        openEntryReader(entry);
      }
    }
  } else if (validAuxViews.includes(initialView)) {
    const auxTask = initialView === "looking-out" ? loadLookingOutFor(1) : loadStorage();
    await Promise.all([
      loadProfiles().catch(() => {}),
      restoreSearchState().catch(() => {}),
      auxTask,
    ]);
  } else {
    await loadProfiles();
    const restoredMode = await restoreSearchState();
    if (elements.discoverWorkspace) {
      elements.discoverWorkspace.classList.remove("is-hidden");
    }
    if (elements.notesSearchContainer) {
      elements.notesSearchContainer.classList.add("is-hidden");
    }
    setActiveView("discover");
    await setDiscoveryMode(restoredMode || "super", true);
  }
  await refreshReleaseAlertBadge();
}

window.addEventListener("hashchange", () => {
  let hashView = (window.location.hash || "").replace(/^#/, "").trim();
  if (hashView.startsWith("entry-reader")) {
    const parts = hashView.split(":");
    const noteId = parts[1] || "";
    if (noteId && (!state.entryReaderEntry || String(state.entryReaderEntry.entry_id) !== String(noteId))) {
      fetchJSON(`/entries/${noteId}`).then((res) => {
        if (res && res.entry) openEntryReader(res.entry);
      }).catch(() => {});
    }
    return;
  }
  if (hashView === "library") {
    try {
      hashView = localStorage.getItem("nope_last_library_shelf") || "new_discovery";
    } catch {
      hashView = "new_discovery";
    }
  } else if (hashView === "notes") {
    hashView = "entries";
  }

  if (!hashView || hashView === "discover") {
    if (state.currentView !== "discover") {
      activateDiscoverView();
    }
  } else if (["favorites", "watched", "watch_later", "rewatch", "excluded", "new_discovery", "entries", "movie-notes"].includes(hashView)) {
    if (state.currentView !== hashView || state.entryReaderEntry) {
      if (hashView === "entries") {
        resetEntryFiltersToCurrent();
      }
      loadShelf(hashView);
    }
  } else if (hashView === "looking-out") {
    if (state.currentView !== "looking-out") {
      loadLookingOutFor(1);
    }
  } else if (hashView === "storage") {
    if (state.currentView !== "storage") {
      loadStorage();
    }
  }
});

initializeApp().catch((error) => showNotice(error.message));
