from pathlib import Path
import logging
from mahou_libs.colors import COLORS, painted_string
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

        supported_formats = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}

        for file_path in folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                song = Song(path = file_path)
                self.song_list.append(song)
                
        log.debug("song list created")


