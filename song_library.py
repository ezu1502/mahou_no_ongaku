from pathlib import Path
import logging
from colors import COLORS, painted_string

log = logging.getLogger(painted_string("SongLibrary", "#FF0000"))

class SongLibrary:
    def __init__(self) -> None:

        self.default_folder = Path.home() / "Mahou no Ongaku"

        self.folder: Path | None = self.default_folder if self.default_folder.exists() else None
        self.path_list: list[Path] = []
        self.display_list: list[str] = []

    def set_folder(self, folder: Path) -> None:
        if not folder:
            log.warning("Exception: path is null")
            return None
        self.folder = folder

    def set_lists_from_folder(self, folder: Path):
        # PATH LIST
        self.path_list = [file for file in folder.iterdir() if file.is_file()]
        log.debug("pathlist created")

        # DISPLAY LIST
        self.display_list.clear()
        for indx, name in enumerate(self.path_list, start = 1):
            justname = name.stem
            display_name = f"{indx} - {justname}"
            self.display_list.append(display_name)
        log.debug("display list created")

    # def set_folder_and_lists(self, folder_path: Path):
        
    #     self.music_listbox.delete(0, tk.END)
        
    #     self.set_listbox_musiclist(self.display_list)



