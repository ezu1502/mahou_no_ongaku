from mahou.new_player import MahouPlayer
from mahou.core.enums import PS, Paths
from mahou.user_interface.window import MahouInterface
from mahou_libs.time_functions import log_delta_time, first_point, second_point
from PySide6.QtWidgets import QApplication
from mahou.core.song_library import SongLibrary
import sys
import time
from mahou import file_manager as FM


class App:
    @log_delta_time
    def __init__(self) -> None:
        self.state = PS.IN_MENU #DEFAULT STATE SET

        self.library = SongLibrary() #library
        folder = self.library.folder

        if folder is not None:
            self.library.set_song_list(folder) #song_list
        
        self.qt_app = QApplication(sys.argv) #qt app
        self.player = MahouPlayer(app = self) #player
        self.mahou_window = MahouInterface(app = self) #mainwindow

        first = first_point()

        self.mahou_window.show()

        second_point(first)


        

        
    def run(self):
        self.qt_app.exec()
        pass

    def set_state(self, state: PS) -> None:
        self.state = state

    
    def set_library_folder(self, folder):
        self.library.set_folder(folder)
    
    @property
    def get_library_song_list(self):
        return self.library.song_list
    
