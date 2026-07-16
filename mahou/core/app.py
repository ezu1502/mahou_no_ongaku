from mahou.player import MahouPlayer
from mahou.core.ENUMS import PS
from mahou.UI2.window import MahouInterface
from mahou_libs.time_functions import log_delta_time
from PySide6.QtWidgets import QApplication
import sys

class App:
    def __init__(self) -> None:

        self.state = PS.IN_MENU #DEFAULT STATE SET

        
        self.mahou_player = MahouPlayer(app = self)
        
        self.qt_app = QApplication(sys.argv)
        
       
        self.mahou_window = MahouInterface()
        self.mahou_window.show()
        


    def run(self):
        self.qt_app.exec()
        pass

    def set_state(self, state: PS) -> None:
        self.state = state
        if state != PS.SHUT_DOWN:
            ...
            # log.debug(f"app state defined to {state}")
    
