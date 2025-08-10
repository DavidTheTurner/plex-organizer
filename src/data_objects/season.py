

from pathlib import Path
from src.protocols.season_protocol import SeasonProtocol


class Season(SeasonProtocol):
    __slots__ = (
        "_season_path",
        "_season_number",
        "_episode_list",
    )

    def __init__(self, series_path: Path, season_number: int, episode_list: dict[int, Path] = {}):
        self._season_path: Path = series_path / f"Season {season_number:02d}"
        self._season_number: int = season_number
        self._episode_list: dict[int, Path] = episode_list

    def add_episode(self, episode_path: Path, episode_number: int) -> "Season":
        self._episode_list[episode_number] = episode_path
        return self
