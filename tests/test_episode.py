

from pathlib import Path

import pytest

from data_objects.episode import Episode, try_parse_file_name


class TestEpisode:

    def test_it_initializes_successfully(self):

        ep = Episode(
            path="/nowherel.mkv"
        )


class TestTryParseFileName:

    def test_it_parses_normal_plex_format(self):

        dummy_episode: Path = Path("The Fist Of The North Star (1993) - s01e22.mkv")
        parse_results: dict = try_parse_file_name(dummy_episode)
        expected: dict = {
            "series_name": "The Fist Of The North Star",
            "production_year": 1993,
            "season_number": 1,
            "episode_number": 22,
        }

        assert parse_results["season_number"] == expected["season_number"]
        assert parse_results["episode_number"] == expected["episode_number"]
    
    @pytest.mark.parametrize(
        "series_name", [
            "Speed Racer (1967) - s01e02.mkv",
            "Speed Racer (1967) - s01E02.mkv",
            "Speed Racer (1967) - S01e02.mkv",
            "Speed Racer (1967) - S01E02.mkv",
        ]
    )
    def test_capitalization_does_not_matter(self, series_name: str):

        dummy_episode: Path = Path(series_name)
        parse_results: dict = try_parse_file_name(dummy_episode)

        assert parse_results["season_number"] == 1
        assert parse_results["episode_number"] == 2