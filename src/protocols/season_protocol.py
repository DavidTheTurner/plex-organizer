from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class SeasonProtocol(Protocol):

    @abstractmethod
    def add_episode(self, episode_path: Path, episode_number: int) -> "SeasonProtocol":
        pass
