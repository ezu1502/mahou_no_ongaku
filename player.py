import pygame
from pygame.mixer import music as Pymusic
import logging
from ENUMS import COLORS, painted_string, PS
from typing import Callable
from functools import wraps

log = logging.getLogger(painted_string("MahouPlayer ☾", COLORS.PURPLE))


class MahouPlayer:
    def __init__(self):
        pygame.mixer.init()
        log.debug("MahouPlayer initialized")

        self.window_set_state = None
        self.window_get_state = None

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

    def play_song(self, song_path):
        current_state = self.get_state()

        if current_state != PS.PLAYING:    
            Pymusic.load(song_path)
            Pymusic.play()

            self.set_state(PS.PLAYING)

            song_name = song_path.stem
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