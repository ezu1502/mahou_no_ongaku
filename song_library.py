from pathlib import Path


class SongLibrary:
    def __init__(self) -> None:

        self.folder: Path 
        self.path_list: list[Path] = []
        self.song_list: list[str] = []

    def set_folder(self, folder: Path) -> None:
        self.folder = folder


