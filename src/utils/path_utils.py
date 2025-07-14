

from pathlib import Path
import re
from typing import Iterable


TRAILING_NUMBER: re.Pattern = re.compile(r"(\d+)$")


def sort_by_trailing_number(paths: Iterable[Path]) -> list[Path]:
    sorted_paths: list[Path] = sorted(paths, key=get_trailing_number)
    return sorted_paths


def get_trailing_number(path: Path) -> int:
    trailing_number: int = int(TRAILING_NUMBER.search(path.stem).group(1))
    return trailing_number
