from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QListWidget,
QListWidgetItem, QGridLayout, QFileDialog, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QShortcut, QKeySequence
from mahou_libs.time_functions import log_delta_time
from pathlib import Path
from mahou.core.song import Song
from mahou.core.ENUMS import PS
from mahou.user_interface.player_bridge import PlayerBridge

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

        WINDOW_WIDTH, WINDOW_HEIGHT = 900, 600
        
        self.setWindowTitle("MAHOU NO ONGAKU - True Music Player")
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
        self.play_pause_button.pressed.connect(self.player_bridge.toggle)

        self.right_panel.addWidget(self.play_pause_button, alignment = align.AlignHCenter)

        # * FOLDER BUTTON ---
        self.folder_button = QPushButton("Choose Folder")
        self.folder_button.setFixedSize(300, 60)
        self.folder_button.pressed.connect(self.choose_folder)
        
        self.right_panel.addWidget(self.folder_button, alignment = align.AlignHCenter)

        # * RESTART SONG BUTTON --
        
        self.restart_button = QPushButton("Restart Song")
        self.restart_button.setFixedSize(300, 60)
        self.restart_button.pressed.connect(self.player_bridge.restart_song)
        self.right_panel.addWidget(self.restart_button, alignment = align.AlignHCenter)
        
        # * PREVIOUS/NEXT SONG BUTTONS

        self.previous_next_widget = QWidget()
        self.previous_next_widget.setFixedSize(300, 60)

        self.previous_next_layout = QHBoxLayout()
        self.previous_next_layout.setContentsMargins(0,0,0,0)
        self.previous_next_layout.setSpacing(20)

        self.previous_next_widget.setLayout(self.previous_next_layout)

        self.previous_button = QPushButton("Previous")
        self.previous_button.setFixedSize(145, 60)
        self.previous_button.pressed.connect(lambda: self.player_bridge.change_song(-1))


        self.next_button = QPushButton("Next")
        self.next_button.setFixedSize(145, 60)
        self.next_button.pressed.connect(lambda: self.player_bridge.change_song(1))

        self.previous_next_layout.addWidget(self.previous_button, alignment = align.AlignLeft)
        self.previous_next_layout.addWidget(self.next_button, alignment = align.AlignRight)

        self.right_panel.addWidget(self.previous_next_widget, alignment = align.AlignHCenter)

        for button in self.right_panel_widget.findChildren(QPushButton):
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            #isso impede que os meus keyboard shortcuts chamem funções dos próprios botões,
            #pra eu poder controlar as ações do player

        
        # * NOW PLAYING LABEL

        self.now_playing = QLabel("Now Playing: xxxx")
        self.now_playing.setAlignment(align.AlignHCenter)
        # self.now_playing.setMinimumWidth(0)

        self.now_playing.setSizePolicy(
            size_policy.Ignored, #eixo X
            size_policy.Minimum #eixo Y
        )

        self.now_playing.setWordWrap(True)
        self.now_playing.hide()
        self.right_panel.addWidget(self.now_playing)


        # * -------

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
    
    @property
    def listbox_selection(self):
        item = self.listbox.currentItem()
        return item
    
    def choose_folder(self):
        self.player_bridge.stop_song()
        folder = Path(QFileDialog.getExistingDirectory(self, "Choose a folder"))
        self.app.set_library_folder(folder)
        new_list = self.app.get_library_song_list

        self.set_listbox_list(new_list)
        
    
#endregion
#region UI Update
    def update_UI_by_state(self):
        match self.get_state():
            case PS.PAUSED | PS.IN_MENU:
                self.play_pause_button.setText("PLAY")
            case PS.PLAYING:
                self.play_pause_button.setText("PAUSE")

    def update_listbox_UI(self, new_item):
        
        if self.playing_item is not None:
            self.playing_item.setForeground(QBrush())
            
        new_item.setForeground(QColor("#FFC400"))
        new_item.setSelected(False)

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

    