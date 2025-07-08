from pathlib import Path
from ..protocols import SeriesContextProtocol, SeasonProtocol, EpisodeProtocol


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
        self._season_map: dict[tuple[int, int], int] = season_map
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

    def add_to_season(
        self,
        *,
        episode: EpisodeProtocol,
        season_number: int,
    ) -> None:
        pass
