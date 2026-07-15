import tkinter as tk
from tkinter import ttk
import logging
from mahou_libs.colors import painted_string
from mahou.core.ENUMS import PS
from mahou.core.song import Song
from mahou_libs.bocca import BoccaFiglia
log = BoccaFiglia("main_screen", "#2424F7")

class MainScreen(tk.Frame):

    def __init__(self, root, sith_lord):
        super().__init__(root, bg = "#111111")

        self.root = root
        self.pack(fill = "both", expand = True)
        self.playing_label_exists = False
        self.duration_label_exists = False

        self.sith_lord = sith_lord
        #region WIDGETS

        self.get_selection_from_listbox = sith_lord.get_listbox_selection_index

        self.title = self.make_mahou_label(self, "Mahou no Ongaku", font = ("Trebuchet MS", 30, "bold"))
        self.title.pack(pady = 20)

        self.music_listbox = self.make_mahou_listbox(self)
        self.music_listbox.pack(padx = 20, pady = (0, 20), side = "left", fill = "both")
        self.music_listbox.bind("<<ListboxSelect>>", self.get_selection_from_listbox)
        self.music_listbox.bind("<Up>", lambda select_up: self.change_selection(-1, select_up))
        self.music_listbox.bind("<Down>", lambda select_down: self.change_selection(1))

        self.listbox_list = []
    
        self.scrollbar = self.make_mahou_scrollbar(self)
        self.scrollbar.pack(side = "right", fill = "y")
        self.music_listbox.config(yscrollcommand = self.scrollbar.set) #Pra scrollbar funcionar
        self.scrollbar.config(command = self.music_listbox.yview)
        
        self.play_button = self.make_mahou_button(
            self,
            "▶ PLAY",
            command = sith_lord.toggle
            )
        
        self.play_button.pack(pady = 10)

        self.folder_button = self.make_mahou_button(self, "Choose folder", command = sith_lord.get_folder_path)
        self.folder_button.pack()

        self.restart_song_button = self.make_mahou_button(self, "Restart song", command = sith_lord.restart_song)
        self.restart_song_button.pack(pady = (10,0), padx = 10)
        
        self.previous_song_button = self.make_mahou_button(self, "Previous", command = lambda: sith_lord.change_song(-1))
        self.previous_song_button.pack(pady = (10,0), padx = 10)

        self.next_song_button = self.make_mahou_button(self, "Next", command = lambda: sith_lord.change_song(1))
        self.next_song_button.pack(pady = (10, 1), padx = 10)

        self.play_selection_button = self.make_mahou_button(
            self,
            f"Play Selected Song",
            command = self.play_selected_song_button
            )
        
        self.duration_label = None

        self.playing_label = None

        #endregion

        log.trace("Main screen created")



    #region ------------------ #01 RESOURCES

    def set_playing_label(self, songname = "null", visible = True):
        if not visible and self.playing_label is not None:
            self.playing_label.pack_forget()
            return
        
        if self.playing_label is None:
            self.playing_label = self.make_mahou_label(
                    self,
                    f"Now Playing: {songname}",
                    font = ("Bahnschrift", 16)
                    )
            self.playing_label.pack()
            return
        

        self.playing_label.config(text = f"Now Playing: {songname}", font = ("Bahnschrift", 16))
        self.playing_label.pack()

        
    def set_duration_label(self, duration: str = "null", visible = True):
        if not visible and self.duration_label is not None:
            self.duration_label.pack_forget()
            return
        
        if self.duration_label is None:
            self.duration_label = self.make_mahou_label(self, wanted_text = duration, font = ("Trebuchet MS", 15, "bold"))
            self.duration_label.pack()

            log.trace("duration label created and shown")
        else:
            self.duration_label.config(text = duration)
            self.duration_label.pack()
            log.trace("duration label changed")

    
    def set_selectedb_visibility(self, visible: bool):
        if visible:
            self.play_selection_button.pack()
        else:
            self.play_selection_button.pack_forget()


    def play_selected_song_button(self):
        self.sith_lord.play_selected_song_button()
        self.set_selectedb_visibility(visible = False)

    def listbox_select(self, index):
        self.music_listbox.select_clear(0, tk.END)
        self.music_listbox.select_set(index)

    def change_selection(self, change, event = None):
        if change == 0:
            return
        index = self.get_selection_from_listbox()
        print(self.get_selection_from_listbox())
        self.listbox_select(index + change)
        self.sith_lord.select(self.listbox_list[index + change][0], index + change)
        return "break"
        

    def highlight_playing_song(self, index):
        self.music_listbox.delete(index)
        self.music_listbox.insert(index, f"▶ {self.sith_lord.library.song_list[index].display_name}")
        self.music_listbox.itemconfig(index, fg = "#FFFF00", bg = "#333333")
        
    def update_UI_by_state(self, state):
        match state:
            case PS.PLAYING:
                self.play_button.config(text = "PAUSE")
            case PS.PAUSED | PS.IN_MENU:
                self.play_button.config(text = "▶ PLAY")

        log.trace("UI updated by state")    

        
    #endregion

    #region ------------------ #02 WIDGETMAKER

    def make_mahou_label(self, parent, wanted_text: str, **settings):
        default_settings = {
            "font": ("Bahnschrift", 14),
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
            "font": ("Segoe UI Semibold", 12),
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
            "Vertical.TScrollbar",
            background = "#b8b8b8",
            troughcolor = "#1a1a1a",
            bordercolor = "#1a1a1a",
            arrowcolor = "#ffffff",
            relief = "flat"
        )

        return ttk.Scrollbar(parent, orient = "vertical", style = "Vertical.TScrollbar")
        
#endregion

    def set_listbox_musiclist(self, list_to_add: list[Song]):
        self.music_listbox.delete(0, tk.END)

        for indx, song in enumerate(list_to_add):
            self.listbox_list.append((indx, song)) # Não esquecer da ordem [0]INDEX [1]SONG

        for indx, each_song in self.listbox_list:
            self.music_listbox.insert(tk.END, f"   {each_song.display_name}")

            if indx % 2 == 0:
                self.music_listbox.itemconfig(indx, bg = "#111111")
            else:
                self.music_listbox.itemconfig(indx, bg = "#1B1B1B")

    

    


    