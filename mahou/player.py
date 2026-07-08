import pygame
from pygame.mixer import music as Pymusic
import logging
from mahou.core.ENUMS import PS
from mahou.colors import COLORS, painted_string
from typing import Callable
from functools import wraps
from pathlib import Path

log = logging.getLogger(painted_string("mahou_player", COLORS.PURPLE))

class MahouPlayer:
    def __init__(self):
        pygame.mixer.init()
        log.debug("MahouPlayer initialized")

        self.window_set_state = None
        self.window_get_state = None

        self.loaded_song_path: Path | None = None

# ----------------- WINDOW STATE MANAGER

    def get_state(self) -> PS | None:
        if self.window_get_state is not None:
            return self.window_get_state()
        else:
            log.warning("Erro no callback da função get_state (Window)")
            return None
            
    def set_state(self, state: PS) -> None:
        if self.window_set_state is not None:
            self.window_set_state(state)
        else:
            log.warning("Erro no callback da função set_state (Window)")


# ------------------ MUSIC CONTROLS
    def load_song(self, song_path):
        Pymusic.load(song_path)
        if song_path is not None:
            self.loaded_song_path = Path(song_path)
            log.debug(f"loaded {self.loaded_song_path.stem} into MahouPlayer")


    def play_song(self):
        current_state = self.get_state()

        if current_state != PS.PLAYING:    
            Pymusic.play()

            self.set_state(PS.PLAYING)

            if self.loaded_song_path is not None:
                song_name = self.loaded_song_path.stem
            else:
                log.warning("Loaded song path is None!")
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
