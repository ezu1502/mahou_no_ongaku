from mahou.UI.new_window import MahouWindow
from mahou.player import MahouPlayer
import logging
from mahou.core.ENUMS import PS
from mahou_libs.colors import painted_string, COLORS

log = logging.getLogger(painted_string("app", "#FF00D4"))

class App:
    def __init__(self) -> None:

        self.state = PS.IN_MENU #DEFAULT STATE SET

        log.debug("App born")
        
        self.mahou_player = MahouPlayer(app = self)
        self.mahou_window = MahouWindow(self.mahou_player, dimensions = "900x600", app = self)

        log.debug("player and window created")

    def run(self):
        self.mahou_window.run()

    def set_state(self, state: PS) -> None:
        self.state = state
        if state != PS.SHUT_DOWN:
            log.debug(f"app state defined to {state}")
        
        
