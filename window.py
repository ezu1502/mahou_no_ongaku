import tkinter as tk
import logging
import os
from pathlib import Path
from tkinter import filedialog as explorer
from ENUMS import PS, COLORS, painted_string
from tkinter import ttk

log = logging.getLogger(__name__)

class MahouWindow:
    def __init__(self, player, dimensions = "900x600"):

        self.define_window(dimensions) #WINDOW DEFINITIONS

        self.mahou_player = player
        self.mahou_player.window_set_state = self.set_state
        self.mahou_player.window_get_state = self.get_state

        log.debug("Player obj. received in window") #RECEIVING PLAYER

        self.create_init_lists() #WINDOW LISTS AND FOLDER CREATION

        self.state = PS.IN_MENU #DEFAULT STATE SET
 
        self.make_main_screen() #DEFINING BUTTONS AND LISTBOX

        self.set_folder_and_lists(self.default_folder) #DEFAULT_FOLDER SET




# ------------------------ #01 - PLAYER CONTROLS

    def play_song_by_index(self, index: int):
        current_path: Path = self.path_list[index]
        self.playing_song_index = index
        self.mahou_player.load_song(current_path)
        self.mahou_player.play_song()
        self.show_playing_label

    def play_song(self):
        if self.selection_path is None:
            log.warning("No song was selected!")
            return
        
        self.mahou_player.load_song(self.selection_path)
        self.mahou_player.play_song()

        self.playing_song_index: int | None = self.selected_index
        # self.selected_index = None

        if(self.playing_song_index is not None):
            self.playing_song_name = self.path_list[self.playing_song_index].stem
        else:
            log.warning("from play_song(self): self.playing_song_index is None!")

        self.show_playing_label(self.playing_song_name)
        # self.selection_path = None

    def play_previous_song(self):
        if self.playing_song_index is not None:
            previous_song_index: int = (self.playing_song_index - 1)

        previous_song_path = self.path_list[previous_song_index]
        self.mahou_player.load_song(previous_song_path)
        self.mahou_player.play_song()

        self.playing_song_index = previous_song_index

        if(self.playing_song_index is not None):
            self.playing_song_name = self.path_list[self.playing_song_index].stem
        else:
            log.warning("from play_previous_song(self): self.playing_song_index is None!")

        self.selected_index = None
        self.selection_path = None

        self.show_playing_label(self.playing_song_name)

    def play_next_song(self):
        if self.playing_song_index is not None:
            next_song_index: int = (self.playing_song_index + 1)

        next_song_path = self.path_list[next_song_index]
        self.mahou_player.load_song(next_song_path)
        self.mahou_player.play_song()

        self.playing_song_index = next_song_index

        if(self.playing_song_index is not None):
            self.playing_song_name = self.path_list[self.playing_song_index].stem
        else:
            log.warning("from play_next_song(self): self.playing_song_index is None!")

        self.selected_index = None
        self.selection_path = None

        self.show_playing_label(self.playing_song_name)
        

    def pause_song(self) -> None:
        self.mahou_player.pause_song()

    def stop_song(self) -> None:
        self.mahou_player.stop_song()

    def load_song(self) -> None:
        self.mahou_player.load_song()

    def unpause_song(self) -> None:
        self.mahou_player.unpause_song()

    def toggle(self):
        match self.state:
            case PS.IN_MENU:
                self.play_song()
            case PS.PLAYING:
                self.pause_song()
            case PS.PAUSED:
                self.unpause_song()


    def goto_previous_song(self):
        log.debug("'Previous' button pressed")

        if self.playing_song_index is None:
            log.warning("self.playing_song_index is None!")
            return
        

        previous_song_index = self.playing_song_index - 1
        self.selection_path = self.path_list[previous_song_index]
        previous_song_selection = self.playing_song_index - 1

        self.music_listbox.selection_clear(self.playing_song_index)
        self.music_listbox.select_set(previous_song_selection)

        match self.state:
            case PS.PLAYING:
                self.stop_song()
                self.play_previous_song()
            case PS.PAUSED:
                self.stop_song()
                self.load_song()


    def goto_next_song(self):
        log.debug("'Next' button pressed")
        if self.playing_song_index is None:
            log.warning("self.playing_song_index is None!")
            return
        

        next_song_index = self.playing_song_index + 1
        self.selection_path = self.path_list[next_song_index]
        next_selection = self.playing_song_index + 1

        self.music_listbox.selection_clear(self.playing_song_index)
        self.music_listbox.select_set(next_selection)

        match self.state:
            case PS.PLAYING:
                self.stop_song()
                self.play_next_song()
            case PS.PAUSED:
                self.stop_song()
                self.load_song()


    def restart_song(self):
        log.debug("Restart Button pressed")

        if self.state == PS.PLAYING:
            self.stop_song()
            self.play_song()

            log.debug("Restarted song successfully")
        elif self.state == PS.PAUSED:
            self.stop_song()
            self.load_song()

            log.debug("Restarted song successfully")
        else:
            log.warning("No song to restart, dummy!")

        

        

# ------------------------ #02 - STATE MANAGER

    def set_state(self, state: PS) -> None:
        self.state = state
        if state != PS.SHUT_DOWN:
            log.debug(f"window state defined to {state}")
        self.update_UI_by_state()

    def update_UI_by_state(self):
        match self.state:
            case PS.PLAYING:
                self.play_button.config(text = "PAUSE")
            case PS.PAUSED:
                self.play_button.config(text = "▶ PLAY")    

    def get_state(self) -> PS:
        return self.state

