from pathlib import Path
from mahou_libs.colors import COLORS, painted_string
from mahou.core.song import Song
from send2trash import send2trash
import json
from mahou_libs.bocca import BoccaFiglia
from mahou.core.enums import Paths
from mahou import file_manager

log = BoccaFiglia("song_library", "#FF0000")

class SongLibrary:
    def __init__(self) -> None:
        self.folder: Path | None = None
        self.song_list: list[Song] = []

        default_folder = self.default_folder
        if default_folder is not None and default_folder is not ".":
            self.set_folder(default_folder)

    @property
    def default_folder(self):
        options_dict = file_manager.read_file(Paths.SETTINGS_FILE)

        folder = options_dict.get("default_folder", None)

        return Path(folder) if folder is not None else None
            

    def save_folder(self, folder):
        folder = str(folder)

        file_manager.save_setting(folder, "default_folder")


    def set_folder(self, folder: Path) -> None:
        if folder is None:
            log.warning("Exception: path is null")
            return None
        
        self.folder = folder
        self.set_song_list(folder)
        self.save_folder(folder)
        

    def set_song_list(self, folder: Path):
        self.song_list.clear()

        supported_formats = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}

        for file_path in folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                song = Song(path = file_path)
                self.song_list.append(song)
    
        self.song_list.sort(key = lambda song: song.title.lower())
                
        log.debug("song list set")


