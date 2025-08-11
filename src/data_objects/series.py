from dataclasses import dataclass
from pathlib import Path

from ..data_objects import Extractor
from ..protocols import SeriesContextProtocol


@dataclass(slots=True)
class Season:
    season_dir: Path
    episodes: dict[int, Path]

    def __init__(self, season_number):
        self.season_dir = f"Season {season_number:02d}"
        self.episodes = {}


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
        "_episode_to_season_map",
        # Dictionary of seasons within a series
        "_seasons",
    )

    def __init__(
        self,
        *,
        series_dir: Path,
        title: str,
        production_year: int,
        episode_to_season_map: dict[tuple[int, int], int],
        seasons: dict[int, Season],
    ):
        self._series_dir: Path = series_dir
        self._title: str = title
        self._production_year: int = production_year
        self._episode_to_season_map: dict[int, tuple[int, int]] = episode_to_season_map
        self._seasons: dict[int, Season] = seasons

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

        desired_season: Season | None = self._seasons.get(season_number)
        if desired_season is None:
            new_season: Season = Season(season_number)

            self._seasons[season_number] = new_season
            desired_season = new_season

        desired_season.episodes[episode_number] = episode_path

    def get_season_and_episode_numbers(self, production_number: int) -> tuple[int, int]:
        """
        Iterates through the season map to find the corresponding season and calculates the episode number
        within the season.
        """
        for season_number, episode_range in self._episode_to_season_map.items():
            if episode_range[0] <= production_number <= episode_range[1]:
                episode_number: int = production_number - episode_range[0] + 1
                return season_number, episode_number

        raise ValueError(f"Production number '{production_number}' is not in season map.")
