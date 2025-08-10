from collections import namedtuple
from pathlib import Path


from .extractor import Extractor
from .season import Season
from ..protocols import SeriesContextProtocol, SeasonProtocol


EpisodeRange = namedtuple("EpisodeRange", ["first_episode", "last_episode"])


class Series(SeriesContextProtocol):
    __slots__ = (
        # Path to the directory that contains configuration information and the directories that contain episodes
        "_series_dir",
        # Title of the series
        "_title",
        # Year the series was first aired
        "_production_year",
        # Dictionary that maps a production number range to a season
        "_season_map",
        # Seasons within the series
        "_season_list",
        # Sub-directories that contain episodes
        "_episode_dirs",
        # The unique identifier for the series on TVDB
        "_tvdb_id",
    )

    def __init__(
        self,
        *,
        save_dir: Path,
        title: str,
        production_year: int,
        tvdb_id: int | None,
        season_map: dict[int, EpisodeRange],
    ):
        self._title: str = title
        self._production_year: int = production_year
        self._tvdb_id: int | None = tvdb_id
        self._series_dir: Path = save_dir / f"{title} ({production_year})"

        self._season_map: dict[int, EpisodeRange] = season_map

        self._season_list: dict[int, SeasonProtocol] = self._initialize_seasons(self._series_dir)

    # Property Methods

    @property
    def title(self) -> str:
        return self._title

    @property
    def production_year(self) -> int:
        return self._production_year

    # Public Methods

    def incorporate(self, paths: list[Path]) -> "Series":
        extractor: Extractor = Extractor(paths)

        for episode_path, production_number in extractor.get_all_videos():
            season_number, episode_number = self.get_season_and_episode_numbers(production_number)
            self.add_to_season(episode_path, season_number, episode_number)

        return self

    def add_to_season(
        self,
        episode_path: Path,
        season_number: int,
        episode_number: int,
    ) -> None:
        season_has_map: bool = season_number in self._season_map
        if not season_has_map:
            raise ValueError(f"Season {season_number} is not mapped in season map.")

        if season_number not in self._season_list:
            self._season_list[season_number] = Season(self._series_dir, season_number)

        specified_season: SeasonProtocol = self._season_list.get(season_number)
        specified_season.add_episode(episode_path, episode_number)

    def get_season_and_episode_numbers(self, production_number: int) -> tuple[int, int]:
        for season_number, episode_range in self._season_map.items():
            first_episode, last_episode = episode_range
            if first_episode <= production_number <= last_episode:
                episode_number: int = production_number - episode_range[0] + 1
                return season_number, episode_number

        raise ValueError(f"Production number '{production_number}' is not in season map.")

    # Private Methods

    @staticmethod
    def _initialize_seasons(series_dir: Path) -> dict[int, SeasonProtocol]:

        # TODO: Flesh this out with actual logic that will incorporate seeason directories if they already exist
        return {}
