import os; os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import logging
from functools import wraps
# from mahou import PS, MahouPlayer, MahouWindow # NÃO USADOS AINDA, MAS JÁ COMENTADOS AQUI PRA FACILITAR DEPOIS
from mahou import COLORS, painted_string, App

logging.basicConfig(
    level = logging.DEBUG, 
    format = "%(levelname)-5s |  %(message)-30s -> CAST BY: \033[96m%(name)s\033[0m"
    )
    
log = logging.getLogger(painted_string("main", "#FF7B00"))
program_is_running = True
FPS = 60
FRAME_TIME = 1/FPS

log.debug(painted_string("Program Started              ", COLORS.RED))

log.debug("Main app launched")
if __name__ == "__main__":
    mahou_app = App()
    mahou_app.run()


print()
