import pygame
from pygame.mixer import music as Pymusic
from mahou.core.ENUMS import PS
from mahou_libs.colors import COLORS, painted_string
from typing import Callable
from functools import wraps
from pathlib import Path
from mahou.core.song import Song
from bunseki import Analyzer
from mahou_libs.bocca import BoccaFiglia

log = BoccaFiglia("mahou_player", COLORS.PURPLE)

def analyze(song_obj):
    song_analysis = song_obj.analysis
    
    if song_analysis is None and song_obj.cache_dict is None:
        song_obj._analysis = Analyzer(song_obj.path)

    log.trace(song_obj.analysis)


class MahouPlayer:
    def __init__(self, app):
        pygame.mixer.init()
        log.trace("MahouPlayer initialized")

        self.app = app
        self.loaded_song: Song | None = None

# ----------------- WINDOW STATE MANAGER

    def get_state(self) -> PS | None:
        return self.app.state
            
    def set_state(self, state: PS) -> None:
        self.app.set_state(state)


# ------------------ MUSIC CONTROLS
    def load_song(self, song: Song):
        if not isinstance(song, Song):
            raise ValueError(f"Argument {song} is not a Song object!")
        
        self.loaded_song = song

        if song._analysis is None:
            log.trace("None")
            analyze(song)
            
        if not song.has_cache:
            song.save_analyzer_data_cache()
            
        path = song.path
        Pymusic.load(path)
        log.trace(f"loaded {path} into MahouPlayer")
         
    def play_song(self):
        current_state = self.get_state()

        if current_state != PS.PLAYING:    
            Pymusic.play()
            self.set_state(PS.PLAYING)
            song_name = self.loaded_song.title if self.loaded_song is not None else None
            log.info(painted_string(f"Now Playing: {song_name}", COLORS.PURPLE))
        else:
            log.warning("Already playing!")

    def pause_song(self):
        current_state = self.get_state()
        if current_state != PS.PAUSED:
            Pymusic.pause()
            self.set_state(PS.PAUSED)
        else:
            log.warning("Already paused")

    def unpause_song(self) -> None:
        Pymusic.unpause()
        self.set_state(PS.PLAYING)

    def stop_song(self) -> None:
        Pymusic.stop()
        self.set_state(PS.IN_MENU)

    def play_without_load(self):
        Pymusic.play()
        self.set_state(PS.PLAYING)

    def get_song_pos(self):
        return Pymusic.get_pos() / 1000





    

    