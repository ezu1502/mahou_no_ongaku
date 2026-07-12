from pathlib import Path
import json

cache_file = Path("cache/song_analysis.json")



def save_song_cache(cache_file: Path, analysis_dictionary: dict) -> None:
    cache_file.parent.mkdir(parents = True, exist_ok = True)
    cache_file.touch(exist_ok = True)

    with cache_file.open("w", encoding = "utf-8") as cache:
        json.dump(analysis_dictionary, cache, ensure_ascii = False, indent = 4)


def load_song_cache(cache_file: Path) -> None | dict:
    if not cache_file.exists():
        return None
    
    try:
        with cache_file.open("r", encoding = "utf-8") as cache:
            return json.load(cache)
    except json.JSONDecodeError:
        return None
    
