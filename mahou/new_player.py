from pathlib import Path
from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from mahou.core.song import Song
from mahou.core.ENUMS import PS

PlayerState =  QMediaPlayer.PlaybackState

class MahouPlayer(QObject):
    state_changed = Signal()
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.loaded_song = None

        
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)

        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.playbackStateChanged.connect(self.handle_playback_state)

        self.current_song: Song | None = None
        

    def handle_playback_state(self, state: PlayerState):
        match state:
            case PlayerState.PlayingState:
                self.app.set_state(PS.PLAYING)
            case PlayerState.PausedState:
                self.app.set_state(PS.PAUSED)
            case PlayerState.StoppedState:
                self.app.set_state(PS.IN_MENU)

        self.state_changed.emit()


    def load_song(self, song: Song):
        path = song.path.resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Song path {path} does not exist or is not a valid song path")
        
        self.loaded_song = song
        
        path_url = QUrl.fromLocalFile(str(path))

        self.media_player.setSource(path_url)

        self.current_song = song

    def play_song(self):
        self.media_player.play()

    def pause_song(self):
        self.media_player.pause()

    def stop_song(self):
        self.media_player.stop()

    def set_pos(self, position):
        self.media_player.setPosition(position)
