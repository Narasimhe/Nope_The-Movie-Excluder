const IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500";

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
  dialog: document.querySelector("#movie-dialog"),
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
  statusSelect: document.querySelector("#status-select"),
  saveStatus: document.querySelector("#save-status"),
  favoriteButton: document.querySelector("#favorite-button"),
  favoriteLabel: document.querySelector("#favorite-label"),
  favoriteHelp: document.querySelector("#favorite-help"),
};

const state = {
  movies: [],
  mode: "shelf",
  currentView: "new_discovery",
  selectedMovie: null,
  requestNumber: 0,
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
  return movie.original_language
    ? String(movie.original_language).toUpperCase()
    : "—";
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

function renderMovies(movies, emptyContext = "library") {
  elements.grid.replaceChildren();
  elements.count.textContent = `${movies.length} ${
    movies.length === 1 ? "movie" : "movies"
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

async function loadShelf(view) {
  if (!(view in VIEW_COPY)) {
    return;
  }

  const requestNumber = ++state.requestNumber;
  state.mode = "shelf";
  state.currentView = view;
  setActiveView(view);
  setSectionCopy(VIEW_COPY[view]);
  clearNotice();
  showLoadingCards();
  elements.count.textContent = "Loading…";

  const url =
    view === "favorites"
      ? "/movies/favorites"
      : `/movies/status/${encodeURIComponent(view)}`;

  try {
    const movies = await fetchJSON(url);

    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = Array.isArray(movies) ? movies : [];
    renderMovies(state.movies);
  } catch (error) {
    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = [];
    renderMovies([]);
    showNotice(error.message);
  }
}

async function searchMovies(query) {
  const cleanedQuery = query.trim();

  if (!cleanedQuery) {
    elements.query.focus();
    return;
  }

  const requestNumber = ++state.requestNumber;
  state.mode = "search";
  state.currentView = null;
  setActiveView(null);
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
    const movies = await fetchJSON(
      `/movies/search?query=${encodeURIComponent(cleanedQuery)}`,
    );

    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = Array.isArray(movies) ? movies : [];
    renderMovies(state.movies, "search");
  } catch (error) {
    if (requestNumber !== state.requestNumber) {
      return;
    }

    state.movies = [];
    renderMovies([], "search");
    showNotice(error.message);
  }
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

function renderPersonalControls(movie) {
  const userData = movie.user_data || null;
  const status = userData?.status || "new_discovery";
  const canFavorite = status === "watched" || status === "rewatch";
  const isFavorite = Boolean(userData?.is_favorite);

  elements.statusSelect.value = status;
  elements.favoriteButton.disabled = !canFavorite;
  elements.favoriteButton.classList.toggle("is-favorite", isFavorite);
  elements.favoriteLabel.textContent = isFavorite
    ? "Remove from favourites"
    : "Add to favourites";
  elements.favoriteHelp.textContent = canFavorite
    ? "Favourites remain a personal subset of watched movies."
    : "Mark this movie as watched or rewatch before favouriting it.";
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
  renderTags(elements.dialogKeywords, movie.keywords, true);
  renderPersonalControls(movie);
}

async function openMovieDetails(movieId) {
  state.selectedMovie = null;
  elements.dialogContent.classList.add("is-hidden");
  elements.dialogLoading.classList.remove("is-hidden");
  elements.dialogLoading.textContent = "Loading movie details…";

  if (!elements.dialog.open) {
    elements.dialog.showModal();
  }

  try {
    const movie = await fetchJSON(`/movies/${movieId}`);
    renderMovieDetails(movie);
    elements.dialogLoading.classList.add("is-hidden");
    elements.dialogContent.classList.remove("is-hidden");
  } catch (error) {
    elements.dialogLoading.textContent = error.message;
  }
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
  const originalLabel = elements.saveStatus.textContent;
  elements.saveStatus.disabled = true;
  elements.saveStatus.textContent = "Saving…";

  try {
    const response = await fetchJSON(`/movies/${movieId}/status`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    });
    updateVisibleMovie(response.user_movie_data);
    renderPersonalControls(state.selectedMovie);
    elements.dialogKicker.textContent = STATUS_LABELS[status];

    if (state.mode === "shelf" && state.currentView) {
      await loadShelf(state.currentView);
    } else {
      renderMovies(state.movies, "search");
    }
  } catch (error) {
    showNotice(error.message);
  } finally {
    elements.saveStatus.disabled = false;
    elements.saveStatus.textContent = originalLabel;
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

    if (state.mode === "shelf" && state.currentView === "favorites") {
      await loadShelf("favorites");
    } else {
      renderMovies(state.movies, state.mode);
    }
  } catch (error) {
    showNotice(error.message);
    renderPersonalControls(state.selectedMovie);
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

elements.emptySearchButton.addEventListener("click", () => {
  elements.query.focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

elements.dialogClose.addEventListener("click", () => {
  elements.dialog.close();
});

elements.dialog.addEventListener("click", (event) => {
  if (event.target === elements.dialog) {
    elements.dialog.close();
  }
});

elements.saveStatus.addEventListener("click", saveSelectedStatus);
elements.favoriteButton.addEventListener("click", toggleSelectedFavorite);

loadShelf("new_discovery");
