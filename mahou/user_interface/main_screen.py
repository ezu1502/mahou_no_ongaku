#PYSIDE6 IMPORTS
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QListWidget,
QListWidgetItem, QGridLayout, QFileDialog, QSizePolicy, QSlider)
from PySide6.QtGui import QBrush, QColor, QShortcut, QKeySequence, QAction
from PySide6.QtCore import Qt
from mahou_libs.time_functions import log_delta_time
from mahou_libs.mahou_math import conversions
from mahou.user_interface.player_bridge import PlayerBridge
from mahou.core.song import Song
from mahou.core.enums import PS, Paths, Themes
from pathlib import Path
import json
from mahou import file_manager

align = Qt.AlignmentFlag
size_policy = QSizePolicy.Policy

HIGHLIGHT_COLORS = {
    Themes.DARK: "#FFC400",
    Themes.LIGHT: "#7F00D3",
    Themes.HABANERO: "#EF3300"
}



class MahouMainScreen(QWidget):
    def __init__(self, main_window, app) -> None:
        super().__init__()

        self.main_window = main_window
        self.app = app

        self.player = app.player
        self.bridge = PlayerBridge(master = self)

        self.playing_item = None

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(align.AlignTop)
        self.setLayout(self.main_layout)

        self.set_interface_aspect()
        self.set_keyboard_shortcuts()

        self.current_song_title = None


# region SIGNAL HANDLERS

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

    def toggle_restart_button_visibility(self, checked):
        if checked:
            self.restart_button.show()
        else:
            self.restart_button.hide()

        self.save_view_options()

    def toggle_folder_button_visibility(self, checked):
        if checked:
            self.folder_button.show()
        else:
            self.folder_button.hide()

        self.save_view_options()

    def manage_play_selected_button(self):
        selected_items = self.listbox.selectedItems()
        item = selected_items[0] if selected_items else None  
        
        
        self.play_selected_button.setEnabled(item is not self.playing_item and item is not None)

    def show_now_playing(self, text: str = "None", just_update_color = False) -> None:
        color = self.get_highlight_color()

        if just_update_color:
            if not self.now_playing.isVisible() or self.current_song_title is None:
                return
            text = self.current_song_title

        self.current_song_title = text

        self.now_playing.setText(f'Now Playing: <span style = "color: {color}">{text}</span>')

        if self.now_playing.isVisible():
            return

        self.now_playing.show()


 

        
        
    def hide_now_playing(self) -> None:
        if not self.now_playing.isVisible():
            return
        
        self.now_playing.hide()

