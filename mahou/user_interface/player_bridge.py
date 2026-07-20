from mahou.core.ENUMS import PS
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Qt
#region PLAYER CONTROLS
class PlayerBridge:
    def __init__(self, window):
        self.window = window

        self.player = self.window.player
        self.player.state_changed.connect(self.window.update_UI_by_state)

        self.app = self.window.app

        self.no_need_to_load = False

    def toggle(self):
        match self.get_state():
            case PS.PLAYING:
                self.player.pause_song()
            case PS.PAUSED:
                self.player.play_song()
            case PS.IN_MENU:
                self.load_and_play()
        # self.window.update_UI_by_state()


    def load_and_play(self, specific_item = None, play = True):
        if specific_item is None:
            item = self.window.get_listbox_selection()
            if item is None:
                return
        else:
            item = specific_item
        
        self.window.update_listbox_UI(new_item = item)
        

        self.window.playing_item = item

        song = item.data(Qt.ItemDataRole.UserRole)
  
        if song is None:
            return
    
        self.player.load_song(song)
        if play:
            self.player.play_song()

        self.window.see_item(item)

        song_title = song.title
        self.show_now_playing(song_title)
        self.set_window_title(song_title = song_title)   

    def play_selected(self):
        self.load_and_play()
        # self.window.update_UI_by_state()

    def play_without_loading(self):
        self.player.play_song()

    def stop_song(self, hide_now_playing = True):
        self.player.stop_song()
        if hide_now_playing:
            self.window.hide_now_playing()

        self.window.playing_item = None
        # self.window.update_UI_by_state()
        self.window.manage_play_selected_button()
        self.window.reset_listbox_UI()
        self.set_window_title(reset = True)
        
        
    
    def set_window_title(self, song_title = None, reset = False):
        if reset:
            self.window.setWindowTitle(self.window.WINDOW_TITLE)
            return
        
        MAX_SIZE = 37
        if song_title is None:
            return
        
        if len(song_title) > MAX_SIZE:
            song_title = song_title[:MAX_SIZE - 1] + "…"

        if song_title:
            self.window.setWindowTitle(f"{song_title} - MAHOU NO ONGAKU")




    def restart_song(self):
        self.player.set_pos(0)
        

    def change_song(self, change):
        if self.player.loaded_song is None or self.window.playing_item is None:
            return
        if change == 0:
            return
        if change > 1 or change < -1:
            raise ValueError(f"Unexpected change value: ({change}). \nChange in function change_song must be between (-1) and (1)")
        
        item_count = self.window.listbox.count()
        current_index = self.window.listbox.row(self.window.playing_item)
        new_index = (current_index + change) % item_count

        new_item = self.window.listbox.item(new_index)

        if new_item is None:
            return

        match self.get_state():
            case PS.PLAYING:
                self.load_and_play(new_item)
            case PS.PAUSED:
                self.load_and_play(new_item)
                self.player.pause_song()


    
            
#endregion
#region UI Updating
    def get_state(self):
        return self.app.state
    
    def set_state(self, state: PS):
        self.window.set_state(state)

    def show_now_playing(self, text: str):
        self.window.show_now_playing(text)