
from pathlib import Path

VALID_EXTENSIONS: frozenset = frozenset({
    ".mkv"
})


class Episode(Path):
    _series: str
    _production_year: int
    _season_number: int

    _episode_number: int
    _production_number: int
    _rip_number: int

    #TODO: add extra meta data like edition, episode titles, etc

    def __init__(self, path: str | Path):

        normalized_path: Path = Path(path)
        self._validate_extension(normalized_path)

        super.__init__(normalized_path)

    def copy_to(self, dir: str | Path):
        ...                                                                                                                                                                                                                                                                                                  
    
    # Private Methods
    def _validate_extension(self, maybe_episode: Path):
        extension: str = maybe_episode.suffix
        is_valid: bool = extension in VALID_EXTENSIONS
        
        if not is_valid:
            raise Exception(f"Invalid episode extension: {extension}")