# ------------------------ #03 - LISTS AND FOLDERS

    def get_folder_path(self):
        folder_str = explorer.askdirectory()
        if not folder_str:
            return
        folder_path = Path(folder_str)
        
        self.set_folder_and_lists(folder_path)

    def set_folder_and_lists(self, folder_path: Path):
        if not folder_path:
            log.warning("Exception: path is null")
            return None
        
        

        self.sourcefolder = folder_path
        self.path_list = [file for file in folder_path.iterdir() if file.is_file()]
        log.debug("pathlist created")

        
        self.display_list.clear()
        self.music_listbox.delete(0, tk.END)

        for indx, name in enumerate(self.path_list, start = 1):
            justname = name.stem
            display_name = f"{indx} - {justname}"
            self.display_list.append(display_name)
        log.debug("display list created")
        
        self.set_listbox_musiclist(self.display_list)

    def set_listbox_musiclist(self, list_to_add):
        for song in list_to_add:
            self.music_listbox.insert(tk.END, song)

    def get_selection_from_listbox(self, event):
        selection = self.music_listbox.curselection()
        if not selection:
            return
        
        selection_index = selection[0]
        selection_name = self.music_listbox.get(selection_index)

        self.selection_path = Path(self.path_list[selection_index])
        self.selected_song = self.selection_path.stem
        self.selected_index = selection_index        
        # print(self.selection_path)

        # print(selection_name)


# ------------------------ #04 - WINDOW DEFINING

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
        self.root.destroy()
        log.info("Window destroyed")
        self.set_state(PS.SHUT_DOWN)

    def define_window(self, dimensions):
        self.root = tk.Tk()
        self.root.title("MAHOU NO ONGAKU")
        
        positioning = self.centralize(dimensions)
        self.root.geometry(positioning)

        self.root.resizable(False, False) #centraliza e escolhe o tamanho dela
        self.root.config(bg = "#111111")

        self.root.protocol("WM_DELETE_WINDOW", self.x_button_was_pressed)

        log.debug("Window created")

    def create_init_lists(self):
        self.display_list = []
        self.path_list = []

        self.selection_path: Path | None = None
        self.selected_index: int | None = None

        self.default_folder = Path.home() / "Mahou no Ongaku"
        log.debug("Window init lists and folder created")


# ----------------------- #05 - SCREEN FACTORY

    def make_main_screen(self):
        self.main_screen_frame = tk.Frame(self.root, bg = "#111111")
        self.main_screen_frame.pack(fill = "both", expand = True)

        self.title = self.make_mahou_label(self.main_screen_frame, "Mahou no Ongaku", font = ("Banschrift", 30))
        self.title.pack(pady = 20)

        self.music_listbox = self.make_mahou_listbox(self.main_screen_frame)
        self.music_listbox.pack(padx = 20, pady = (0, 20), side = "left", fill = "both")
        self.music_listbox.bind("<<ListboxSelect>>", self.get_selection_from_listbox)
        
        self.play_button = self.make_mahou_button(self.main_screen_frame, "▶ PLAY", command = self.toggle)
        self.play_button.pack(pady = 10)

        self.folder_button = self.make_mahou_button(self.main_screen_frame, "Choose folder", command = self.get_folder_path)
        self.folder_button.pack()

        self.previous_song_button = self.make_mahou_button(self.main_screen_frame, "Restart song", command = self.restart_song)
        self.previous_song_button.pack(pady = (10,0), padx = 10)
        
        self.previous_song_button = self.make_mahou_button(self.main_screen_frame, "Previous", command = self.goto_previous_song)
        self.previous_song_button.pack(pady = (10,0), padx = 10)

        self.next_song_button = self.make_mahou_button(self.main_screen_frame, "Next", command = self.goto_next_song)
        self.next_song_button.pack(pady = 10, padx = 10)

        self.scrollbar = self.make_mahou_scrollbar(self.main_screen_frame)
        self.scrollbar.pack(side = "right", fill = "y")
        self.music_listbox.config(yscrollcommand = self.scrollbar.set) #Pra scrollbar funcionar
        self.scrollbar.config(command = self.music_listbox.yview)

        log.debug("Main screen created")


# - - - - - - - - - - - - - #06 SCREEN RESOURCES FACTORY

    def show_playing_label(self, songname):
        self.playing_label = self.make_mahou_label(self.main_screen_frame, f"Now Playing: {songname}")
        self.playing_label.pack()
        log.debug("playing label shown")


# ----------------------- #07 WIDGET FACTORY

    def make_mahou_label(self, parent, wanted_text: str, **settings):
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

        return tk.Label(parent, text = wanted_text, **chosen_settings)
    
    def make_mahou_button(self, parent, button_text: str, command, **settings):
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

        return tk.Button(parent, text = button_text, command = command, **chosen_settings)
    
    def make_mahou_listbox(self, parent, **listbox_config):
        default_config = {
            "font": ("Segoe UI", 12),
            # "bg": parent.cget("bg") or "#000000",
            "bg": "#2E2E2E",
            "fg": "#ffffff",
            "selectbackground": "#616161",
            "selectforeground": "#ffffff",
            "width": 50,
            "height": 14,
            "highlightthickness": 0,
            "borderwidth": 0,
            "activestyle": "none"
        }

        chosen_config = default_config.copy()
        chosen_config.update(listbox_config)

        return tk.Listbox(parent, **chosen_config)
    
    def make_mahou_scrollbar(self, parent):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Purple.Vertical.TScrollbar",
            background = "#7b2cbf",
            troughcolor = "#1a1a1a",
            bordercolor = "#1a1a1a",
            arrowcolor = "#ffffff",
            relief = "flat"
        )

        return ttk.Scrollbar(parent, orient = "vertical", style = "Purple.Vertical.TScrollbar")
        
        
    

        