

from abc import abstractmethod
from typing import Protocol

from .video_protocol import VideoProtocol


class ExtractorProtocol(Protocol):

    @abstractmethod
    def get_all_videos(self) -> list[VideoProtocol]:
        pass
