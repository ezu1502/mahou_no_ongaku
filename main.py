import os; os.environ["BOCCA_HIDE_GREETING"] = "1"
os.environ["QT_LOGGING_RULES"] = "qt.multimedia.ffmpeg.*=false"
os.environ.pop("QT_FFMPEG_DEBUG", None)

from mahou_libs.colors import painted_string
from mahou.core.app import App
from mahou_libs import bocca

log = bocca.BoccaFiglia("main", "#FFAE00") 
bocca.configure_default_settings()
bocca.set_core_level(11) # Nível do logger

program_is_running = True

launch_message = painted_string(f"{'Program Started.':<30}", "#FF2222")
end_message = painted_string(f"{'Program Terminated.':<30}", "#FF2222")


log.info(f"{launch_message}")

try:
    if __name__ == "__main__":
        mahou_app = App()
        mahou_app.run()
finally:
    log.info(end_message)

