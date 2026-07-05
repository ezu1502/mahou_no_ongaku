import tkinter as tk
import logging
import os
from pathlib import Path
from tkinter import filedialog as explorer

log = logging.getLogger(__name__)

class MahouWindow:
    def __init__(self, player, dimensions = "900x600"):
        self.root = tk.Tk()
        self.root.title("MAHOU NO ONGAKU")
        
        positioning = self.centralize(dimensions)
        self.root.geometry(positioning)

        self.root.resizable(False, False) #centraliza e escolhe o tamanho dela
        self.root.config(bg = "#111111")
        log.debug("Window created")

        self.mahou_player = player
        log.debug("Player obj. received in window")

        self.display_list = []

        self.default_folder = Path.home() / "Mahou no Ongaku"      

        self.title = self.make_mahou_label("Mahou no Ongaku", font = ("Banschrift", 20))
        self.title.pack(pady = 20)
        
        self.play_button = self.make_mahou_button("PLAY", command = self.play_song)
        self.play_button.pack(pady = 10)

        self.folder_button = self.make_mahou_button("Choose folder", command = self.get_folder_path)
        self.folder_button.pack()

        self.music_listbox = self.make_mahou_listbox()
        self.music_listbox.pack(pady = 20)

        self.root.protocol("WM_DELETE_WINDOW", self.x_button_was_pressed)

        self.set_folder_and_lists(self.default_folder)
 


        log.debug("Player object loaded")


    def play_song(self):
        # print(path.exists())
        # self.mahou_player.play_song(song_path = path)
        pass

    def get_folder_path(self):
        folder_path = Path(explorer.askdirectory())
        if not folder_path:
            return
        
        self.set_folder_and_lists(folder_path)

    def set_folder_and_lists(self, folder_path: Path):
        if not folder_path:
            log.warning("Exception: path is null")
            return None
        
        

        self.sourcefolder = folder_path
        path_list = [file for file in folder_path.iterdir() if file.is_file()]
        log.debug("pathlist created")

        
        self.display_list.clear()
        self.music_listbox.delete(0, tk.END)

        for indx, name in enumerate(path_list, start = 1):
            justname = name.stem
            display_name = f"{indx} - {justname}"
            self.display_list.append(display_name)
        log.debug("display list created")
        
        self.set_listbox_musiclist(self.display_list)



    def set_listbox_musiclist(self, list_to_add):
        for song in list_to_add:
            self.music_listbox.insert(tk.END, song)


    def centralize(self, dimensions: str) -> str:
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        root_width, root_height = dimensions.split("x")
        root_width, root_height = int(root_width), int(root_height)

        x = (screen_width//2) - (root_width//2)
        y = (screen_height//2) - (root_height//2)
        position_and_dimensions = f"{dimensions}+{x}+{y}"
        return position_and_dimensions
    
    def x_button_was_pressed(self):
        log.info("Program Terminated")
        self.root.destroy()
        os._exit(0)
        # self.player.set_state(PS.SHUT_DOWN)


    def make_mahou_label(self, wanted_text: str, **settings):
        default_settings = {
            "font": ("Banschrift", 14),
            "bg": self.root.cget("bg") or "#000000",
            "fg": "#ffffff",
            "anchor": "center",
            "justify": "center",
            "wraplength": 400
        }
        chosen_settings = default_settings.copy()
        chosen_settings.update(settings)

        return tk.Label(self.root, text = wanted_text, **chosen_settings)
    
    def make_mahou_button(self, button_text: str, command, **settings):
        default_config = {
            "font": ("Bahnschrift", 14),
            "width": 20,
            "height": 2,
            "bg": "#222222",
            "fg": "#ffffff",
            "activebackground": "#333333",
            "activeforeground": "#ffffff"
        }
        
        chosen_settings = default_config.copy()
        chosen_settings.update(settings)

        return tk.Button(self.root, text = button_text, command = command, **chosen_settings)
    
    def make_mahou_listbox(self, **listbox_config):
        default_config = {
            "font": ("Segoe UI", 12),
            # "bg": parent.cget("bg") or "#000000",
            "bg": "#2E2E2E",
            "fg": "#ffffff",
            "selectbackground": "#616161",
            "selectforeground": "#ffffff",
            "width": 70,
            "height": 14,
            "highlightthickness": 0,
            "borderwidth": 0,
            "activestyle": "none"
        }

        chosen_config = default_config.copy()
        chosen_config.update(listbox_config)

        return tk.Listbox(self.root, **chosen_config)