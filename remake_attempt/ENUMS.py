from enum import Enum, StrEnum

class PS(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"
    WELCOME_SCREEN = "welcome_screen"
    IN_MENU = "in_menu"
    SHUT_DOWN = "shut_down"




def ansi(code: str) -> str:
    return f"\033[{code}"

class COLORS(StrEnum):
    RESET = ansi("0m")
    WHITE = ansi("37m")
    RED = ansi("31m")
    GREEN = ansi("32m")
    BLUE = ansi("34m")
    PURPLE = ansi ("35m")
    ORANGE = ansi ("38;5;208m")
        
def painted_string(string: str, color: COLORS = COLORS.WHITE) -> str:
    colored_text = f"{color}{string}{COLORS.RESET} "
    return colored_text