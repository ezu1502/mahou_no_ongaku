from pathlib import Path
import logging
from mahou.colors import COLORS, painted_string
from mahou.core.song import Song

log = logging.getLogger(painted_string("song_library", "#FF0000"))

class SongLibrary:
    def __init__(self) -> None:

        self.default_folder = Path.home() / "Mahou no Ongaku"

        self.folder: Path | None = self.default_folder if self.default_folder.exists() else None

        self.song_list: list[Song] = []


    def set_folder(self, folder: Path) -> None:
        if not folder:
            log.warning("Exception: path is null")
            return None
        self.folder = folder

    def set_song_list(self, folder: Path):
        self.song_list.clear()
        for file in folder.iterdir():
            if file.is_file():
                song = Song(file)
                self.song_list.append(song)
        log.debug("song list created")


