from pathlib import Path
import pytest

from src.data_objects import Series


@pytest.fixture
def dummy_directories(tmp_path: Path) -> list[Path]:

    dummy_dirs: list[Path] = []
    for dir_num in range(0, 4):
        dummy_dir: Path = tmp_path / f"dummy_extraction_{dir_num}"
        dummy_dir.mkdir()
        dummy_dirs.append(dummy_dir)

        for episode_num in range(0, 3):
            dummy_ep: Path = dummy_dir / f"dummy_episode_{episode_num}.mkv"
            dummy_ep.touch()

    return dummy_dirs


@pytest.fixture
def dummy_series_map() -> dict[int, tuple[int, int]]:
    return {
        1: (1, 7),
        2: (8, 9),
        3: (10, 15),
    }


class TestConstruction:

    def test_it_creates_series(self, dummy_series_map: dict[int, tuple[int, int]], tmp_path: Path):
        series: Series = Series(
            series_dir=tmp_path / "Series Output (1969)",
            title="Series Output",
            production_year=1969,
            episode_to_season_map=dummy_series_map,
            seasons={}
        )

        assert series.title == "Series Output"
        assert series.production_year == 1969
        assert series._episode_to_season_map == dummy_series_map


class TestIncorporate:

    def test_it_incorporates_a_fresh_directory(
        self,
        tmp_path: Path,
        dummy_series_map: dict[int, tuple[int, int]],
        dummy_directories: Path,
    ):
        series: Series = Series(
            series_dir=tmp_path / "Series Output (1969)",
            title="Series Output",
            production_year=1969,
            episode_to_season_map=dummy_series_map,
            seasons={}
        )
        series.incorporate(dummy_directories)

        print(series._seasons)
