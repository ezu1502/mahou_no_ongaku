from pathlib import Path
from PySide6.QtCore import QObject, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from mahou.core.song import Song
from mahou.core.ENUMS import PS

class MahouPlayer(QObject):
    def init(self, app):
        self.app = app
        
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)

        self.media_player.setAudioOutput(self.audio_output)

        self.current_song: Song | None = None


    def load_song(self, song: Song):
        path = song.path.resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Song path {path} does not exist or is not a valid song path")
        
        path_string = str(path)
        path_url = QUrl.fromLocalFile(path_string)

        self.media_player.setSource(path_url)

        self.current_song = song

    def play_song(self):
        self.media_player.play()
        self.app.set_state(PS.PLAYING)

    def pause_song(self):
        self.media_player.pause()
        self.app.set_state(PS.PAUSED)

    def stop_song(self):
        self.media_player.stop()