#endregion
#region UI BUILDING

    def set_keyboard_shortcuts(self):
        self.toggle_key = QShortcut(QKeySequence("Space"), self)
        self.toggle_key.activated.connect(self.bridge.toggle)

        self.stop_key = QShortcut(self)
        self.stop_key.setKeys([QKeySequence("Escape"), QKeySequence("S")])
        self.stop_key.activated.connect(self.bridge.stop_song)

        self.left_key = QShortcut(QKeySequence("Left"), self)
        self.left_key.activated.connect(lambda: self.bridge.change_song(-1))

        self.right_key = QShortcut(QKeySequence("Right"), self)
        self.right_key.activated.connect(lambda: self.bridge.change_song(1))

        self.enter_key = QShortcut(QKeySequence("Return"), self)
        self.enter_key.activated.connect(self.bridge.load_and_play)

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
        self.play_pause_button.pressed.connect(self.bridge.toggle)
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
        self.restart_button.pressed.connect(self.bridge.restart_song)

        self.restart_button.setEnabled(False)


        self.right_panel.addWidget(self.restart_button, alignment = align.AlignHCenter)

        # This loads user's preferences about the buttons visibility
        self.load_view_options()
        
        # * PREVIOUS/NEXT SONG BUTTONS

        self.previous_next_widget = QWidget()
        self.previous_next_widget.setFixedSize(300, 60)

        self.previous_next_layout = QHBoxLayout()
        self.previous_next_layout.setContentsMargins(0,0,0,0)
        self.previous_next_layout.setSpacing(10)

        self.previous_next_widget.setLayout(self.previous_next_layout)

        self.previous_button = QPushButton("Previous")
        self.previous_button.setFixedSize(145, 60)
        self.previous_button.pressed.connect(lambda: self.bridge.change_song(-1))


        self.next_button = QPushButton("Next")
        self.next_button.setFixedSize(145, 60)
        self.next_button.pressed.connect(lambda: self.bridge.change_song(1))

        self.previous_button.setEnabled(False)
        self.next_button.setEnabled(False)


        self.previous_next_layout.addWidget(self.previous_button, alignment = align.AlignLeft)
        self.previous_next_layout.addWidget(self.next_button, alignment = align.AlignRight)

        self.right_panel.addWidget(self.previous_next_widget, alignment = align.AlignHCenter)

        # * PLAY SELECTED BUTTON -------
        self.play_selected_button = QPushButton("Play Selected Song")
        self.play_selected_button.setFixedSize(300, 50)
        self.play_selected_button.pressed.connect(self.bridge.play_selected)
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
        self.now_playing.setObjectName("now_playing")
        self.right_panel.addWidget(self.now_playing, alignment = align.AlignTop)

        # * -------------

        self.set_listbox_list(self.song_list)

        # * ------------------------------

#endregion
#region SAVE/LOAD options

    def save_view_options(self) -> None:
        view_restart = self.main_window.view_restart_button.isChecked()
        view_folder = self.main_window.view_folder_button.isChecked()

        view_options = {
            "restart_button": view_restart,
            "folder_button": view_folder,
        }

        file_manager.save_setting(view_options, "view")

    def load_view_options(self) -> None:
        option_dict = file_manager.read_file(Paths.SETTINGS_FILE)

        view_options = option_dict.get("view", {}) #get vai tentar puxar um parametro e retorna o segundo se n achar

        restart_visible = view_options.get("restart_button", True)
        folder_visible = view_options.get("folder_button", True)

        self.restart_button.setVisible(restart_visible)
        self.folder_button.setVisible(folder_visible)

        self.main_window.user_options_dict = {
            "restart_button" : restart_visible,
            "folder_button": folder_visible
        }


#endregion
#region LIST REGION
    @log_delta_time
    def set_listbox_list(self, list_to_add: list[Song]):
        if list_to_add is None:
            return
        
        self.listbox.clear()

        for item in list_to_add:
            song_item = QListWidgetItem(item.title)
            song_item.setData(Qt.ItemDataRole.UserRole, item)
            self.listbox.addItem(song_item)

    def song_list_length(self) -> int:
        return len(self.app.library.song_list)
    
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

        self.bridge.stop_song()

        self.set_listbox_list(new_list)
    
    @property
    def song_list(self):
        return self.app.library.song_list

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

    def get_highlight_color(self):
        theme = self.main_window.current_theme
        color = HIGHLIGHT_COLORS.get(theme, "#FF0000")
        return color
    def update_listbox_UI(self, new_item):
        if self.playing_item is not None:
            self.playing_item.setForeground(QBrush())
            
        color = self.get_highlight_color()
        new_item.setForeground(QColor(color))
        new_item.setSelected(False)

    def update_highlight_theme(self, theme):
        if self.playing_item is None:
            return
        
        color = HIGHLIGHT_COLORS.get(theme, "#FF0000")
        self.playing_item.setForeground(QColor(color))
        self.playing_item.setSelected(False)

    def reset_listbox_UI(self):
        if self.playing_item is None:
            return
        
        self.playing_item.setForeground(QBrush())

    def see_item(self, item) -> None:
        self.listbox.scrollToItem(item)


#region state
    def get_state(self) -> PS:
        return self.app.state
