

from pathlib import Path
import pytest
from src.data_objects.extractor import Extractor


@pytest.fixture
def dummy_dirs(tmp_path) -> list[Path]:

    dummy1: Path = tmp_path / "JoJo's Bizzare Adventure - 1"
    dummy1.mkdir()
    for i in range(5):
        (dummy1 / f"Jojo - {i}.mkv").touch()

    dummy2: Path = tmp_path / "JoJo's Bizzare Adventure - 2"
    dummy2.mkdir()
    for i in range(3):
        (dummy2 / f"Jojo - {i}.mkv").touch()

    return [dummy2, dummy1]


class TestGetAllVideos:

    def test_it_gets_videos(self, dummy_dirs: list[Path]):
        extractor: Extractor = Extractor(
            extraction_paths=dummy_dirs
        )

        results = list(extractor.get_all_videos())
        print(results)
