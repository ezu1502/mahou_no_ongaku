from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont
from mahou_libs.time_functions import log_delta_time

class MahouInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MAHOU NO ONGAKU - True Music Player")
        self.setFixedSize(900, 600)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.main_layout = QVBoxLayout()
        self.central.setLayout(self.main_layout)

        self.bahnschrift_title = QFont("Bahnschrift", 30)
        self.title = QLabel("Mahou no Ongaku")
        self.title.setFont(self.bahnschrift_title)
        self.main_layout.addWidget(self.title)

        self.test_button = QPushButton("PLAY")
        self.test_button.setFixedSize(100, 50)
        self.main_layout.addWidget(self.test_button)

