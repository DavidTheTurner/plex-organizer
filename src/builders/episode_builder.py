

from pathlib import Path
import re
from ..data_objects import Episode
from ..protocols import SeriesContextProtocol


VALID_EXTENSIONS: frozenset = frozenset({
    ".mkv"
})


class EpisodeBuilder:
    """
    Class for simplifying the process of creating episode objects
    """
    __slots__ = (
        "_series_context",
        "_path",
        "_season_number",
        "_episode_number",
        "_local_number",
    )

    def __init__(self, series_context: SeriesContextProtocol, path: Path | str):

        normalized_path: Path = Path(path)
        self._validate_extension(normalized_path)
        self._path = normalized_path

        self._series_context: SeriesContextProtocol = series_context

        self._season_number: int | None = None
        self._episode_number: int | None = None
        self._local_number: int | None = None

    def set_local_number(self, local_number: int) -> "EpisodeBuilder":
        self._local_number = local_number
        return self

    def set_season_number(self, season_number: int) -> "EpisodeBuilder":
        self._season_number = season_number
        return self

    def set_episode_number(self, episode_number: int) -> "EpisodeBuilder":
        self._episode_number = episode_number
        return self

    def build(self) -> Episode:
        return Episode(
            series_context=self._series_context,
            path=self._path,
            season_number=self._season_number,
            episode_number=self._episode_number,
            local_number=self._local_number,
        )

    # Private Methods

    def _validate_extension(self, maybe_episode: Path):
        extension: str = maybe_episode.suffix
        is_valid: bool = extension in VALID_EXTENSIONS

        if not is_valid:
            raise Exception(f"Invalid episode extension: {maybe_episode.stem}")


# Handles extracting the season number and episode number from the typical plex episode naming
# scheme. Capitalization of the 's' and 'e' does not matter.
#
# Example:
#   Revolutionary Girl Utena (1997) - s01e03 - On The Night Of The Ball.mkv
#   # season_number = 01, episode_number = 03
#
#   Revolutionary Girl Utena (1997) - S01E04 - The Sunlit Garden (Prelude).mkv
#   # season_number = 01, episode_number = 04
SEASON_AND_EPISODE_PATTERN: re.Pattern = re.compile(r"\-\s+[sS](?P<season_number>\d+)[eE](?P<episode_number>\d+)")

# Handles episode files with an automatically generated number at the end which typically
# results from ripping DVDs.
#
# Example:
#   UTENA_SET3_BD1_t00.mkv
#   # local_number = 00
#
#   UTENA_SET3_BD1_t01.mkv
#   # local_number = 01
#
#   UTENA_SET3_BD1_t02.mkv
#   # local_number = 02
LOCALLY_NUMBERED: re.Pattern = re.compile(r"(?P<local_number>\d+)$")


def create_episode(series_context: SeriesContextProtocol, episode_path: Path) -> Episode:
    """
    Factory that builds appropriate episode objects based on name of episode
    """

    episode_name: str = episode_path.name

    resulting_episode: Episode
    if match := SEASON_AND_EPISODE_PATTERN.search(episode_name):
        season_number: int = int(match.group("season_number"))
        episode_number: int = int(match.group("episode_number"))
        resulting_episode = (
            EpisodeBuilder(series_context=series_context, path=episode_path)
            .set_season_number(season_number)
            .set_episode_number(episode_number)
            .set_local_number(episode_number)
            .build()
        )
    elif match := LOCALLY_NUMBERED.search(episode_name):
        local_number: int = int(match.group("local_number"))
        resulting_episode = (
            EpisodeBuilder(series_context=series_context, path=episode_path)
            .set_local_number(local_number)
            .build
        )
    else:
        raise Exception(f"Cannot determine order from episode {episode_name}.")

    return resulting_episode
