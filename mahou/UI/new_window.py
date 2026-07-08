import tkinter as tk
import logging
from pathlib import Path
from tkinter import filedialog as explorer
from mahou.core.ENUMS import PS
from mahou.colors import painted_string
from mahou.core.song_library import SongLibrary
from mahou.core.song import Song
from mahou.UI.main_screen import MainScreen

log = logging.getLogger(painted_string("mahou_window", "#7AF9FD"))

class MahouWindow:
    def __init__(self, player, app, dimensions = "900x600"):

        self.define_window(dimensions) #WINDOW DEFINITIONS

        self.app = app
        self.mahou_player = player

        self.mahou_player.window_set_state = self.set_state

        self.library = SongLibrary()

        log.debug("Player and App obj. received in window")

    # ------------- USEFUL VARIABLES
        
        self.new_loaded_song = False

        self.selection_path: Path | None = None
        self.selected_index: int | None = None

        log.debug("Window init lists and folder created")

    # ------------------------------------------------------------------

       
        self.main_screen = MainScreen(root = self.root, sith_lord = self)
        self.silence_listbox_stupid_keys()

        if self.library.default_folder is not None:
            self.set_folder_and_lists(self.library.default_folder) #DEFAULT_FOLDER SET



#region ------------------ #00 WINDOW DEFINING

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

    def define_window(self, dimensions):
        self.root = tk.Tk()
        self.root.title("MAHOU NO ONGAKU")
        
        positioning = self.centralize(dimensions)
        self.root.geometry(positioning)

        self.root.resizable(False, False) #centraliza e escolhe o tamanho dela
        self.root.config(bg = "#111111")

        self.root.bind("<KeyPress>", self.on_key_pressed)

        self.root.protocol("WM_DELETE_WINDOW", self.x_button_was_pressed)

        log.debug("Window created")

    def start_ui_loop(self):
        self.update_dynamic_UI()
        self.root.after(16, self.start_ui_loop)

    def update_dynamic_UI(self):
        #waveform, progress bar, animações, etc
        pass

    def run(self):
        log.debug("MahouWindow is now running")
        self.start_ui_loop()
        self.root.mainloop()

#endregion
#region ------------------ #01 PLAYER CONTROLS

    def play_song_by_index(self, index: int):
        self.reset_listbox_ui()
        current_song = self.library.song_list[index]
        self.mahou_player.load_song(current_song.path)
        self.mahou_player.play_song()

        self.playing_song_name = current_song.display_name
        self.playing_song_index = index

        self.main_screen.highlight_playing_song(index)

        self.set_state(PS.PLAYING)
        self.main_screen.show_playing_label(self.playing_song_name)

    def play_without_load(self):
        self.mahou_player.play_without_load()

    def pause_song(self) -> None:
        self.mahou_player.pause_song()

    def stop_song(self) -> None:
        self.mahou_player.stop_song()
        try:
            self.main_screen.playing_label.destroy()
            self.main_screen.playing_label_exists = False
        except:
            pass
        self.reset_listbox_ui()


    def reset_listbox_ui(self):
        self.main_screen.set_listbox_musiclist(self.library.song_list)



    def load_song_index(self, index) -> None:
        path_to_load: Path = self.library.song_list[index].path
        self.mahou_player.load_song(path_to_load)
        self.playing_song_index = index

    def unpause_song(self) -> None:
        self.mahou_player.unpause_song()

    def toggle(self):
        match self.app.state:
            case PS.IN_MENU:
                if self.selected_index is not None:
                    self.play_song_by_index(self.selected_index)
            case PS.PLAYING:
                self.pause_song()
            case PS.PAUSED:
                if not self.new_loaded_song:
                    self.unpause_song() 
                else:
                    if self.selected_index is not None:
                        self.play_song_by_index(self.selected_index)
                    self.new_loaded_song = False
            case _:
                self.play_without_load()


    def goto_previous_song(self):
        if self.selected_index is None:
            return
        
        log.debug("'Previous' button pressed")

        folder_length: int = len(self.library.song_list)

        print(self.selected_index)
        if self.selected_index <= 0:
            self.selected_index = (folder_length - 1)
        else:
            self.selected_index -= 1

        match self.app.state:
            case PS.PLAYING:
                self.stop_song()
                self.play_song_by_index(self.selected_index)
            case PS.PAUSED:
                self.stop_song()
                self.new_loaded_song = True


    def goto_next_song(self):
        if self.selected_index is None:
            return
        log.debug("'Previous' button pressed")

        folder_length: int = len(self.library.song_list)
        if self.selected_index >= (folder_length - 1):
            self.selected_index = 0
        else:
            self.selected_index += 1

        match self.app.state:
            case PS.PLAYING:
                self.stop_song()
                self.play_song_by_index(self.selected_index)
            case PS.PAUSED:
                self.stop_song()
                self.new_loaded_song = True


    
    def restart_song(self):
        log.debug("Restart Button pressed")

        if self.app.state == PS.PLAYING:
            self.stop_song()
            self.play_song_by_index(self.playing_song_index)
            log.debug("Restarted song successfully")

        elif self.app.state == PS.PAUSED:
            self.stop_song()
            self.load_song_index(self.playing_song_index)
            self.main_screen.highlight_playing_song(self.playing_song_index)
            log.debug("Restarted song successfully")
        else:
            log.warning("No song to restart, dummy!")

#endregion

#region ------------------ #02 STATE MANAGER

    def set_state(self, state: PS):
        self.app.set_state(state)
        self.main_screen.update_UI_by_state(self.app.state)


    def get_state(self) -> PS:
        return self.app.state

#endregion

#region ------------------ #03 LISTS AND FOLDERS

    def get_folder_path(self):
        folder_str = explorer.askdirectory()
        if not folder_str:
            return
        folder_path = Path(folder_str)
        
        self.set_folder_and_lists(folder_path)

    def set_folder_and_lists(self, folder_path: Path):
        self.library.set_folder(folder_path)
        self.library.set_song_list(folder_path)

        self.main_screen.music_listbox.delete(0, tk.END)
        self.main_screen.set_listbox_musiclist(self.library.song_list)

    
# melhor deixar isso aqui embaixo na window mesmo kkkkkkkkk

    def get_selection_from_listbox(self, event):
        selection = self.main_screen.music_listbox.curselection()
        if not selection:
            return
        
        selection_index = selection[0]
        self.selected_index = selection_index   

        self.selection_path = Path(self.library.song_list[selection_index].path)
        self.selected_song = self.selection_path.stem
            
        # print(self.selection_path)
        # print(selection_name)

#endregion

#region ------------------ #04 KEYBOARD
 

    def on_key_pressed(self, event):
        raw_command = event.keysym
        command = raw_command.lower()

        match command:
            case "space":
                self.toggle()
            case "right":
                self.goto_next_song()
                return "break"
            case "left":
                self.goto_previous_song()
                return "break"
            case "r":
                self.restart_song()
            case "s" | "escape":
                self.stop_song()

    def silence_listbox_stupid_keys(self):
        lb = self.main_screen.music_listbox

        self.root.bind_class("Listbox", "<Right>", lambda e: (self.on_key_pressed, "break"))
        self.root.bind_class("Listbox", "<Left>", lambda e: (self.on_key_pressed, "break"))
        self.root.bind_class("Listbox", "<space>", lambda e: (self.on_key_pressed, "break"))

        tags = list(lb.bindtags())
        if "Listbox" in tags:
            tags.remove("Listbox")
           




#endregion

        