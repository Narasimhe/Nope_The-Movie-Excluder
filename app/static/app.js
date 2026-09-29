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
  ["en", "English"], ["te", "Telugu"], ["hi", "Hindi"],
  ["ta", "Tamil"], ["ml", "Malayalam"], ["kn", "Kannada"],
  ["bn", "Bengali"], ["ur", "Urdu"], ["ja", "Japanese"],
  ["ko", "Korean"], ["zh", "Chinese"], ["fr", "French"],
  ["es", "Spanish"], ["de", "German"], ["it", "Italian"],
  ["ru", "Russian"], ["pt", "Portuguese"], ["ar", "Arabic"],
];

const COUNTRY_OPTIONS = [
  ["US", "United States"], ["GB", "United Kingdom"], ["IN", "India"],
  ["PK", "Pakistan"], ["CA", "Canada"], ["AU", "Australia"],
  ["JP", "Japan"], ["KR", "South Korea"], ["CN", "China"],
  ["FR", "France"], ["DE", "Germany"], ["IT", "Italy"],
  ["ES", "Spain"], ["RU", "Russia"], ["BR", "Brazil"],
  ["MX", "Mexico"], ["NZ", "New Zealand"], ["IE", "Ireland"],
];

const PICKER_CONFIG = {
  "include-genres": { options: GENRE_OPTIONS, opposite: "exclude-genres" },
  "exclude-genres": { options: GENRE_OPTIONS, opposite: "include-genres" },
  "include-languages": { options: LANGUAGE_OPTIONS, opposite: "exclude-languages" },
  "exclude-languages": { options: LANGUAGE_OPTIONS, opposite: "include-languages" },
  "include-countries": { options: COUNTRY_OPTIONS },
};

const DEFAULT_SYSTEM_FILTERS = {
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
  description: document.querySelector("#library-description"),
  count: document.querySelector("#result-count"),
  navLinks: [...document.querySelectorAll("[data-view]")],
  mobileView: document.querySelector("#mobile-view"),
  discoverWorkspace: document.querySelector("#discovery-workspace"),
  refreshFeed: document.querySelector("#refresh-feed"),
  viewModeToggle: document.querySelector("#view-mode-toggle"),
  viewModeButtons: [...document.querySelectorAll(".view-mode-btn")],
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
  entryDialog: document.querySelector("#entry-dialog"),
  entryForm: document.querySelector("#entry-form"),
  entryDialogTitle: document.querySelector("#entry-dialog-title"),
  entryType: document.querySelector("#entry-type"),
  entryTitle: document.querySelector("#entry-title"),
  entryBody: document.querySelector("#entry-body"),
  entryUrl: document.querySelector("#entry-url"),
  entryTags: document.querySelector("#entry-tags"),
  entryUrlField: document.querySelector("#entry-url-field"),
  cancelEntry: document.querySelector("#cancel-entry"),
  saveEntry: document.querySelector("#save-entry"),
  entryReader: document.querySelector("#entry-reader"),
  entryReaderBack: document.querySelector("#entry-reader-back"),
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
};

const state = {
  movies: [],
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
  },
  currentSearchSpec: null,
  searchPage: 1,
  searchTotalPages: 0,
  totalResults: 0,
  pageLoader: null,
  paginationExact: true,
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
  lookingOutPage: 1,
  showRelatedFamiliar: false,
  profileDialogMode: "create",
  detailTrail: [],
  detailReturnLabel: "Back to movies",
  searchOriginMovie: null,
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
}

function setActiveView(view) {
  elements.navLinks.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.view === view);
  });

  if (view in VIEW_COPY) {
    elements.mobileView.value = view;
  }
}

function getSavedViewMode() {
  return localStorage.getItem("movie_excluder_card_layout") || "compact";
}

function setViewMode(mode) {
  const isCompact = mode !== "detailed";
  localStorage.setItem("movie_excluder_card_layout", isCompact ? "compact" : "detailed");
  elements.grid.classList.toggle("is-compact", isCompact);
  elements.grid.classList.toggle("is-detailed", !isCompact);
  elements.viewModeButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.layout === (isCompact ? "compact" : "detailed"));
  });
}

function showNotice(message) {
  elements.notice.textContent = message;
  elements.notice.classList.remove("is-hidden");
}

function clearNotice() {
  elements.notice.textContent = "";
  elements.notice.classList.add("is-hidden");
}

