

from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class VideoProtocol(Protocol):

    @abstractmethod
    @property
    def order_number(self) -> int:
        pass

    @abstractmethod
    @property
    def video_path(self) -> Path:
        pass
