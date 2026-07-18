from mahou.core.ENUMS import PS
from PySide6.QtGui import Qt, QColor, QBrush

#region PLAYER CONTROLS
class PlayerBridge:
    def __init__(self, window):
        self.window = window
        self.player = self.window.player
        self.app = self.window.app
        

    def toggle(self):
        match self.get_state():
            case PS.PLAYING:
                self.player.pause_song()
            case PS.PAUSED:
                self.player.unpause_song()
            case PS.IN_MENU:
                self.load_and_play()
        self.window.update_UI_by_state()


    def load_and_play(self):
        item = self.window.listbox_selection
        if item is None:
            return
        
        self.window.update_listbox_UI(new_item = item)

        self.window.playing_item = item

        song = item.data(Qt.ItemDataRole.UserRole)
  
        if song is None:
            return
    
        self.player.load_song(song)
        self.player.play_song()

    def stop_song(self):
        ...

    def restart_song(self):
        self.stop_song
        
#endregion
#region UI Updating
    def get_state(self):
        return self.app.state
    
    def set_state(self, state: PS):
        self.window.set_state(state)