from pathlib import Path

from ..data_objects import Extractor
from ..protocols import SeriesContextProtocol, SeasonProtocol


class Series(SeriesContextProtocol):
    __slots__ = (
        # Path to the directory that contains configuration
        # information and the directories that contain
        # episodes
        "_series_dir",
        # Title of the series
        "_title",
        # Year the series was first aired
        "_production_year",
        # Dictionary that maps a production number range
        # to a season
        "_season_map",
        # Seasons within the series
        "_season_dirs",
        # Sub-directories that contain episodes
        "_episode_dirs",
        # The unique identifier for the series on
        # TVDB
        "_tvdb_id",
    )

    def __init__(
        self,
        *,
        series_dir: Path,
        title: str,
        production_year: int,
        tvdb_id: int | None,
        season_map: dict[tuple[int, int], int],
        season_list: list[SeasonProtocol],
    ):
        self._series_dir: Path = series_dir
        self._title: str = title
        self._production_year: int = production_year
        self._season_map: dict[int, tuple[int, int]] = season_map
        self._season_list: list[SeasonProtocol] = season_list
        self._tvdb_id: int | None = tvdb_id

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
        pass

    def get_season_and_episode_numbers(self, production_number: int) -> tuple[int, int]:
        for season_number, episode_range in self._season_map.items():
            if episode_range[0] <= production_number <= episode_range[1]:
                episode_number: int = production_number - episode_range[0] + 1
                return season_number, episode_number

        raise ValueError(f"Production number '{production_number}' is not in season map.")
