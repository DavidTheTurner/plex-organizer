

from abc import abstractmethod
from typing import Protocol

from .video_protocol import VideoProtocol


class ExtractionDirectoryProtocol(Protocol):

    @abstractmethod
    @property
    def videos_contained(self) -> int:
        pass

    @abstractmethod
    def get_videos(self) -> list[VideoProtocol]:
        pass
