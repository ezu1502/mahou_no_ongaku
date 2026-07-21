from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QListWidget,
QListWidgetItem, QGridLayout, QFileDialog, QSizePolicy, QSlider)
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QShortcut, QKeySequence, QAction
from mahou_libs.time_functions import log_delta_time
from pathlib import Path
from mahou.core.song import Song
from mahou.core.ENUMS import PS
from mahou.user_interface.player_bridge import PlayerBridge
from mahou_libs.mahou_math import conversions

import json


align = Qt.AlignmentFlag
size_policy = QSizePolicy.Policy

class MahouInterface(QMainWindow):
    @log_delta_time
    def __init__(self, player, app):
        super().__init__()
        
        self.player = player
        self.app = app
        self.player_bridge = PlayerBridge(window = self)

        self.playing_item = None
        self.user_options_dict = None

        self.WINDOW_TITLE = "MAHOU NO ONGAKU - True Music Player"
        self.setWindowTitle(self.WINDOW_TITLE)

        WINDOW_WIDTH, WINDOW_HEIGHT = 900, 600
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        style_path = Path(__file__).parent / "styles" / "mahou_main_theme.qss"
        self.setStyleSheet(self.load_stylesheet_string(style_path))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
    
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(align.AlignTop)
        self.central_widget.setLayout(self.main_layout)

        self.set_interface_aspect()
        self.set_shortcuts()
        self.setup_menu_bar()


        
    

    def handle_duration_changed(self, duration):
        self.progress_bar.setMaximum(duration)

        duration_string = conversions.seconds_to_base60(duration/1000)
        self.duration_label.setText(f"{duration_string}")

    def handle_position_changed(self, position): #esse acha a posição depois do usuario arrastar
        if not self.progress_bar.isSliderDown(): #IsSliderDown significa que o usuario ta segurando
            self.progress_bar.setValue(position)
            position_string = conversions.seconds_to_base60(position/1000)
            self.position_label.setText(f"{position_string}")

    def set_position_string(self, position): #Esse monitora a posição do slider
        position_string = conversions.seconds_to_base60(position/1000)
        self.position_label.setText(f"{position_string}")

    def set_slider_position(self):
        position = self.progress_bar.value()
        self.player.set_pos(position)

   

    def set_shortcuts(self):
        self.toggle_key = QShortcut(QKeySequence("Space"), self)
        self.toggle_key.activated.connect(self.player_bridge.toggle)

        self.stop_key = QShortcut(self)
        self.stop_key.setKeys([QKeySequence("Escape"), QKeySequence("S")])
        self.stop_key.activated.connect(self.player_bridge.stop_song)

        self.left_key = QShortcut(QKeySequence("Left"), self)
        self.left_key.activated.connect(lambda: self.player_bridge.change_song(-1))

        self.right_key = QShortcut(QKeySequence("Right"), self)
        self.right_key.activated.connect(lambda: self.player_bridge.change_song(1))

        self.enter_key = QShortcut(QKeySequence("Return"), self)
        self.enter_key.activated.connect(self.player_bridge.load_and_play)

    
    def setup_menu_bar(self):
        self.menu_bar = self.menuBar()

        self.file_menu = self.menu_bar.addMenu("File")
        self.view_menu = self.menu_bar.addMenu("View")
        self.themes_menu = self.menu_bar.addMenu("Theme")
        self.shortcuts_menu = self.menu_bar.addMenu("Shortcuts")
        self.about_menu = self.menu_bar.addMenu("About")

        self.choose_folder_action = QAction("Choose Folder")
        self.choose_folder_action.setShortcut("Ctrl+O")
        self.choose_folder_action.triggered.connect(self.choose_folder)

        self.view_restart_button = QAction("Restart Button")
        self.view_restart_button.setCheckable(True)
        self.view_restart_button.toggled.connect(self.toggle_restart_button_visibility)

        self.view_folder_button = QAction("Folder Button")
        self.view_folder_button.setCheckable(True)
        self.view_folder_button.toggled.connect(self.toggle_folder_button_visibility)


        if self.user_options_dict is not None:
            self.view_restart_button.setChecked(self.user_options_dict["restart"])
            self.view_folder_button.setChecked(self.user_options_dict["folder"])
        else:
            self.view_restart_button.setChecked(True)
            self.view_folder_button.setChecked(True)


        self.dark_theme_action = QAction("Dark Theme")
        self.light_theme_action = QAction("Light Theme")
        
        self.themes_menu.addAction(self.dark_theme_action)
        self.themes_menu.addAction(self.light_theme_action)

        self.view_menu.addAction(self.view_restart_button)
        self.view_menu.addAction(self.view_folder_button)

        self.file_menu.addAction(self.choose_folder_action)



    def toggle_restart_button_visibility(self, checked):
        if checked:
            self.restart_button.show()
        else:
            self.restart_button.hide()

        self.save_personalized_options()

    def toggle_folder_button_visibility(self, checked):
        if checked:
            self.folder_button.show()
        else:
            self.folder_button.hide()

        self.save_personalized_options()
        


    def save_personalized_options(self):
        options_save_file = Path ("mahou_cache") / ("app_cache") / "user_settings.json"

        view_restart = self.view_restart_button.isChecked()
        view_folder = self.view_folder_button.isChecked()

        options = {
            "view restart": view_restart,
            "view folder": view_folder,
        }

        with options_save_file.open("w", encoding = "utf-8") as save:
            json.dump(options, save, ensure_ascii = True, indent = 4)

    def load_personalized_options(self):
        options_save_file = Path ("mahou_cache") / ("app_cache") / "user_settings.json"
        valid = options_save_file.exists() and options_save_file.is_file()
        
        if not valid:
            return
        
        with options_save_file.open("r", encoding = "utf-8") as options:
            option_dict = json.load(options)

        restart_visible = option_dict["view restart"]
        folder_visible = option_dict["view folder"]

        self.restart_button.setVisible(restart_visible)
        self.folder_button.setVisible(folder_visible)

        self.user_options_dict = {
            "restart" : restart_visible,
            "folder": folder_visible
        }



    
            


    @log_delta_time
    def set_interface_aspect(self):
        
        # * TÍTULO -------
        self.title = QLabel("Mahou no Ongaku")
        self.title.setObjectName("title")
        self.main_layout.addWidget(self.title, 2, alignment = align.AlignHCenter)

        # * PÁGINA DO MEIO/ 
        self.middle_layout = QHBoxLayout()
        self.main_layout.addLayout(self.middle_layout, 14)
        
        # * LISTBOX ---

        self.listbox = QListWidget()
        self.listbox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.listbox.setAlternatingRowColors(True)
        self.listbox.setUniformItemSizes(True)
        self.listbox.itemSelectionChanged.connect(self.manage_play_selected_button)

        self.middle_layout.addWidget(self.listbox, 9)
    
        # * RIGHT PANEL/
        

        self.right_panel_widget = QWidget()
        self.right_panel_widget.setMinimumWidth(0)
        self.right_panel_widget.setContentsMargins(0, 0, 0, 0)

        self.right_panel_widget.setSizePolicy(
            size_policy.Expanding,
            size_policy.Preferred
        )

        self.right_panel = QVBoxLayout()
        self.right_panel.setAlignment(align.AlignTop)
        self.right_panel.setSpacing(15)
        self.right_panel.setContentsMargins(10, 0, 10, 0)

        self.right_panel_widget.setLayout(self.right_panel)

        self.middle_layout.addWidget(self.right_panel_widget, 8)

        # * PLAY AND PAUSE BUTTON ---

        self.play_pause_button = QPushButton("PLAY")
        self.play_pause_button.setFixedSize(300, 60)
        self.play_pause_button.clicked.connect(self.player_bridge.toggle)
        self.play_pause_button.setObjectName("play_button")

        self.right_panel.addWidget(self.play_pause_button, alignment = align.AlignHCenter)

        # * FOLDER BUTTON ---
        self.folder_button = QPushButton("Choose Folder")
        self.folder_button.setFixedSize(300, 60)
        self.folder_button.clicked.connect(self.choose_folder)
        
        self.right_panel.addWidget(self.folder_button, alignment = align.AlignHCenter)

        # * RESTART SONG BUTTON --
        
        self.restart_button = QPushButton("Restart Song")
        self.restart_button.setFixedSize(300, 60)
        self.restart_button.pressed.connect(self.player_bridge.restart_song)

        self.restart_button.setEnabled(False)


        self.right_panel.addWidget(self.restart_button, alignment = align.AlignHCenter)

        # This loads user's preferences about the buttons visibility
        self.load_personalized_options()
        
        # * PREVIOUS/NEXT SONG BUTTONS

        self.previous_next_widget = QWidget()
        self.previous_next_widget.setFixedSize(300, 60)

        self.previous_next_layout = QHBoxLayout()
        self.previous_next_layout.setContentsMargins(0,0,0,0)
        self.previous_next_layout.setSpacing(10)

        self.previous_next_widget.setLayout(self.previous_next_layout)

        self.previous_button = QPushButton("Previous")
        self.previous_button.setFixedSize(145, 60)
        self.previous_button.pressed.connect(lambda: self.player_bridge.change_song(-1))


        self.next_button = QPushButton("Next")
        self.next_button.setFixedSize(145, 60)
        self.next_button.pressed.connect(lambda: self.player_bridge.change_song(1))

        self.previous_button.setEnabled(False)
        self.next_button.setEnabled(False)


        self.previous_next_layout.addWidget(self.previous_button, alignment = align.AlignLeft)
        self.previous_next_layout.addWidget(self.next_button, alignment = align.AlignRight)

        self.right_panel.addWidget(self.previous_next_widget, alignment = align.AlignHCenter)

        # * PLAY SELECTED BUTTON -------
        self.play_selected_button = QPushButton("Play Selected Song")
        self.play_selected_button.setFixedSize(300, 50)
        self.play_selected_button.pressed.connect(self.player_bridge.play_selected)
        self.play_selected_button.setEnabled(False)
        self.right_panel.addWidget(self.play_selected_button, alignment = align.AlignHCenter)

        # * Revoking button focus ---------
        for button in self.right_panel_widget.findChildren(QPushButton):
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            #isso impede que os meus keyboard shortcuts chamem funções dos próprios botões,
            #pra eu poder controlar as ações do player

        # * PROGRESS BAR
        self.bar_and_numbers_layout = QVBoxLayout()
        self.bar_and_numbers_layout.setSpacing(5)

        self.progress_bar = QSlider(Qt.Orientation.Horizontal)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(320)

        self.player.duration_changed.connect(self.handle_duration_changed)
        self.player.position_changed.connect(self.handle_position_changed)

        self.progress_bar.sliderMoved.connect(self.set_position_string)
        self.progress_bar.sliderReleased.connect(self.set_slider_position)

        self.right_panel.addSpacing(7)

        self.bar_and_numbers_layout.addWidget(self.progress_bar, alignment = align.AlignHCenter)

        # * PROGRESS LABEL

        self.progress_widget = QWidget()
        self.progress_widget.setFixedSize(300, 18)

        self.progress_layout = QHBoxLayout()
        self.progress_layout.setContentsMargins(0,0,0,0)
        self.progress_layout.setSpacing(10)

        self.progress_widget.setLayout(self.progress_layout)

        self.position_label = QLabel("0:00")
        self.duration_label = QLabel("0:00")

        # self.position_label.hide()
        # self.duration_label.hide()

        self.progress_layout.addWidget(self.position_label, alignment = align.AlignLeft)
        self.progress_layout.addWidget(self.duration_label, alignment = align.AlignRight)

    
        self.bar_and_numbers_layout.addWidget(self.progress_widget, alignment = align.AlignHCenter)

        self.right_panel.addLayout(self.bar_and_numbers_layout)
        
 # * NOW PLAYING LABEL

        self.right_panel.addSpacing(7)

        self.now_playing = QLabel("Now Playing: xxxx")
        self.now_playing.setAlignment(align.AlignHCenter)
        # self.now_playing.setMinimumWidth(0)

        self.now_playing.setSizePolicy(
            size_policy.Ignored, #eixo X
            size_policy.Minimum #eixo Y
        )

        self.now_playing.setWordWrap(True)
        self.now_playing.hide()
        self.right_panel.addWidget(self.now_playing, alignment = align.AlignTop)

        





        # * -------------

        self.set_listbox_list(self.song_list)

        # * ------------------------------