function updatePickerSummary(container) {
  const checked = [...container.querySelectorAll("input:checked")];
  const summary = container.querySelector("summary");

  if (checked.length === 0) {
    summary.textContent = "Any";
  } else if (checked.length === 1) {
    summary.textContent = checked[0].dataset.label;
  } else {
    summary.textContent = `${checked.length} selected`;
  }
}

function buildMultiPicker(container, config) {
  const details = document.createElement("details");
  const summary = document.createElement("summary");
  const options = document.createElement("div");
  details.className = "multi-picker-menu";
  summary.textContent = "Any";
  options.className = "multi-picker-options";

  const actions = document.createElement("div");
  const clear = document.createElement("button");
  const done = document.createElement("button");
  actions.className = "picker-actions";
  clear.type = "button";
  clear.className = "picker-clear is-hidden";
  clear.textContent = "Clear";
  done.type = "button";
  done.textContent = "Done";
  actions.append(clear, done);

  config.options.forEach(([value, label]) => {
    const option = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = String(value);
    checkbox.dataset.label = label;
    option.append(checkbox, document.createTextNode(label));
    options.append(option);

    checkbox.addEventListener("change", () => {
      if (checkbox.checked && config.opposite) {
        const opposite = document.querySelector(`#${config.opposite}`);
        const oppositeCheckbox = [...opposite.querySelectorAll("input")].find(
          (item) => item.value === checkbox.value,
        );

        if (oppositeCheckbox) {
          oppositeCheckbox.checked = false;
          updatePickerSummary(opposite);
        }
      }

      updatePickerSummary(container);
      clear.classList.toggle(
        "is-hidden",
        !container.querySelector("input:checked"),
      );
      scheduleSearchStateSave();
    });
  });

  clear.addEventListener("click", () => {
    container.querySelectorAll("input:checked").forEach((input) => {
      input.checked = false;
    });
    updatePickerSummary(container);
    clear.classList.add("is-hidden");
    scheduleSearchStateSave();
  });
  done.addEventListener("click", () => {
    details.open = false;
  });

  options.append(actions);
  details.append(summary, options);
  container.append(details);
}

function initializePickers() {
  Object.entries(PICKER_CONFIG).forEach(([id, config]) => {
    const container = document.querySelector(`#${id}`);
    buildMultiPicker(container, config);
  });
}

function getPickerValues(id, numeric = false) {
  return [...document.querySelectorAll(`#${id} input:checked`)].map((input) =>
    numeric ? Number(input.value) : input.value,
  );
}

function setPickerValues(id, values = []) {
  const selected = new Set(values.map((value) => String(value)));
  const container = document.querySelector(`#${id}`);

  container.querySelectorAll("input").forEach((input) => {
    input.checked = selected.has(input.value);
  });

  updatePickerSummary(container);
  const clear = container.querySelector(".picker-clear");
  if (clear) {
    clear.classList.toggle("is-hidden", selected.size === 0);
  }
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
};

function renderSelectedEntities(key) {
  const config = ENTITY_CONFIG[key];
  const container = document.querySelector(`#${config.selectedId}`);
  if (!container) return;
  container.replaceChildren();

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
    });
    container.append(clear);
  }
}

