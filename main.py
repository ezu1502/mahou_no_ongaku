import os; os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import time
import logging
from functools import wraps
from ENUMS import PS, COLORS, painted_string

from window import MahouWindow
from player import MahouPlayer

logging.basicConfig(
    level = logging.DEBUG, 
    format = "%(levelname)-5s |  %(message)-30s -> CAST BY: \033[96m%(name)s\033[0m"
    )

log = logging.getLogger(painted_string("main", COLORS.ORANGE))
program_is_running = True
FPS = 60
FRAME_TIME = 1/FPS

mahou_player = MahouPlayer()
mahou_window = MahouWindow(mahou_player, dimensions = "900x600")

def tick(function):
    log.debug("tick decorator created")

    @wraps(function)
    def wrapper():

        initial_time = time.monotonic()

        function()

        final_time = time.monotonic()
        meantime = final_time - initial_time
        sleep = FRAME_TIME - meantime

        if sleep > 0:
            time.sleep(sleep)
        else:
            # log.warning("Frame took long than expected")
            pass

    return wrapper



def update():
    if mahou_window.state == PS.SHUT_DOWN:
        shut_down()
        return
    mahou_window.root.update()

def shut_down():
    global program_is_running
    program_is_running = False

    log.info("Program Terminated")

@tick
def mainloop():
    update()

while program_is_running:
    mainloop() #tá com o tick decorator, então toda vez roda automaticamente forçando 60FPS

print()