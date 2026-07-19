from mahou.core.ENUMS import PS
from PySide6.QtGui import Qt, QColor, QBrush

#region PLAYER CONTROLS
class PlayerBridge:
    def __init__(self, window):
        self.window = window
        self.player = self.window.player
        self.app = self.window.app

        self.no_need_to_load = False
        song_list_length = window.song_list_length()
        self.usable_length = song_list_length - 1

    def toggle(self):
        # print("toggle")
        # print(self.get_state())

        match self.get_state():
            case PS.PLAYING:
                self.player.pause_song()
            case PS.PAUSED:
                if self.no_need_to_load:
                    self.play_without_loading()
                    self.no_need_to_load = False
                else:
                    self.player.unpause_song()
            case PS.IN_MENU:
                self.load_and_play()
        self.window.update_UI_by_state()


    def load_and_play(self, specific_item = None):
        if specific_item is None:
            item = self.window.listbox_selection
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
        self.player.play_song()

        self.window.see_item(item)

        song_title = song.title
        self.show_now_playing(song_title)
        self.set_window_title(song_title = song_title)   

    def play_selected(self):
        self.load_and_play()
        self.window.update_UI_by_state()

    def play_without_loading(self):
        self.player.play_song()

    def stop_song(self, hide_now_playing = True, **kwargs):
        self.player.stop_song(**kwargs)
        if hide_now_playing:
            self.window.hide_now_playing()
        self.window.update_UI_by_state()
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
        match self.get_state():
            case PS.PLAYING:
                self.stop_song(hide_now_playing= False, reset_loaded_song = False)
                self.load_and_play()
            case PS.PAUSED:
                self.stop_song(hide_now_playing = False, reset_loaded_song = False)
                self.player.load_song(self.player.loaded_song)
                self.set_state(PS.PAUSED)
                self.no_need_to_load = True
        

    def change_song(self, change):
        if self.player.loaded_song is None or self.window.playing_item is None:
            return
        if change == 0:
            return
        if change > 1 or change < -1:
            raise ValueError(f"Unexpected change value: ({change}). \nChange in function change_song must be between (-1) and (1)")
       
        current_index = self.window.listbox.row(self.window.playing_item)
        new_index = current_index + change

        if new_index > self.usable_length and change > 0:
            new_index = 0
        elif new_index < 0 and change < 0:
            new_index = self.usable_length

        new_item = self.window.listbox.item(new_index)

        match self.get_state():
            case PS.PLAYING:
                self.load_and_play(new_item)
            case PS.PAUSED:
                self.stop_song()


                self.window.update_listbox_UI(new_item = new_item)
                self.window.playing_item = new_item


                song = new_item.data(Qt.ItemDataRole.UserRole)
                self.player.load_song(song)
                self.set_state(PS.PAUSED)
                self.no_need_to_load = True
                self.window.see_item(new_item)

     
    
            
#endregion
#region UI Updating
    def get_state(self):
        return self.app.state
    
    def set_state(self, state: PS):
        self.window.set_state(state)

    def show_now_playing(self, text: str):
        self.window.show_now_playing(text)