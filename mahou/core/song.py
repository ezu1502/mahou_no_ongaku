from dataclasses import dataclass, field
from pathlib import Path
from bunseki import Analyzer
from functools import wraps
from mahou_libs import mahou_math
from send2trash import send2trash
from mahou_libs.colors import painted_string
from mahou_libs.bocca import BoccaFiglia

log = BoccaFiglia("Song_Class", "#00FF00")

@dataclass
class Song:
    path: Path
    
    @property
    def title(self):
        name = self.path.stem
        name = name.replace("\ufeff", "")
        return name

        

        








#endregion