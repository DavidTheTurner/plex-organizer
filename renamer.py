from pathlib import Path
import re
import shutil

def rename(
    *,
    season_path: str,
    season_map: dict[tuple[int, int], int],
    episode_offset: int = 1
):

    season: Path = Path(season_path)
    pattern: re.Pattern = re.compile(r"-\s?(?P<episode>[0-9]+)$")

    print("File List Length:", len(list(season.iterdir())))

    episodes: list[Path] = [
        episode_file for episode_file
        in season.iterdir() if pattern.search(episode_file.stem)
    ]

    print("Episode Len:", len(episodes))
    first_ep: int = min(
        [
            int(pattern.search(episode_file.stem).group("episode")) for episode_file
            in season.iterdir() if pattern.search(episode_file.stem)
        ]
    )
    print(first_ep)
    for file in episodes:
        stated_number: int = int(pattern.search(file.stem).group("episode"))
        production_number: int = stated_number + episode_offset
        season_number, episode_number = _get_episode_number(season_map, production_number)
        file.rename(fr"{file.parent}\{file.parent.name} - s{season_number:02d}e{episode_number:02d}{file.suffix}")
        # print(f"{file.parent}\Fist of the North Star (1984) - s0{season_number}e{episode_number:02d}{file.suffix}")
        # print(f"{first_ep=}")
        # print(f"{stated_number=}")
        # print(f"{episode_number=}")
        # print(f"{file.parent}\Fist of the North Star (1984) - s0{season_number}e{episode_number:02d}{file.suffix}\n")


def _get_episode_number(season_map: dict[tuple[int, int], int], production_number: int) -> tuple[int, int]:

    for episode_range, season in season_map.items():
        if episode_range[0] <= production_number <= episode_range[1]:
            episode_number: int = production_number - episode_range[0] + 1
            return season, episode_number
    
    raise Exception(f"Production number not mapped to season: {production_number=}")


def combine_episode_folders(folders: list[Path | str], output_name: str):
    normalized_folders: list[Path] = [Path(folder) for folder in folders]

    if not normalized_folders:
        return

    ending_number: re.Pattern = re.compile(r".*\D(?P<ending_number>[0-9]+)$")
    if any(not ending_number.search(folder.stem) for folder in normalized_folders):
        raise Exception("Not all episode folders are numbered")
    
    output_folder: Path = normalized_folders[0].parent / output_name
    output_folder.mkdir(parents=True, exist_ok=True)

    episode_number = 1
    for folder in normalized_folders:
        episode_list: list[Path] = sorted(list(folder.iterdir()), key=lambda x: int(ending_number.search(x.stem).group("ending_number")))
        for episode in episode_list:
            production_episode: Path = output_folder / f"{output_name} - {episode_number:03d}{''.join(episode.suffixes)}"
            print(f"{str(episode)} -> {str(production_episode)}\n")
            shutil.copyfile(episode, production_episode)
            episode_number += 1





fist_of_the_north_star_season_map: dict[tuple[int, int], int] = {
    (23, 57): 2,
    (58, 82): 3,
    (83, 109): 4,
    (110, 122): 5,
    (123, 152): 6
}

scooby_doo_season_map: dict[tuple[int, int], int] = {
    (1, 17): 1,
    (18, 25): 2,
    (26, 41): 3,
}

if __name__ == "__main__":
    rename(
        season_path=r"E:\Scooby-Doo, Where Are You! (1969)",
        season_map=scooby_doo_season_map,
        episode_offset=0
    )
    # combine_episode_folders([
    #     "E:\Scooby-Doo™, Where Are You! Disc 1",
    #     "E:\Scooby-Doo™, Where Are You! Disc 2",
    #     "E:\Scooby-Doo™, Where Are You! Disc 3",
    #     "E:\Scooby-Doo™, Where Are You! Disc 4",
    # ],
    # "Scooby-Doo, Where Are You!"
    # )