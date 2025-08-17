from pathlib import Path
import pytest

from src.data_objects import Series
from src.data_objects.series import Season


@pytest.fixture
def dummy_files(tmp_path: Path) -> tuple[list[Path], list[Path]]:

    dummy_dirs: list[Path] = []
    dummy_eps: list[Path] = []
    for dir_num in range(0, 4):
        dummy_dir: Path = tmp_path / f"dummy_extraction_{dir_num}"
        dummy_dir.mkdir()
        dummy_dirs.append(dummy_dir)

        for episode_num in range(0, 3):
            dummy_ep: Path = dummy_dir / f"dummy_episode_{episode_num}.mkv"
            dummy_ep.touch()
            dummy_eps.append(dummy_ep)

    return dummy_dirs, dummy_eps


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
            output_dir=tmp_path,
            title="Series Output",
            production_year=1969,
            episode_to_season_map=dummy_series_map,
            seasons={}
        )

        assert series.title == "Series Output"
        assert series.production_year == 1969
        assert series._episode_to_season_map == dummy_series_map
        assert series.series_dir == tmp_path / "Series Output (1969)"


class TestIncorporate:

    def test_it_incorporates_a_fresh_directory(
        self,
        tmp_path: Path,
        dummy_series_map: dict[int, tuple[int, int]],
        dummy_files: tuple[list[Path], list[Path]],
    ):
        dummy_dirs, dummy_eps = dummy_files

        series: Series = Series(
            output_dir=tmp_path,
            title="Series Output",
            production_year=1969,
            episode_to_season_map=dummy_series_map,
            seasons={}
        )
        series.incorporate(dummy_dirs)

        expected: dict[int, Season] = {
            1: Season(1, {ep_num + 1: ep_path for ep_num, ep_path in enumerate(dummy_eps[0:7])}),
            2: Season(2, {ep_num + 1: ep_path for ep_num, ep_path in enumerate(dummy_eps[7:9])}),
            3: Season(3, {ep_num + 1: ep_path for ep_num, ep_path in enumerate(dummy_eps[9:15])}),
        }

        assert series._seasons == expected