#region LIST REGION

    @property
    def apps_music_list(self):
        return self.app.library.song_list

    @log_delta_time
    def set_listbox_list(self, list_to_add: list[Song]):
        if list_to_add is None:
            return
        
        self.listbox.clear()

        for item in list_to_add:
            song_item = QListWidgetItem(item.title)
            song_item.setData(Qt.ItemDataRole.UserRole, item)
            self.listbox.addItem(song_item)

   
    @property
    def song_list(self):
        return self.app.library.song_list
    

    def get_listbox_selection(self):
        selected_items = self.listbox.selectedItems()
        item = selected_items[0] if selected_items else None  
        return item
    

    def choose_folder(self):
        folder_string = QFileDialog.getExistingDirectory(self, "Choose a folder")
        if not folder_string: 
            return
        
        folder = Path(folder_string)

        self.app.set_library_folder(folder)
        new_list = self.app.get_library_song_list

        self.player_bridge.stop_song()

        self.set_listbox_list(new_list)
        
    
#endregion
#region UI Update
    def update_UI_by_state(self):
        match self.get_state():
            case PS.PAUSED:
                self.play_pause_button.setText("PLAY")

                self.next_button.setEnabled(True)
                self.previous_button.setEnabled(True)
                self.restart_button.setEnabled(True)

            case PS.IN_MENU:
                self.play_pause_button.setText("PLAY")

                self.next_button.setEnabled(False)
                self.previous_button.setEnabled(False)
                self.restart_button.setEnabled(False)

                self.duration_label.setText("0:00")

                self.reset_listbox_UI()

            case PS.PLAYING:
                self.play_pause_button.setText("PAUSE")

                self.next_button.setEnabled(True)
                self.previous_button.setEnabled(True)
                self.restart_button.setEnabled(True)        


    def update_listbox_UI(self, new_item):
        if self.playing_item is not None:
            self.playing_item.setForeground(QBrush())
            
        
        new_item.setForeground(QColor("#FFC400"))
        new_item.setSelected(False)


    def manage_play_selected_button(self):
        selected_items = self.listbox.selectedItems()
        item = selected_items[0] if selected_items else None  
        
        
        self.play_selected_button.setEnabled(item is not self.playing_item and item is not None)


    def reset_listbox_UI(self):
        if self.playing_item is None:
            return
        
        self.playing_item.setForeground(QBrush())

    def song_list_length(self) -> int:
        return len(self.app.library.song_list)

    def get_state(self) -> PS:
        return self.app.state
    
    def set_state(self, state: PS):
        self.app.state = state
        self.update_UI_by_state()

    def see_item(self, item) -> None:
        self.listbox.scrollToItem(item)


    def show_now_playing(self, text: str) -> None:

        self.now_playing.setText(f'Now Playing: <span style = "color: #FFC400">{text}</span>')

        if self.now_playing.isVisible():
            return
        
        self.now_playing.show()
        
    def hide_now_playing(self) -> None:
        if not self.now_playing.isVisible():
            return
        
        self.now_playing.hide()

    #endregion

    #region STYLESHEET

    def load_stylesheet_string(self, style_path: Path | str):
        if isinstance(style_path, str):
            style_path = Path(style_path)

        return style_path.read_text(encoding = "utf-8")
    
    #endregion

    