from mahou.UI.new_window import MahouWindow
from mahou.player import MahouPlayer
from mahou.core.ENUMS import PS
from mahou_libs.colors import painted_string, COLORS
from mahou_libs.bocca import BoccaFiglia

from PySide6.QtWidgets import QApplication
import sys
from mahou.UI2.window import MahouInterface
from mahou_libs.time_functions import log_delta_time
log = BoccaFiglia("app", "#FF00D4")
import time
class App:
    def __init__(self) -> None:

        self.state = PS.IN_MENU #DEFAULT STATE SET

        log.trace("App born")
        
        self.mahou_player = MahouPlayer(app = self)
        
        
        self.qt_app = QApplication(sys.argv)
        
       
        self.mahou_window = MahouInterface()
        t = time.perf_counter()
        self.mahou_window.show()
        f = time.perf_counter()

        print(f-t)
        
        self.qt_app.exec()


    def run(self):
        # self.mahou_window.run()
        pass

    def set_state(self, state: PS) -> None:
        self.state = state
        if state != PS.SHUT_DOWN:
            log.debug(f"app state defined to {state}")
    
