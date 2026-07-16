from time import perf_counter as o

import os; os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"; os.environ["BOCCA_HIDE_GREETING"] = "1"

from mahou_libs.colors import painted_string
p = o()
from mahou.core.app import App
s = o()
from mahou_libs import bocca

log = bocca.BoccaFiglia("main", "#FFAE00")

bocca.configure_default_settings()
bocca.set_core_level(11) # Nível do logger


print(s-p, "tempo")
program_is_running = True
FPS = 60
FRAME_TIME = 1/FPS

launch_message = painted_string(f"{'Program Started.':<30}", "#FF2222")
end_message = painted_string(f"{'Program Terminated.':<30}", "#FF2222")


log.info(f"{launch_message}")
log.trace("Main app launched")

try:
    if __name__ == "__main__":
        mahou_app = App()
        mahou_app.run()
finally:
    log.info(end_message)

