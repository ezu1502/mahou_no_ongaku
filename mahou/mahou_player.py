from pygame import mixer as pymixer
from pygame.mixer import music as pymusic
from mahou.core.song import Song
from mahou.core.ENUMS import PS

class MahouPlayer:
    def __init__(self, app) -> None:
        self.app = app
        pymixer.init()
        self.loaded_song = None

    def load_song(self, song: Song):
        self.loaded_song = song

        if self.loaded_song is None:
            return 
        
        song_path = song.path
        
        if song_path is None:
            return
        pymusic.load(song_path)

    def play_song(self):
        pymusic.play()
        self.app.set_state(PS.PLAYING)


    def pause_song(self):
        pymusic.pause()
        self.app.set_state(PS.PAUSED)

    def unpause_song(self):
        pymusic.unpause()
        self.app.set_state(PS.PLAYING)

    def stop_song(self):
        pymusic.stop()
        self.loaded_song = None
        self.app.set_state(PS.IN_MENU)