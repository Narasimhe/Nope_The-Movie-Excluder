from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FilterLogic(str, Enum):
    AND = "and"
    OR = "or"


VALID_SORT_OPTIONS = frozenset(
    {
        "original_title.asc",
        "original_title.desc",
        "popularity.asc",
        "popularity.desc",
        "primary_release_date.asc",
        "primary_release_date.desc",
        "revenue.asc",
        "revenue.desc",
        "title.asc",
        "title.desc",
        "vote_average.asc",
        "vote_average.desc",
        "vote_count.asc",
        "vote_count.desc",
    }
)


@dataclass
class AdvancedMovieFilters:
    include_genre_ids: list[int] = field(default_factory=list)
    exclude_genre_ids: list[int] = field(default_factory=list)
    genre_logic: str | FilterLogic = FilterLogic.OR

    include_keyword_ids: list[int] = field(default_factory=list)
    exclude_keyword_ids: list[int] = field(default_factory=list)
    keyword_logic: str | FilterLogic = FilterLogic.OR

    include_original_languages: list[str] = field(default_factory=list)
    exclude_original_languages: list[str] = field(default_factory=list)

    include_origin_countries: list[str] = field(default_factory=list)
    exclude_origin_countries: list[str] = field(default_factory=list)
    country_logic: str | FilterLogic = FilterLogic.OR

    minimum_rating: float | None = None
    maximum_rating: float | None = None
    minimum_vote_count: int | None = None

    release_year_from: int | None = None
    release_year_to: int | None = None
    runtime_min: int | None = None
    runtime_max: int | None = None

    sort_by: str = "popularity.desc"
    include_adult: bool = False

    def __post_init__(self) -> None:
        self.genre_logic = self._normalize_logic(
            self.genre_logic,
            "genre_logic",
        )
        self.keyword_logic = self._normalize_logic(
            self.keyword_logic,
            "keyword_logic",
        )
        self.country_logic = self._normalize_logic(
            self.country_logic,
            "country_logic",
        )

        self.include_genre_ids = self._normalize_ids(
            self.include_genre_ids,
            "include_genre_ids",
        )
        self.exclude_genre_ids = self._normalize_ids(
            self.exclude_genre_ids,
            "exclude_genre_ids",
        )
        self.include_keyword_ids = self._normalize_ids(
            self.include_keyword_ids,
            "include_keyword_ids",
        )
        self.exclude_keyword_ids = self._normalize_ids(
            self.exclude_keyword_ids,
            "exclude_keyword_ids",
        )

        self.include_original_languages = self._normalize_codes(
            self.include_original_languages,
            "include_original_languages",
            uppercase=False,
        )
        self.exclude_original_languages = self._normalize_codes(
            self.exclude_original_languages,
            "exclude_original_languages",
            uppercase=False,
        )
        self.include_origin_countries = self._normalize_codes(
            self.include_origin_countries,
            "include_origin_countries",
            uppercase=True,
        )
        self.exclude_origin_countries = self._normalize_codes(
            self.exclude_origin_countries,
            "exclude_origin_countries",
            uppercase=True,
        )

        self._validate_no_overlap(
            self.include_genre_ids,
            self.exclude_genre_ids,
            "genre",
        )
        self._validate_no_overlap(
            self.include_keyword_ids,
            self.exclude_keyword_ids,
            "keyword",
        )
        self._validate_no_overlap(
            self.include_original_languages,
            self.exclude_original_languages,
            "original language",
        )
        self._validate_no_overlap(
            self.include_origin_countries,
            self.exclude_origin_countries,
            "origin country",
        )

        self._validate_range(
            self.minimum_rating,
            self.maximum_rating,
            "rating",
            minimum=0,
            maximum=10,
        )
        self._validate_non_negative(
            self.minimum_vote_count,
            "minimum_vote_count",
        )
        self._validate_range(
            self.release_year_from,
            self.release_year_to,
            "release year",
            minimum=1,
            maximum=9999,
        )
        self._validate_range(
            self.runtime_min,
            self.runtime_max,
            "runtime",
            minimum=0,
        )

        if self.sort_by not in VALID_SORT_OPTIONS:
            raise ValueError(
                f"Invalid sort option: {self.sort_by!r}."
            )

    def to_tmdb_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {
            "include_adult": self.include_adult,
            "sort_by": self.sort_by,
        }

        if self.include_genre_ids:
            params["with_genres"] = self._join_ids(
                self.include_genre_ids,
                self.genre_logic,
            )
        if self.exclude_genre_ids:
            params["without_genres"] = "|".join(
                str(value)
                for value in self.exclude_genre_ids
            )
        if self.include_keyword_ids:
            params["with_keywords"] = self._join_ids(
                self.include_keyword_ids,
                self.keyword_logic,
            )
        if self.exclude_keyword_ids:
            params["without_keywords"] = "|".join(
                str(value)
                for value in self.exclude_keyword_ids
            )

        # TMDB accepts one original-language or origin-country value
        # directly. Multiple allowed values are handled locally.
        if len(self.include_original_languages) == 1:
            params["with_original_language"] = (
                self.include_original_languages[0]
            )
        if len(self.include_origin_countries) == 1:
            params["with_origin_country"] = (
                self.include_origin_countries[0]
            )

        if self.minimum_rating is not None:
            params["vote_average.gte"] = self.minimum_rating
        if self.maximum_rating is not None:
            params["vote_average.lte"] = self.maximum_rating
        if self.minimum_vote_count is not None:
            params["vote_count.gte"] = self.minimum_vote_count

        if self.release_year_from is not None:
            params["primary_release_date.gte"] = (
                f"{self.release_year_from:04d}-01-01"
            )
        if self.release_year_to is not None:
            params["primary_release_date.lte"] = (
                f"{self.release_year_to:04d}-12-31"
            )
        if self.runtime_min is not None:
            params["with_runtime.gte"] = self.runtime_min
        if self.runtime_max is not None:
            params["with_runtime.lte"] = self.runtime_max

        return params

    def matches_local_rules(self, movie: dict[str, Any]) -> bool:
        original_language = (
            str(movie.get("original_language") or "").lower()
        )

        if (
            self.include_original_languages
            and original_language
            not in self.include_original_languages
        ):
            return False

        if original_language in self.exclude_original_languages:
            return False

        country_codes = self._movie_country_codes(movie)
        has_country_rules = bool(
            self.include_origin_countries
            or self.exclude_origin_countries
        )

        if has_country_rules and country_codes is None:
            return False

        if country_codes is not None:
            included_countries = set(self.include_origin_countries)
            excluded_countries = set(self.exclude_origin_countries)

            if included_countries:
                if self.country_logic == FilterLogic.AND:
                    if not included_countries.issubset(country_codes):
                        return False
                elif not included_countries.intersection(country_codes):
                    return False

            if excluded_countries.intersection(country_codes):
                return False

        return True

    def apply_local_rules(
        self,
        movies: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        return [
            movie
            for movie in movies
            if self.matches_local_rules(movie)
        ]

    def needs_country_details(self, movie: dict[str, Any]) -> bool:
        has_country_rules = bool(
            self.include_origin_countries
            or self.exclude_origin_countries
        )
        return (
            has_country_rules
            and self._movie_country_codes(movie) is None
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "include_genre_ids": list(self.include_genre_ids),
            "exclude_genre_ids": list(self.exclude_genre_ids),
            "genre_logic": self.genre_logic.value,
            "include_keyword_ids": list(self.include_keyword_ids),
            "exclude_keyword_ids": list(self.exclude_keyword_ids),
            "keyword_logic": self.keyword_logic.value,
            "include_original_languages": list(
                self.include_original_languages
            ),
            "exclude_original_languages": list(
                self.exclude_original_languages
            ),
            "include_origin_countries": list(
                self.include_origin_countries
            ),
            "exclude_origin_countries": list(
                self.exclude_origin_countries
            ),
            "country_logic": self.country_logic.value,
            "minimum_rating": self.minimum_rating,
            "maximum_rating": self.maximum_rating,
            "minimum_vote_count": self.minimum_vote_count,
            "release_year_from": self.release_year_from,
            "release_year_to": self.release_year_to,
            "runtime_min": self.runtime_min,
            "runtime_max": self.runtime_max,
            "sort_by": self.sort_by,
            "include_adult": self.include_adult,
        }

    @staticmethod
    def _normalize_logic(
        value: str | FilterLogic,
        field_name: str,
    ) -> FilterLogic:
        if isinstance(value, FilterLogic):
            return value

        try:
            return FilterLogic(str(value).lower())
        except ValueError as error:
            raise ValueError(
                f"{field_name} must be 'and' or 'or'."
            ) from error

    @staticmethod
    def _normalize_ids(
        values: list[int],
        field_name: str,
    ) -> list[int]:
        normalized = []

        for value in values:
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or value <= 0
            ):
                raise ValueError(
                    f"{field_name} must contain positive integers."
                )

            if value not in normalized:
                normalized.append(value)

        return normalized

    @staticmethod
    def _normalize_codes(
        values: list[str],
        field_name: str,
        *,
        uppercase: bool,
    ) -> list[str]:
        normalized = []

        for value in values:
            code = str(value).strip()

            if len(code) != 2 or not code.isalpha():
                raise ValueError(
                    f"{field_name} must contain two-letter codes."
                )

            code = code.upper() if uppercase else code.lower()

            if code not in normalized:
                normalized.append(code)

        return normalized

    @staticmethod
    def _validate_no_overlap(
        included: list[Any],
        excluded: list[Any],
        label: str,
    ) -> None:
        overlap = set(included).intersection(excluded)

        if overlap:
            raise ValueError(
                f"The same {label} cannot be both included and excluded."
            )

    @staticmethod
    def _validate_non_negative(
        value: int | None,
        field_name: str,
    ) -> None:
        if value is not None and value < 0:
            raise ValueError(f"{field_name} cannot be negative.")

    @staticmethod
    def _validate_range(
        lower: float | int | None,
        upper: float | int | None,
        label: str,
        *,
        minimum: float | int | None = None,
        maximum: float | int | None = None,
    ) -> None:
        for value in (lower, upper):
            if value is None:
                continue
            if minimum is not None and value < minimum:
                raise ValueError(
                    f"{label} cannot be below {minimum}."
                )
            if maximum is not None and value > maximum:
                raise ValueError(
                    f"{label} cannot be above {maximum}."
                )

        if (
            lower is not None
            and upper is not None
            and lower > upper
        ):
            raise ValueError(
                f"{label} minimum cannot exceed its maximum."
            )

    @staticmethod
    def _join_ids(
        values: list[int],
        logic: FilterLogic,
    ) -> str:
        separator = "," if logic == FilterLogic.AND else "|"
        return separator.join(str(value) for value in values)

    @staticmethod
    def _movie_country_codes(
        movie: dict[str, Any],
    ) -> set[str] | None:
        country_fields = (
            "origin_country",
            "origin_countries",
            "production_countries",
        )
        found_country_field = any(
            field_name in movie
            for field_name in country_fields
        )

        if not found_country_field:
            return None

        country_codes = set()

        for field_name in country_fields:
            raw_countries = movie.get(field_name) or []

            for country in raw_countries:
                if isinstance(country, dict):
                    code = country.get("iso_3166_1")
                else:
                    code = country

                if code:
                    country_codes.add(str(code).upper())

        return country_codes
