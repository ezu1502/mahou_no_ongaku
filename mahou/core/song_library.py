from pathlib import Path
from mahou_libs.colors import COLORS, painted_string
from mahou.core.song import Song
from send2trash import send2trash
import json
from mahou_libs.bocca import BoccaFiglia

log = BoccaFiglia("song_library", "#FF0000")

class SongLibrary:
    def __init__(self) -> None:
        self.folder: Path | None = None
        self.song_list: list[Song] = []

        default_folder = self.default_folder
        if default_folder is not None:
            self.set_folder(default_folder)

    @property
    def default_folder(self):
        default_folder_cache_file = Path ("mahou_cache") / ("app_cache") / "folder_settings.json"

        if default_folder_cache_file.exists():
            try:
                with default_folder_cache_file.open("r", encoding = "utf-8") as cache:
                    dictionary = json.load(cache)
                    folder = dictionary.get("default_folder")
                    return Path(folder) if folder is not None else None

            except (json.JSONDecodeError, TypeError, KeyError): #(quebrado, invalido, sem a chave)
                log.warning("Couldn't read JSON file")
                return None
        return None
            
    def save_folder(self, folder):
        default_folder_cache_file = Path ("mahou_cache") / ("app_cache") / "folder_settings.json"
        dictionary = {"default_folder": str(folder)}
        default_folder_cache_file.parent.mkdir(parents = True, exist_ok = True)
        with default_folder_cache_file.open("w", encoding = "utf-8") as cache:
            json.dump(dictionary, cache, ensure_ascii = True, indent = 4)


    def set_folder(self, folder: Path) -> None:
        if folder is None:
            log.warning("Exception: path is null")
            return None
        
        self.folder = folder
        self.save_folder(folder)

    def set_song_list(self, folder: Path):
        self.song_list.clear()

        supported_formats = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}

        for file_path in folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_formats:
                song = Song(path = file_path)
                self.song_list.append(song)
                
        log.debug("song list created")

# ! cuidado pra n fazer merda kkkkkkkkkkkkk

    def clear_all_songs_cache(self):
        folder = Path ("mahou_cache") / ("song_cache")
        if not folder.exists():
            return
        for file in Path.iterdir(folder):
            if file.suffix != ".json" or not file.is_file():
                log.warning("Cannot erase folder, as you may be trying to erase something you dont really wanna remove...")
                return
        
        send2trash(folder)
        log.info("Songs cache cleared.")
            
        

