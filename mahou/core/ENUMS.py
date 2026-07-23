from enum import Enum

class PS(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"
    WELCOME_SCREEN = "welcome_screen"
    IN_MENU = "in_menu"
    SHUT_DOWN = "shut_down"

class Themes(Enum):
    DARK = "main_theme"
    LIGHT = "light_theme"
    HABANERO = "habanero_theme"
    