function addSelectedEntity(key, entity) {
  if (key === "keywords" && !entity.mode) {
    entity.mode = "include";
  }
  if (!state.selectedEntities[key].some((item) => item.id === entity.id)) {
    state.selectedEntities[key].push(entity);
    renderSelectedEntities(key);
    updateFilterPillBadges();
    renderActiveFilterTags();
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

  if (!results.length) {
    const empty = document.createElement("p");
    empty.textContent = "No matches found";
    container.append(empty);
  } else {
    results.slice(0, 6).forEach((result) => {
      const button = document.createElement("button");
      const name = document.createElement("strong");
      const context = document.createElement("span");
      button.type = "button";
      name.textContent = result.name || "Unnamed result";
      context.textContent = result.known_for_department
        || result.origin_country
        || (result.known_for_titles || []).slice(0, 2).join(" · ")
        || "TMDB result";
      button.append(name, context);
      button.addEventListener("click", () => {
        addSelectedEntity(key, {
          id: Number(result.id),
          name: result.name || `TMDB #${result.id}`,
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
          const response = await fetchJSON(
            `${config.searchPath}?query=${encodeURIComponent(query)}`,
          );
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
  const incKeywords = await Promise.all((filters.include_keyword_ids || []).map(async (id) => {
    try {
      const result = await fetchJSON(`${ENTITY_CONFIG.keywords.detailPath}${id}`);
      return { id: Number(id), name: result.name || `TMDB #${id}`, mode: "include" };
    } catch {
      return { id: Number(id), name: `TMDB #${id}`, mode: "include" };
    }
  }));

  const excKeywords = await Promise.all((filters.exclude_keyword_ids || []).map(async (id) => {
    try {
      const result = await fetchJSON(`${ENTITY_CONFIG.keywords.detailPath}${id}`);
      return { id: Number(id), name: result.name || `TMDB #${id}`, mode: "exclude" };
    } catch {
      return { id: Number(id), name: `TMDB #${id}`, mode: "exclude" };
    }
  }));

  state.selectedEntities.keywords = [...incKeywords, ...excKeywords];
  renderSelectedEntities("keywords");

  const otherGroups = {
    actors: filters.include_actor_ids || [],
    directors: filters.include_director_ids || [],
    companies: filters.include_company_ids || [],
    excludedCompanies: filters.exclude_company_ids || [],
    excludedKeywords: filters.exclude_keyword_ids || [],
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
    exclude_origin_countries: [],
    include_actor_ids: state.selectedEntities.actors.map((item) => item.id),
    include_director_ids: state.selectedEntities.directors.map((item) => item.id),
    include_keyword_ids: state.selectedEntities.keywords
      .filter((item) => item.mode !== "exclude")
      .map((item) => item.id),
    exclude_keyword_ids: [
      ...state.selectedEntities.keywords
        .filter((item) => item.mode === "exclude")
        .map((item) => item.id),
      ...(state.selectedEntities.excludedKeywords || []).map((item) => item.id),
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
  document.querySelectorAll(".filter-card").forEach((card) => {
    card.classList.add("is-collapsed");
    const heading = card.querySelector(".filter-card-heading");
    if (!heading || heading.querySelector(".filter-card-toggle")) return;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "filter-card-toggle";
    button.textContent = "Open";
    button.setAttribute("aria-expanded", "false");
    button.addEventListener("click", () => {
      const collapsed = card.classList.toggle("is-collapsed");
      button.textContent = collapsed ? "Open" : "Close";
      button.setAttribute("aria-expanded", String(!collapsed));
      updateFilterPillStates();
    });
    heading.append(button);
  });
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

  // Quality badge (rating or year)
  const minRating = elements.minimumRating?.value?.trim();
  const maxRating = elements.maximumRating?.value?.trim();
  const yearFrom = elements.releaseYearFrom?.value?.trim();
  const yearTo = elements.releaseYearTo?.value?.trim();
  const qualityCount = (minRating || maxRating ? 1 : 0) + (yearFrom || yearTo ? 1 : 0);
  const badgeQuality = document.querySelector("#badge-quality");
  if (badgeQuality) {
    badgeQuality.textContent = String(qualityCount);
    badgeQuality.classList.toggle("is-hidden", qualityCount === 0);
  }
  document.querySelector("#pill-quality")?.classList.toggle("has-filters", qualityCount > 0);

  // Origin badge
  const incLang = getPickerValues("include-languages").length;
  const excLang = getPickerValues("exclude-languages").length;
  const incCountry = getPickerValues("include-countries").length;
  const originCount = incLang + excLang + incCountry;
  const badgeOrigin = document.querySelector("#badge-origin");
  if (badgeOrigin) {
    badgeOrigin.textContent = String(originCount);
    badgeOrigin.classList.toggle("is-hidden", originCount === 0);
  }
  document.querySelector("#pill-origin")?.classList.toggle("has-filters", originCount > 0);

  // People badge
  const actors = state.selectedEntities?.actors?.length || 0;
  const directors = state.selectedEntities?.directors?.length || 0;
  const keywords = state.selectedEntities?.keywords?.length || 0;
  const excKeywords = state.selectedEntities?.excludedKeywords?.length || 0;
  const companies = state.selectedEntities?.companies?.length || 0;
  const excCompanies = state.selectedEntities?.excludedCompanies?.length || 0;
  const peopleCount = actors + directors + keywords + excKeywords + companies + excCompanies;
  const badgePeople = document.querySelector("#badge-people");
  if (badgePeople) {
    badgePeople.textContent = String(peopleCount);
    badgePeople.classList.toggle("is-hidden", peopleCount === 0);
  }
  document.querySelector("#pill-people")?.classList.toggle("has-filters", peopleCount > 0);

  // Library badge
  const checkedStatuses = document.querySelectorAll('input[name="included-status"]:checked').length;
  const includeUntracked = elements.includeUntracked?.checked ? 1 : 0;
  const libraryTotal = checkedStatuses + includeUntracked;
  const badgeLibrary = document.querySelector("#badge-library");
  if (badgeLibrary) {
    badgeLibrary.textContent = String(libraryTotal);
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

function setupFilterPills() {
  const pills = document.querySelectorAll(".filter-pill");
  pills.forEach((pill) => {
    pill.addEventListener("click", () => {
      const targetId = pill.dataset.target;
      const card = document.getElementById(targetId);
      if (!card) return;

      const isCollapsed = card.classList.contains("is-collapsed");

      // Accordion mode: collapse other cards or toggle this one
      pills.forEach((p) => {
        if (p !== pill) {
          p.classList.remove("is-open");
          const otherCard = document.getElementById(p.dataset.target);
          if (otherCard) {
            otherCard.classList.add("is-collapsed");
            const btn = otherCard.querySelector(".filter-card-toggle");
            if (btn) {
              btn.textContent = "Open";
              btn.setAttribute("aria-expanded", "false");
            }
          }
        }
      });

      card.classList.toggle("is-collapsed", !isCollapsed);
      pill.classList.toggle("is-open", isCollapsed);

      const toggleBtn = card.querySelector(".filter-card-toggle");
      if (toggleBtn) {
        toggleBtn.textContent = isCollapsed ? "Close" : "Open";
        toggleBtn.setAttribute("aria-expanded", String(isCollapsed));
      }

      setWorkspaceCollapsed(false);

      if (isCollapsed) {
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
        const c = document.getElementById(p.dataset.target);
        if (c) {
          c.classList.add("is-collapsed");
          const btn = c.querySelector(".filter-card-toggle");
          if (btn) {
            btn.textContent = "Open";
            btn.setAttribute("aria-expanded", "false");
          }
        }
      });
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
        const c = document.getElementById(p.dataset.target);
        if (c) {
          c.classList.add("is-collapsed");
          const btn = c.querySelector(".filter-card-toggle");
          if (btn) {
            btn.textContent = "Open";
            btn.setAttribute("aria-expanded", "false");
          }
        }
      });
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
  });
}

async function setAdvancedFilters(filters = {}) {
  state.profilePassthroughFilters = { ...filters };
  setPickerValues("include-genres", filters.include_genre_ids);
  setPickerValues("exclude-genres", filters.exclude_genre_ids);
  setPickerValues("include-languages", filters.include_original_languages);
  setPickerValues("exclude-languages", filters.exclude_original_languages);
  setPickerValues("include-countries", filters.include_origin_countries);
  elements.genreLogic.value = filters.genre_logic || "or";
  elements.minimumRating.value = filters.minimum_rating ?? "";
  elements.maximumRating.value = filters.maximum_rating ?? "";
  elements.minimumVotes.value = filters.minimum_vote_count ?? "";
  elements.releaseYearFrom.value = filters.release_year_from ?? "";
  elements.releaseYearTo.value = filters.release_year_to ?? "";
  elements.sortBy.value = filters.sort_by || "popularity.desc";
  await hydrateEntitySelections(filters);
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
  posterButton.append(createPoster(movie));
  posterButton.addEventListener("click", () => openMovieDetails(movieId));

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
    const noteSnippet = document.createElement("p");
    noteSnippet.className = "card-note-snippet";
    noteSnippet.innerHTML = formatRichText(movie.user_data.notes);
    copy.append(noteSnippet);
  }

  article.append(posterButton, copy);
  return article;
}

function renderMovies(movies, emptyContext = "library", total = null) {
  elements.grid.replaceChildren();
  const count = total ?? movies.length;
  elements.count.textContent = `${count} ${
    count === 1 ? "movie" : "movies"
  }`;

  if (movies.length === 0) {
    elements.grid.classList.add("is-hidden");
    elements.empty.classList.remove("is-hidden");

    if (emptyContext === "search") {
      elements.emptyTitle.textContent = "No matching movies";
      elements.emptyCopy.textContent =
        "Try another title or use fewer words in your search.";
    } else {
      elements.emptyTitle.textContent = "Nothing here yet";
      elements.emptyCopy.textContent =
        "Search for a movie above and give it a personal status.";
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
  document.querySelector(".section-heading").classList.toggle("is-hidden", visible);
  elements.grid.classList.toggle("force-hidden", visible);
  elements.empty.classList.toggle("force-hidden", visible);
  if (elements.discoverWorkspace) {
    elements.discoverWorkspace.classList.toggle("force-hidden", visible);
  }
  if (elements.notesSearchContainer) {
    elements.notesSearchContainer.classList.toggle("force-hidden", visible);
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

async function loadShelf(view, page = 1) {
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
  showLoadingCards();
  elements.count.textContent = "Loading…";

  const url =
    view === "favorites"
      ? "/movies/favorites"
      : `/movies/status/${encodeURIComponent(view)}`;

  try {
    const basePage = (page - 1) * 3;
    const [p1, p2, p3] = await Promise.all([
      fetchJSON(`${url}?page=${basePage + 1}`),
      fetchJSON(`${url}?page=${basePage + 2}`).catch(() => ({ results: [] })),
      fetchJSON(`${url}?page=${basePage + 3}`).catch(() => ({ results: [] })),
    ]);

    if (requestNumber !== state.requestNumber) {
      return;
    }

    const combinedResults = [
      ...(Array.isArray(p1.results) ? p1.results : []),
      ...(Array.isArray(p2.results) ? p2.results : []),
      ...(Array.isArray(p3.results) ? p3.results : []),
    ];

    state.movies = combinedResults;
    state.searchPage = Number(page);
    const backendTotalPages = Number(p1.total_pages || 1);
    state.searchTotalPages = Math.max(1, Math.ceil(backendTotalPages / 3));
    state.totalResults = Number(p1.total_results || combinedResults.length);
    state.pageLoader = (target) => loadShelf(view, target);
    renderMovies(state.movies, "library", state.totalResults);
    renderPagination(
      elements.pagination,
      state.searchPage,
      state.searchTotalPages,
      async (target) => { await loadShelf(view, target); scrollToResults(); },
    );
  } catch (error) {
    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = [];
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
  state.mode = "movie-notes";
  state.currentView = "movie-notes";
  setActiveView("movie-notes");
  setModeButton(null);
  elements.simpleControls.classList.add("is-hidden");
  elements.advancedControls.classList.add("is-hidden");
  elements.pagination.classList.add("is-hidden");
  setSectionCopy(VIEW_COPY["movie-notes"]);
  clearNotice();
  showLoadingCards();
  elements.count.textContent = "Loading…";

  try {
    const basePage = (page - 1) * 3;
    const [p1, p2, p3] = await Promise.all([
      fetchJSON(`/movies/notes?page=${basePage + 1}`),
      fetchJSON(`/movies/notes?page=${basePage + 2}`).catch(() => ({ results: [] })),
      fetchJSON(`/movies/notes?page=${basePage + 3}`).catch(() => ({ results: [] })),
    ]);

    if (requestNumber !== state.requestNumber) return;

    const combinedResults = [
      ...(Array.isArray(p1.results) ? p1.results : []),
      ...(Array.isArray(p2.results) ? p2.results : []),
      ...(Array.isArray(p3.results) ? p3.results : []),
    ];

    state.movies = combinedResults;
    state.searchPage = Number(page);
    const backendTotalPages = Number(p1.total_pages || 1);
    state.searchTotalPages = Math.max(1, Math.ceil(backendTotalPages / 3));
    state.totalResults = Number(p1.total_results || combinedResults.length);
    state.pageLoader = (target) => loadMovieNotes(target);
    renderMovies(state.movies, "library", state.totalResults);
    renderPagination(
      elements.pagination,
      state.searchPage,
      state.searchTotalPages,
      async (target) => { await loadMovieNotes(target); scrollToResults(); },
    );
  } catch (error) {
    if (requestNumber !== state.requestNumber) return;
    state.movies = [];
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

    const combined = [
      ...(Array.isArray(p1.results) ? p1.results : []),
      ...(Array.isArray(p2.results) ? p2.results : []),
      ...(Array.isArray(p3.results) ? p3.results : []),
    ];

    const response = {
      results: combined,
      page: page,
      tmdb_total_pages: Math.max(1, Math.ceil(Number(p1.tmdb_total_pages || 1) / 3)),
      tmdb_total_results: Number(p1.tmdb_total_results || combined.length),
      has_next_page: Boolean(p3.has_next_page || (basePage + 3 < Number(p1.tmdb_total_pages || 1))),
      pagination_exact: p1.pagination_exact !== false,
    };

    discoveryCache.set(nextKey, response);
  } catch {
    // Background prefetch errors are safely ignored
  }
}

async function executeDiscoverySearch(spec, page = 1) {
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

  if (discoveryCache.has(cacheKey)) {
    applyResponse(discoveryCache.get(cacheKey));
    return;
  }

  elements.pagination.classList.add("is-hidden");
  showLoadingCards();
  elements.count.textContent = "Searching…";

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

    const combined = [
      ...(Array.isArray(p1.results) ? p1.results : []),
      ...(Array.isArray(p2.results) ? p2.results : []),
      ...(Array.isArray(p3.results) ? p3.results : []),
    ];

    const response = {
      results: combined,
      page: page,
      tmdb_total_pages: Math.max(1, Math.ceil(Number(p1.tmdb_total_pages || 1) / 3)),
      tmdb_total_results: Number(p1.tmdb_total_results || combined.length),
      has_next_page: Boolean(p3.has_next_page || (basePage + 3 < Number(p1.tmdb_total_pages || 1))),
      pagination_exact: p1.pagination_exact !== false,
    };

    discoveryCache.set(cacheKey, response);
    applyResponse(response);
  } catch (error) {
    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = [];
    renderMovies([], "search");
    showNotice(error.message);
  }
}

async function runDiscoverySearch() {
  await executeDiscoverySearch(buildSearchSpec(), 1);
}

function updateProfileButtons() {
  const preferenceId = Number(elements.profileSelect.value);
  const preference = state.preferences.find(
    (item) => item.preference_id === preferenceId,
  );
  const hasPreference = Boolean(preference);
  elements.updateProfile.disabled = !hasPreference;
  elements.deleteProfile.disabled = !hasPreference;
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
  tags.forEach((tag) => {
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

async function explorePerson(person, entityKey) {
  const personId = Number(person.tmdb_person_id || person.id);
  if (!personId) return;
  const originMovie = {
    id: state.selectedMovie.tmdb_id,
    title: state.selectedMovie.title || state.selectedMovie.original_title,
  };
  closeMovieDetails();
  resetAdvancedFilters({ notify: false });
  state.selectedEntities[entityKey] = [{ id: personId, name: person.name }];
  renderSelectedEntities(entityKey);
  await setDiscoveryMode("advanced", false);
  setSearchOriginMovie(originMovie);
  setWorkspaceCollapsed(false);
  await runDiscoverySearch();
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

function renderMovieDetails(movie) {
  state.selectedMovie = movie;
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
    appendMetaItem(`★ ${rating} TMDB`);
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
  const poster = createPoster(movie);
  const copy = document.createElement("span");
  copy.className = "related-card-copy";
  const title = document.createElement("strong");
  title.textContent = movie.title || movie.original_title || "Untitled movie";
  const meta = document.createElement("span");
  meta.textContent = getMovieYear(movie);
  copy.append(title, meta);
  const status = getStatus(movie);
  if (status) {
    const badge = document.createElement("span");
    badge.className = "status-badge";
    badge.dataset.status = status;
    badge.textContent = STATUS_LABELS[status];
    copy.append(badge);
  }
  button.append(poster, copy);
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
      limit: "6",
      include_previously_watched: String(state.showRelatedFamiliar),
    });
    const response = await fetchJSON(`/movies/${movieId}/related?${parameters}`);
    if (state.selectedMovie?.tmdb_id !== movieId) return;
    const movies = Array.isArray(response.results) ? response.results : [];
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
    state.previousScrollPosition = window.scrollY;
    state.detailReturnLabel = state.mode === "shelf"
      ? "Back to movies"
      : (state.mode === "looking-out" ? "Back to Looking Out For" : "Back to results");
  }
  state.selectedMovie = null;
  state.showRelatedFamiliar = false;
  elements.shell.classList.add("is-hidden");
  elements.detailPage.classList.remove("is-hidden");
  elements.dialogContent.classList.add("is-hidden");
  elements.dialogLoading.classList.remove("is-hidden");
  elements.dialogLoading.textContent = "Loading movie details…";
  window.scrollTo({ top: 0, behavior: "auto" });

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
  window.scrollTo({
    top: state.previousScrollPosition,
    behavior: "auto",
  });
  state.selectedMovie = null;
  state.detailTrail = [];
  elements.detailTrail.replaceChildren();
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
  const escaped = String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

  // Markdown links: [Title](https://...)
  const withMarkdown = escaped.replace(
    /\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g,
    '<a href="$2" target="_blank" rel="noreferrer noopener" class="note-link">$1</a>',
  );

  // Autolink bare URLs: https://...
  return withMarkdown.replace(
    /(^|[\s(])(https?:\/\/[^\s<)]+)/g,
    '$1<a href="$2" target="_blank" rel="noreferrer noopener" class="note-link">$2</a>',
  );
}

function appendEntryBody(container, body) {
  const lines = String(body || "").split(/\r?\n/);
  let list = null;
  lines.forEach((line) => {
    const match = line.match(/^\s*[-*]\s+(.+)/);
    if (match) {
      if (!list) {
        list = document.createElement("ul");
        container.append(list);
      }
      const item = document.createElement("li");
      item.innerHTML = formatRichText(match[1]);
      list.append(item);
      return;
    }
    list = null;
    if (!line.trim()) return;
    const paragraph = document.createElement("p");
    paragraph.innerHTML = formatRichText(line);
    container.append(paragraph);
  });
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
  const { year, month } = getJournalNow();
  elements.entryQuery.value = "";
  elements.entryTypeFilter.value = entryType;
  state.entryTagFilter = "";
  elements.entryYearFilter.value = String(Math.max(year, JOURNAL_START_YEAR));
  populateJournalMonths(elements.entryYearFilter.value, month);
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
  state.entryTagFilter = name;
  elements.entryTypeFilter.value = "";
  setAuxiliaryView("entries");
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
      loadEntries(1);
    });
  }
  button.textContent = `Tag: ${state.entryTagFilter} ×`;
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

function renderEntries(entries) {
  elements.entryList.replaceChildren();
  renderActiveEntryTag();
  if (!entries.length) {
    const empty = document.createElement("div");
    empty.className = "entry-empty";
    empty.textContent = "No notes or links match this view.";
    elements.entryList.append(empty);
    return;
  }
  entries.forEach((entry, index) => {
    const article = document.createElement("article");
    article.className = "entry-card";
    const header = document.createElement("header");
    const type = document.createElement("span");
    const title = document.createElement("h3");
    const date = document.createElement("time");
    type.className = "entry-type";
    type.textContent = entry.entry_type;
    title.textContent = entry.title;
    date.textContent = entryWasEdited(entry)
      ? `Updated ${formatEntryDate(entry.updated_at)}`
      : formatEntryDate(entry.created_at);
    header.append(type, title, date);

    const tags = document.createElement("div");
    tags.className = "entry-card-tags";
    (entry.tags || []).slice(0, 3).forEach((tag) => {
      tags.append(createEntryTag(tag));
    });

    const content = document.createElement("div");
    content.className = "entry-card-content";
    const body = document.createElement("div");
    body.className = "entry-body";
    appendEntryBody(body, entry.body);
    content.append(body);
    if (entry.url) {
      const links = document.createElement("div");
      links.className = "entry-links";
      appendEntryLinks(links, entry.url);
      content.append(links);
    }

    const read = document.createElement("button");
    read.type = "button";
    read.className = "entry-preview-action";
    read.textContent = entry.entry_type === "note" ? "Read note →" : "Open link entry →";
    read.addEventListener("click", (event) => {
      event.stopPropagation();
      openEntryReader(entry, index);
    });
    article.addEventListener("click", (event) => {
      if (!event.target.closest("button, a")) openEntryReader(entry, index);
    });
    article.append(header, tags, content, read);
    elements.entryList.append(article);
  });
}

function buildEntryParameters(page) {
  const parameters = new URLSearchParams({ page: String(page) });
  const query = elements.entryQuery.value.trim();
  if (query) parameters.set("query", query);
  if (elements.entryTypeFilter.value) parameters.set("entry_type", elements.entryTypeFilter.value);
  if (state.entryTagFilter) parameters.set("tag", state.entryTagFilter);
  if (elements.entryYearFilter.value) parameters.set("year", elements.entryYearFilter.value);
  if (elements.entryMonthFilter.value) parameters.set("month", elements.entryMonthFilter.value);
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
    renderEntries(state.entryResults);
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
  state.entryReaderEntry = entry;
  state.entryReaderIndex = index ?? state.entryResults.findIndex(
    (item) => item.entry_id === entry.entry_id,
  );
  setAuxiliaryView("entry-reader");
  elements.entryReaderBack.textContent = entry.entry_type === "link"
    ? "← Links"
    : "← Notes";
  elements.entryReaderType.textContent = entry.entry_type;
  elements.entryReaderTitle.textContent = entry.title;
  elements.entryReaderDate.textContent = entryWasEdited(entry)
    ? `Updated ${formatEntryDateTime(entry.updated_at)}`
    : formatEntryDateTime(entry.created_at);
  elements.entryReaderTags.replaceChildren();
  (entry.tags || []).forEach((tag) => {
    elements.entryReaderTags.append(createEntryTag(tag));
  });
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
}

function closeEntryReader() {
  setAuxiliaryView("entries");
  renderEntries(state.entryResults);
  window.scrollTo({ top: state.entryReturnScroll, behavior: "auto" });
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

function updateBlogStats() {
  const bodyText = elements.entryBody?.value || "";
  const words = bodyText.trim().split(/\s+/).filter(Boolean).length;
  const wordCountEl = document.querySelector("#blog-word-count");
  const readTimeEl = document.querySelector("#blog-read-time");
  if (wordCountEl) {
    wordCountEl.textContent = `${words} ${words === 1 ? "word" : "words"}`;
  }
  if (readTimeEl) {
    const minutes = Math.max(1, Math.ceil(words / 200));
    readTimeEl.textContent = `${minutes} min read`;
  }
}

function openEntryDialog(entry = null) {
  state.editingEntryId = entry?.entry_id || null;
  elements.entryForm.reset();
  elements.entryType.value = entry?.entry_type || "note";
  elements.entryTitle.value = entry?.title || "";
  elements.entryBody.value = entry?.body || "";
  elements.entryUrl.value = entry?.url || "";
  elements.entryTags.value = (entry?.tags || []).map((tag) => tag.name).join(", ");
  elements.entryDialogTitle.textContent = entry ? "Edit note" : "New note";
  updateEntryUrlField();
  updateBlogStats();
  elements.entryDialog.showModal();
  elements.entryTitle.focus();
}

function updateEntryUrlField() {
  if (elements.entryUrlField) {
    elements.entryUrlField.classList.remove("is-hidden");
  }
}

async function saveEntry(event) {
  event.preventDefault();
  const editing = Boolean(state.editingEntryId);
  elements.saveEntry.disabled = true;
  elements.saveEntry.textContent = "Saving…";
  try {
    const rawUrl = elements.entryUrl.value.trim();
    const rawBody = elements.entryBody.value.trim();
    const entryType = rawUrl && !rawBody ? "link" : "note";
    const response = await fetchJSON(
      editing ? `/entries/${state.editingEntryId}` : "/entries",
      {
        method: editing ? "PUT" : "POST",
        body: JSON.stringify({
          entry_type: entryType,
          title: elements.entryTitle.value,
          body: elements.entryBody.value || null,
          url: rawUrl || null,
          tags: elements.entryTags.value.split(",").map((tag) => tag.trim()).filter(Boolean),
        }),
      },
    );
    elements.entryDialog.close();
    showNotice(editing ? "Note updated." : "Note saved.");
    if (editing && state.entryReaderEntry) {
      const updated = response.entry;
      const index = state.entryResults.findIndex(
        (entry) => entry.entry_id === updated.entry_id,
      );
      if (index >= 0) state.entryResults[index] = updated;
      openEntryReader(updated, index, { preserveScroll: true });
    } else {
      await loadEntries(1);
    }
  } catch (error) {
    showNotice(error.message);
  } finally {
    elements.saveEntry.disabled = false;
    elements.saveEntry.textContent = "Save note";
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

elements.viewModeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setViewMode(button.dataset.layout);
  });
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
    runDiscoverySearch();
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
  runDiscoverySearch();
});

elements.advancedForm.addEventListener("submit", (event) => {
  event.preventDefault();
  clearDiscoveryCache();
  runDiscoverySearch();
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

elements.returnToOrigin.addEventListener("click", () => {
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

elements.newEntry.addEventListener("click", () => openEntryDialog());
elements.cancelEntry.addEventListener("click", () => elements.entryDialog.close());
elements.entryType.addEventListener("change", updateEntryUrlField);
elements.entryForm.addEventListener("submit", saveEntry);
elements.entryBody.addEventListener("input", updateBlogStats);
elements.entryForm.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    event.preventDefault();
    elements.entryForm.requestSubmit();
  }
});
elements.entryFilters.addEventListener("submit", (event) => {
  event.preventDefault();
  loadEntries(1);
});
elements.entryYearFilter.addEventListener("change", () => {
  populateJournalMonths(elements.entryYearFilter.value);
});
elements.clearEntryFilters.addEventListener("click", () => {
  elements.entryFilters.reset();
  state.entryTagFilter = "";
  populateJournalMonths();
  loadEntries(1);
});

elements.entryReaderBack.addEventListener("click", closeEntryReader);
elements.entryReaderEdit.addEventListener("click", () => {
  if (state.entryReaderEntry) openEntryDialog(state.entryReaderEntry);
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

async function initializeApp() {
  setViewMode(getSavedViewMode());
  initializePickers();
  initializeEntityPickers();
  initializeCollapsibleFilters();
  setupFilterPills();
  initializeOutsideClosing();
  populateJournalYears();
  resetEntryFiltersToCurrent();
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
  await refreshReleaseAlertBadge();
}

initializeApp().catch((error) => showNotice(error.message));
