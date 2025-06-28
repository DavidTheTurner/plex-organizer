from abc import abstractmethod
from typing import Protocol


class SeriesContextProtocol(Protocol):

    @abstractmethod
    def add_to_season(self, *, episode, season_num: int) -> None:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def production_year(self) -> int:
        pass
