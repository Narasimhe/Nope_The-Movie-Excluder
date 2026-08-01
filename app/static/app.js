const IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500";

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
  "include-countries": { options: COUNTRY_OPTIONS, opposite: "exclude-countries" },
  "exclude-countries": { options: COUNTRY_OPTIONS, opposite: "include-countries" },
};

const STATUS_LABELS = {
  new_discovery: "New discovery",
  watch_later: "Watch later",
  watched: "Watched",
  rewatch: "Rewatch",
  excluded: "Nope",
};

const VIEW_COPY = {
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
  entryUrlField: document.querySelector("#entry-url-field"),
  cancelEntry: document.querySelector("#cancel-entry"),
  saveEntry: document.querySelector("#save-entry"),
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
  profileDialogMode: "create",
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
  container.replaceChildren();

  state.selectedEntities[key].forEach((entity) => {
    const chip = document.createElement("span");
    const name = document.createElement("span");
    const remove = document.createElement("button");
    chip.className = "selected-entity";
    name.textContent = entity.name;
    remove.type = "button";
    remove.textContent = "×";
    remove.setAttribute("aria-label", `Remove ${entity.name}`);
    remove.addEventListener("click", () => {
      state.selectedEntities[key] = state.selectedEntities[key].filter(
        (item) => item.id !== entity.id,
      );
      renderSelectedEntities(key);
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
      scheduleSearchStateSave();
    });
    container.append(clear);
  }
}

function addSelectedEntity(key, entity) {
  if (!state.selectedEntities[key].some((item) => item.id === entity.id)) {
    state.selectedEntities[key].push(entity);
    renderSelectedEntities(key);
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
    let timer = null;

    input.addEventListener("input", () => {
      window.clearTimeout(timer);
      const query = input.value.trim();
      const results = document.querySelector(`#${config.resultsId}`);

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
  const idGroups = {
    actors: filters.include_actor_ids || [],
    directors: filters.include_director_ids || [],
    keywords: filters.include_keyword_ids || [],
    excludedKeywords: filters.exclude_keyword_ids || [],
    companies: filters.include_company_ids || [],
    excludedCompanies: filters.exclude_company_ids || [],
  };

  await Promise.all(Object.entries(idGroups).map(async ([key, ids]) => {
    const config = ENTITY_CONFIG[key];
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
    exclude_origin_countries: getPickerValues("exclude-countries"),
    include_actor_ids: state.selectedEntities.actors.map((item) => item.id),
    include_director_ids: state.selectedEntities.directors.map((item) => item.id),
    include_keyword_ids: state.selectedEntities.keywords.map((item) => item.id),
    exclude_keyword_ids: state.selectedEntities.excludedKeywords.map((item) => item.id),
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
    await setAdvancedFilters(saved.filters || {});
    setPersonalFilters(saved.personal_filters || {});
    if (saved.selected_preference_id) {
      elements.profileSelect.value = String(saved.selected_preference_id);
    }
    updateProfileButtons();
    state.discoveryMode = saved.mode || "simple";
    setWorkspaceCollapsed(Boolean(saved.filters_collapsed), false);
    return state.discoveryMode;
  } catch {
    setWorkspaceCollapsed(false, false);
    return "simple";
  }
}

function initializeCollapsibleFilters() {
  document.querySelectorAll(".filter-card").forEach((card) => {
    card.classList.add("is-collapsed");
    const heading = card.querySelector(".filter-card-heading");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "filter-card-toggle";
    button.textContent = "Open";
    button.setAttribute("aria-expanded", "false");
    button.addEventListener("click", () => {
      const collapsed = card.classList.toggle("is-collapsed");
      button.textContent = collapsed ? "Open" : "Close";
      button.setAttribute("aria-expanded", String(!collapsed));
    });
    heading.append(button);
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
  });
}

async function setAdvancedFilters(filters = {}) {
  state.profilePassthroughFilters = { ...filters };
  setPickerValues("include-genres", filters.include_genre_ids);
  setPickerValues("exclude-genres", filters.exclude_genre_ids);
  setPickerValues("include-languages", filters.include_original_languages);
  setPickerValues("exclude-languages", filters.exclude_original_languages);
  setPickerValues("include-countries", filters.include_origin_countries);
  setPickerValues("exclude-countries", filters.exclude_origin_countries);
  elements.genreLogic.value = filters.genre_logic || "or";
  elements.minimumRating.value = filters.minimum_rating ?? "";
  elements.maximumRating.value = filters.maximum_rating ?? "";
  elements.minimumVotes.value = filters.minimum_vote_count ?? "";
  elements.releaseYearFrom.value = filters.release_year_from ?? "";
  elements.releaseYearTo.value = filters.release_year_to ?? "";
  elements.sortBy.value = filters.sort_by || "popularity.desc";
  await hydrateEntitySelections(filters);
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
  elements.favoriteOnly.checked = filters.favorite_only ?? false;
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
  posterButton.append(createPoster(movie));
  posterButton.addEventListener("click", () => openMovieDetails(movieId));

  if (movie.user_data?.is_favorite) {
    const favorite = document.createElement("span");
    favorite.className = "favorite-mark";
    favorite.textContent = "♥";
    favorite.setAttribute("aria-label", "Favourite");
    posterButton.append(favorite);
  }

  const statusBadge = document.createElement("span");
  statusBadge.className = "status-badge";
  statusBadge.dataset.status = status || "untracked";
  statusBadge.textContent = status ? STATUS_LABELS[status] : "Unsorted";
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
  year.textContent = getMovieYear(movie);
  const language = document.createElement("span");
  language.textContent = getMovieLanguage(movie);
  meta.append(year, language);

  copy.append(heading, meta);
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

function setEntriesVisible(visible) {
  elements.entriesPage.classList.toggle("is-hidden", !visible);
  document.querySelector(".section-heading").classList.toggle("is-hidden", visible);
  elements.grid.classList.toggle("force-hidden", visible);
  elements.empty.classList.toggle("force-hidden", visible);
  elements.pagination.classList.toggle("force-hidden", visible);
  document.querySelector(".discovery-workspace").classList.toggle("force-hidden", visible);
}

async function loadShelf(view, page = 1) {
  if (view === "entries") {
    await loadEntries(page);
    return;
  }
  if (!(view in VIEW_COPY)) {
    return;
  }

  setEntriesVisible(false);
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
    const response = await fetchJSON(`${url}?page=${page}`);

    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = Array.isArray(response.results) ? response.results : [];
    state.searchPage = Number(response.page || page);
    state.searchTotalPages = Number(response.total_pages || 1);
    state.totalResults = Number(response.total_results || 0);
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
  setEntriesVisible(false);
  state.mode = "movie-notes";
  state.currentView = null;
  setActiveView(null);
  setModeButton(null);
  elements.simpleControls.classList.add("is-hidden");
  elements.advancedControls.classList.add("is-hidden");
  elements.pagination.classList.add("is-hidden");
  setSectionCopy({
    kicker: "Personal memory",
    title: "Movie Notes",
    description: "Movies where you saved personal thoughts and observations.",
  });
  clearNotice();
  showLoadingCards();
  elements.count.textContent = "Loading…";

  try {
    const response = await fetchJSON(`/movies/notes?page=${page}`);
    if (requestNumber !== state.requestNumber) return;
    state.movies = Array.isArray(response.results) ? response.results : [];
    state.searchPage = Number(response.page || page);
    state.searchTotalPages = Number(response.total_pages || 1);
    state.totalResults = Number(response.total_results || 0);
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

async function searchMovies(query, page = 1) {
  const cleanedQuery = query.trim();

  if (!cleanedQuery) {
    elements.query.focus();
    return;
  }

  const requestNumber = ++state.requestNumber;
  setEntriesVisible(false);
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
    kicker: "TMDB + your library",
    title: "Super Advanced results",
    description: "The same filters, with your personal statuses applied.",
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
    return;
  }

  state.discoveryMode = mode;
  setEntriesVisible(false);
  state.mode = "discovery";
  state.currentView = null;
  setActiveView(null);
  setModeButton(mode);
  setSectionCopy(DISCOVERY_COPY[mode]);
  elements.simpleControls.classList.toggle("is-hidden", mode !== "simple");
  elements.advancedControls.classList.toggle("is-hidden", mode === "simple");
  elements.personalFilters.classList.toggle("is-hidden", mode !== "super");
  elements.pagination.classList.add("is-hidden");
  scheduleSearchStateSave();

  if (runSearch || mode === "simple") {
    await runDiscoverySearch();
  }
}

function buildSearchSpec() {
  if (state.discoveryMode === "simple") {
    return { mode: "simple", filters: {} };
  }

  const spec = {
    mode: state.discoveryMode,
    filters: collectAdvancedFilters(),
  };

  if (state.discoveryMode === "super") {
    spec.personalFilters = collectPersonalFilters();
  }

  return spec;
}

async function executeDiscoverySearch(spec, page = 1) {
  const requestNumber = ++state.requestNumber;
  state.mode = "discovery";
  state.currentView = null;
  setActiveView(null);
  setModeButton(spec.mode);
  setSectionCopy(DISCOVERY_COPY[spec.mode]);
  clearNotice();
  elements.pagination.classList.add("is-hidden");
  showLoadingCards();
  elements.count.textContent = "Searching…";

  let url = "/movies/discover/advanced";
  let body = { filters: spec.filters, page };

  if (spec.mode === "super") {
    url = "/movies/discover/super-advanced";
    body = {
      filters: spec.filters,
      page,
      ...spec.personalFilters,
    };
  }

  try {
    const response = await fetchJSON(url, {
      method: "POST",
      body: JSON.stringify(body),
    });

    if (requestNumber !== state.requestNumber) {
      return;
    }

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
  updateProfileButtons();
  if (notify) {
    showNotice("All filters cleared.");
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
  closeMovieDetails();
  resetAdvancedFilters({ notify: false });
  state.selectedEntities[entityKey] = [{ id: personId, name: person.name }];
  renderSelectedEntities(entityKey);
  await setDiscoveryMode("advanced", false);
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

function renderMovieDetails(movie) {
  state.selectedMovie = movie;
  elements.dialogPoster.replaceChildren(createPoster(movie));
  elements.dialogKicker.textContent = getStatus(movie)
    ? STATUS_LABELS[getStatus(movie)]
    : "Unsorted movie";
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
  elements.notes.value = movie.user_data?.notes || "";
  elements.notesPanel.open = true;
  elements.customKeywordForm.classList.add("is-hidden");
  elements.showCustomKeyword.classList.remove("is-hidden");
  [elements.statusFeedback, elements.verdictFeedback, elements.notesFeedback,
    elements.keywordFeedback].forEach((item) => { item.textContent = ""; });
}

async function openMovieDetails(movieId) {
  state.selectedMovie = null;
  state.previousScrollPosition = window.scrollY;
  elements.shell.classList.add("is-hidden");
  elements.detailPage.classList.remove("is-hidden");
  elements.dialogContent.classList.add("is-hidden");
  elements.dialogLoading.classList.remove("is-hidden");
  elements.dialogLoading.textContent = "Loading movie details…";
  window.scrollTo({ top: 0, behavior: "auto" });

  try {
    const movie = await fetchJSON(`/movies/${movieId}`);
    renderMovieDetails(movie);
    elements.dialogLoading.classList.add("is-hidden");
    elements.dialogContent.classList.remove("is-hidden");
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
      item.textContent = match[1];
      list.append(item);
      return;
    }
    list = null;
    if (!line.trim()) return;
    const paragraph = document.createElement("p");
    paragraph.textContent = line;
    container.append(paragraph);
  });
}

function formatEntryDate(value) {
  const date = new Date(`${String(value).replace(" ", "T")}Z`);
  return Number.isNaN(date.getTime())
    ? String(value || "")
    : date.toLocaleDateString(undefined, {
      year: "numeric", month: "short", day: "numeric",
    });
}

function renderEntries(entries) {
  elements.entryList.replaceChildren();
  if (!entries.length) {
    const empty = document.createElement("div");
    empty.className = "entry-empty";
    empty.textContent = "No notes or links match this view.";
    elements.entryList.append(empty);
    return;
  }
  entries.forEach((entry) => {
    const article = document.createElement("article");
    article.className = "entry-card";
    const header = document.createElement("header");
    const heading = document.createElement("div");
    const type = document.createElement("span");
    const title = document.createElement("h3");
    const date = document.createElement("time");
    type.className = "entry-type";
    type.textContent = entry.entry_type;
    title.textContent = entry.title;
    date.textContent = formatEntryDate(entry.created_at);
    heading.append(type, title, date);
    const actions = document.createElement("div");
    const edit = document.createElement("button");
    const remove = document.createElement("button");
    edit.type = remove.type = "button";
    edit.textContent = "Edit";
    remove.textContent = "Delete";
    remove.className = "danger-button";
    edit.addEventListener("click", () => openEntryDialog(entry));
    remove.addEventListener("click", async () => {
      if (!window.confirm(`Delete “${entry.title}”?`)) return;
      await fetchJSON(`/entries/${entry.entry_id}`, { method: "DELETE" });
      showNotice(`Moved “${entry.title}” to trash.`);
      await loadEntries(state.entryPage);
    });
    actions.append(edit, remove);
    header.append(heading, actions);
    const body = document.createElement("div");
    body.className = "entry-body";
    appendEntryBody(body, entry.body);
    article.append(header, body);
    if (entry.url) {
      const links = document.createElement("div");
      links.className = "entry-links";
      entry.url.split(/\r?\n/).map((url) => url.trim()).filter(Boolean).forEach((raw) => {
        const anchor = document.createElement("a");
        anchor.href = /^https?:\/\//i.test(raw) ? raw : `https://${raw}`;
        anchor.textContent = raw;
        anchor.target = "_blank";
        anchor.rel = "noreferrer";
        links.append(anchor);
      });
      article.append(links);
    }
    elements.entryList.append(article);
  });
}

async function loadEntries(page = 1) {
  state.mode = "entries";
  state.currentView = "entries";
  state.entryPage = page;
  setActiveView("entries");
  elements.mobileView.value = "entries";
  setEntriesVisible(true);
  clearNotice();
  elements.entryList.innerHTML = '<div class="entry-empty">Loading your notebook…</div>';
  const parameters = new URLSearchParams({ page: String(page) });
  const query = elements.entryQuery.value.trim();
  if (query) parameters.set("query", query);
  if (elements.entryTypeFilter.value) parameters.set("entry_type", elements.entryTypeFilter.value);
  if (elements.entryYearFilter.value) parameters.set("year", elements.entryYearFilter.value);
  if (elements.entryMonthFilter.value) parameters.set("month", elements.entryMonthFilter.value);
  try {
    const response = await fetchJSON(`/entries?${parameters}`);
    renderEntries(response.results || []);
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

function openEntryDialog(entry = null) {
  state.editingEntryId = entry?.entry_id || null;
  elements.entryForm.reset();
  elements.entryType.value = entry?.entry_type || "note";
  elements.entryTitle.value = entry?.title || "";
  elements.entryBody.value = entry?.body || "";
  elements.entryUrl.value = entry?.url || "";
  elements.entryDialogTitle.textContent = entry ? "Edit entry" : "New note or link";
  updateEntryUrlField();
  elements.entryDialog.showModal();
  elements.entryTitle.focus();
}

function updateEntryUrlField() {
  const isLink = elements.entryType.value === "link";
  elements.entryUrlField.classList.toggle("is-hidden", !isLink);
  elements.entryUrl.required = isLink;
}

async function saveEntry(event) {
  event.preventDefault();
  const editing = Boolean(state.editingEntryId);
  elements.saveEntry.disabled = true;
  elements.saveEntry.textContent = "Saving…";
  try {
    await fetchJSON(
      editing ? `/entries/${state.editingEntryId}` : "/entries",
      {
        method: editing ? "PUT" : "POST",
        body: JSON.stringify({
          entry_type: elements.entryType.value,
          title: elements.entryTitle.value,
          body: elements.entryBody.value || null,
          url: elements.entryType.value === "link" ? elements.entryUrl.value : null,
        }),
      },
    );
    elements.entryDialog.close();
    showNotice(editing ? "Entry updated." : "Entry created.");
    await loadEntries(1);
  } catch (error) {
    showNotice(error.message);
  } finally {
    elements.saveEntry.disabled = false;
    elements.saveEntry.textContent = "Save entry";
  }
}

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  searchMovies(elements.query.value);
});

elements.navLinks.forEach((button) => {
  button.addEventListener("click", () => loadShelf(button.dataset.view));
});

elements.mobileView.addEventListener("change", () => {
  loadShelf(elements.mobileView.value);
});

elements.modeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setDiscoveryMode(button.dataset.discoveryMode).catch((error) => {
      showNotice(error.message);
    });
  });
});

elements.refreshDiscovery.addEventListener("click", () => {
  runDiscoverySearch();
});

elements.advancedForm.addEventListener("submit", (event) => {
  event.preventDefault();
  runDiscoverySearch();
});

elements.resetFilters.addEventListener("click", resetAdvancedFilters);

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
  closeMovieDetails();
});

elements.saveStatus.addEventListener("click", saveSelectedStatus);
elements.favoriteButton.addEventListener("click", toggleSelectedFavorite);
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
elements.entryFilters.addEventListener("submit", (event) => {
  event.preventDefault();
  loadEntries(1);
});
elements.clearEntryFilters.addEventListener("click", () => {
  elements.entryFilters.reset();
  loadEntries(1);
});

elements.footerViews.forEach((button) => {
  button.addEventListener("click", () => {
    const view = button.dataset.footerView;
    if (view === "movie-notes") {
      loadMovieNotes(1);
      return;
    }
    elements.entryFilters.reset();
    elements.entryTypeFilter.value = view === "links" ? "link" : "note";
    loadEntries(1);
  });
});

async function initializeApp() {
  initializePickers();
  initializeEntityPickers();
  initializeCollapsibleFilters();
  initializeOutsideClosing();
  const currentYear = new Date().getFullYear();
  for (let year = currentYear; year >= currentYear - 15; year -= 1) {
    const option = document.createElement("option");
    option.value = String(year);
    option.textContent = String(year);
    elements.entryYearFilter.append(option);
  }
  await loadProfiles();
  const restoredMode = await restoreSearchState();
  await setDiscoveryMode(restoredMode, true);
}

initializeApp().catch((error) => showNotice(error.message));
