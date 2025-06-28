
from pathlib import Path
from ..protocols import SeriesContextProtocol


class Episode:
    __slots__ = (
        # Path to the movie file
        "_path",

        # Title of the series
        "_series_context",

        # Season number the episode belongs to
        "_season_number",

        # What number this episode is within the season
        "_episode_number",

        # What number the epsiode is relative to other episodes in the directory
        "_local_number",
    )

    # TODO: add extra meta data like edition, episode titles, etc

    def __init__(
        self,
        *,
        path: Path,
        series_context: SeriesContextProtocol,
        season_number: int | None,
        episode_number: int | None,
        local_number: int | None,
    ):

        self._path: Path = path
        self._series_context: SeriesContextProtocol = series_context
        self._season_number: int | None = season_number
        self._episode_number: int | None = episode_number
        self._local_number: int | None = local_number

    def copy_to(self, dir: str | Path) -> "Episode":
        ...
