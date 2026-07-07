from new_window import MahouWindow
from player import MahouPlayer
import logging
from ENUMS import PS
from colors import painted_string, COLORS

log = logging.getLogger(painted_string("MahouApp", "#FF00D4"))

class App:
    def __init__(self) -> None:

        self.state = PS.IN_MENU #DEFAULT STATE SET

        log.debug("App born")
        self.mahou_player = MahouPlayer()
        self.mahou_window = MahouWindow(self.mahou_player, dimensions = "900x600", app = self)
        log.debug("player and window created")

    def run(self):
        self.mahou_window.run()

    def set_state(self, state: PS) -> None:
        self.state = state
        if state != PS.SHUT_DOWN:
            log.debug(f"app state defined to {state}")
        
