from PySide6.QtWidgets import (QMainWindow, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup
from mahou_libs.time_functions import log_delta_time
from pathlib import Path
from mahou.core.enums import Themes
from mahou.user_interface.main_screen import MahouMainScreen

align = Qt.AlignmentFlag
size_policy = QSizePolicy.Policy

class MahouInterface(QMainWindow):
    @log_delta_time
    def __init__(self, app):
        super().__init__()
        
        self.app = app
        self.player = app.player

        self.user_options_dict = None

        self.WINDOW_TITLE = "MAHOU NO ONGAKU - True Music Player"
        WINDOW_WIDTH, WINDOW_HEIGHT = 900, 600

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.current_theme = None #implementar memória de cache pro tema
        self.set_theme(Themes.DARK)

        self.main_screen = MahouMainScreen(main_window = self, app = self.app)
        self.setCentralWidget(self.main_screen)

        self.setup_menu_bar()
    

    def load_stylesheet_string(self, style_path: Path | str):
        if isinstance(style_path, str):
            style_path = Path(style_path)

        return style_path.read_text(encoding = "utf-8")

    def set_theme(self, theme: Themes = Themes.DARK):
        if theme == self.current_theme:
            return 
        
        match theme:
            case Themes.DARK:
                style_path = Path(__file__).parent / "styles" / "dark_theme.qss"
            case Themes.LIGHT:
                style_path = Path(__file__).parent / "styles" / "light_theme.qss"
            case Themes.HABANERO:
                style_path = Path(__file__).parent / "styles" / "habanero_theme.qss"
            case _:
                style_path = Path(__file__).parent / "styles" / "dark_theme.qss"

        stylesheet_string = self.load_stylesheet_string(style_path)
        self.setStyleSheet(stylesheet_string)

        self.current_theme = theme

    def setup_menu_bar(self):
        self.menu_bar = self.menuBar()

        self.make_menubar_menus()

        self.set_file_menu()

        self.set_view_menu()

        self.set_themes_menu()

        self.set_shortcuts_menu()
        

    def make_menubar_menus(self):
        self.file_menu = self.menu_bar.addMenu("File")
        self.view_menu = self.menu_bar.addMenu("View")
        self.themes_menu = self.menu_bar.addMenu("Theme")
        self.shortcuts_menu = self.menu_bar.addMenu("Shortcuts")
        self.about_menu = self.menu_bar.addMenu("About")

    def set_file_menu(self):
        self.choose_folder_action = QAction("Choose Folder")
        self.choose_folder_action.setShortcut("Ctrl+O")
        self.choose_folder_action.triggered.connect(self.main_screen.choose_folder)

        self.file_menu.addAction(self.choose_folder_action)
        
    def set_view_menu(self):        
        self.view_restart_button = QAction("Restart Button")
        self.view_folder_button = QAction("Folder Button")

        self.view_restart_button.setCheckable(True)
        self.view_folder_button.setCheckable(True)

        self.view_restart_button.toggled.connect(self.main_screen.toggle_restart_button_visibility)
        self.view_folder_button.toggled.connect(self.main_screen.toggle_folder_button_visibility)


        if self.user_options_dict is not None:
            self.view_restart_button.setChecked(self.user_options_dict["restart"])
            self.view_folder_button.setChecked(self.user_options_dict["folder"])
        else:
            self.view_restart_button.setChecked(True)
            self.view_folder_button.setChecked(True)

        
        self.view_menu.addAction(self.view_restart_button)
        self.view_menu.addAction(self.view_folder_button)

    def set_themes_menu(self):
        self.themes_group = QActionGroup(self)

        self.dark_theme_action = QAction("Dark Theme")
        self.light_theme_action = QAction("Light Theme")
        self.habanero_theme_action = QAction("Habanero Theme")


        self.dark_theme_action.setCheckable(True)
        self.light_theme_action.setCheckable(True)
        self.habanero_theme_action.setCheckable(True)

        self.dark_theme_action.setChecked(True)

        self.themes_group.addAction(self.dark_theme_action)
        self.themes_group.addAction(self.light_theme_action)
        self.themes_group.addAction(self.habanero_theme_action)


        self.themes_group.setExclusive(True) #Só dá pra escolher 1 por vez

        self.themes_group.triggered.connect(self.on_theme_group_triggered)


        self.themes_menu.addActions(self.themes_group.actions())

    def set_shortcuts_menu(self):
        self.stop_song_shortcut = QAction("Stop Song - [S]")
        self.shortcuts_menu.addAction(self.stop_song_shortcut)


    def on_theme_group_triggered(self, action):
        match action:
            case self.dark_theme_action:
                self.set_theme(Themes.DARK)
            case self.light_theme_action:
                self.set_theme(Themes.LIGHT)
            case self.habanero_theme_action:
                self.set_theme(Themes.HABANERO)



