from itertools import chain
import logging

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator

from ..utils import TRAILING_NUMBER, sort_by_trailing_number
from ..protocols import ExtractorProtocol

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ExtractedVideo:
    path: Path
    extraction_number: int


class Extractor(ExtractorProtocol):
    __slots__ = (
        "_extraction_directories",
    )

    def __init__(
        self,
        *,
        extraction_paths: list[Path],
    ):
        self._validate_extraction_paths(extraction_paths)
        self._extraction_directories: list[Path] = sort_by_trailing_number(extraction_paths)

    def get_all_videos(self) -> Generator[tuple[Path, int], Any, None]:

        extracted_content: list[Path] = chain.from_iterable([
            sort_by_trailing_number(dir.iterdir())
            for dir
            in self._extraction_directories
        ])

        extraction_number: int = 1
        for video_file in extracted_content:
            if video_file.is_dir():
                logger.warning(
                    f"File '{video_file.name}' in '{str(video_file.parent)}' is a directory and will be ignored."
                )
                continue

            yield video_file, extraction_number
            extraction_number += 1

        return

    @staticmethod
    def _validate_extraction_paths(dirs: list[Path]):

        if not all([maybe_dir.is_dir() for maybe_dir in dirs]):
            raise ValueError("Not all provided paths are directories.")
        if not all([TRAILING_NUMBER.search(maybe_numbered.name) for maybe_numbered in dirs]):
            raise ValueError("Not all provided directories are numbered.")

        indicies: list[int] = [int(TRAILING_NUMBER.search(dir.name).group(1)) for dir in dirs]
        if len(set(indicies)) != len(indicies):
            raise ValueError("Not all directories are uniquely numbered.")
