from mahou.core.enums import PS
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Qt
from mahou_libs.time_functions import log_delta_time

#region PLAYER CONTROLS
class PlayerBridge:
    def __init__(self, master):
        self.master = master

        self.player = self.master.player
        self.player.state_changed.connect(self.master.update_UI_by_state)
        self.player.song_ended.connect(lambda: self.change_song(1))


        self.app = self.master.app

        self.no_need_to_load = False

    @log_delta_time
    def toggle(self):
        match self.get_state():
            case PS.PLAYING:
                self.player.pause_song()
            case PS.PAUSED:
                self.player.play_song()
            case PS.IN_MENU:
                self.load_and_play()



    def load_and_play(self, specific_item = None, play = True):
        if specific_item is None:
            item = self.master.get_listbox_selection()
            if item is None:
                return
        else:
            item = specific_item
        
       
        song = item.data(Qt.ItemDataRole.UserRole)
  
        if song is None:
            return
    
        self.player.load_song(song)
        if play:
            self.player.play_song()


        self.master.update_listbox_UI(new_item = item)
        
        self.master.playing_item = item


        self.master.see_item(item)

        song_title = song.title
        self.show_now_playing(song_title)
        self.set_window_title(song_title = song_title)

        # if self.master.position_label.isHidden() or self.master.duration_label.isHidden():
        #     self.master.position_label.show()
        #     self.master.duration_label.show()   


    def play_selected(self):
        self.load_and_play()
        # self.master.update_UI_by_state()

    def play_without_loading(self):
        self.player.play_song()

    def stop_song(self):
        self.player.stop_song()
    
        self.master.hide_now_playing()
        self.master.reset_listbox_UI()
        self.master.playing_item = None
        self.master.manage_play_selected_button()
        self.app.set_state(PS.IN_MENU)
        
        self.master.update_UI_by_state()
        self.set_window_title(reset = True)
        
    
    def set_window_title(self, song_title = None, reset = False):
        if reset:
            self.master.setWindowTitle(self.master.WINDOW_TITLE)
            return
        
        MAX_SIZE = 37
        if song_title is None:
            return
        
        if len(song_title) > MAX_SIZE:
            song_title = song_title[:MAX_SIZE - 1] + "…"

        if song_title:
            self.master.setWindowTitle(f"{song_title} - MAHOU NO ONGAKU")


    def restart_song(self):
        self.player.set_pos(0)
        

    def change_song(self, change):
        if self.player.loaded_song is None or self.master.playing_item is None:
            return
        if change == 0:
            return
        if change not in (-1, 1):
            raise ValueError(f"Unexpected change value: ({change}). \nChange in function change_song must be between (-1) and (1)")
        
        item_count = self.master.listbox.count()
        if item_count == 0:
            return
        
        current_index = self.master.listbox.row(self.master.playing_item)
        new_index = (current_index + change) % item_count

        new_item = self.master.listbox.item(new_index)

        if new_item is None:
            return

        match self.get_state():
            case PS.PLAYING | PS.IN_MENU:
                self.load_and_play(new_item)
            case PS.PAUSED:
                self.load_and_play(new_item)
                self.player.pause_song()


    
            
#endregion
#region UI Updating
    def get_state(self):
        return self.app.state
    
    def set_state(self, state: PS):
        self.app.set_state(state)

    def show_now_playing(self, text: str):
        self.master.show_now_playing(text)