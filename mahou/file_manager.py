from pathlib import Path
import json
from mahou.core.enums import Paths

# json.loads() transforma uma string num objeto python
# json.dumps() transforma um objeto python em string

def read_file(file: Paths) -> dict:
    path = file.value #value é o valor do enum mesmo, o path em si nesse caso
    if not path.exists():
        return {}
    str_info = path.read_text() #retorna uma string crua do json
    info = json.loads(str_info) #o json pega a string crua e transforma em dict manipulável

    return info


def save_setting(setting, name: str):
    path = Paths.SETTINGS_FILE.value #puxa o caminho da user_settings.json
    path.parent.mkdir(parents = True, exist_ok = True) #cria a pasta mãe se n existir

    settings_dict = read_file(Paths.SETTINGS_FILE) #consegue o dict contido no arquivo
    settings_dict[name] = setting #altera a configuração que o usuário quiser

    new_settings_str = json.dumps(settings_dict, indent = 4) #faz uma string atualizada pronta pra ir pro arquivo
    path.write_text(new_settings_str) #atualiza o arquivo 


def get_setting(setting_name : str, subsetting_name: str | None = None):
    path = Paths.SETTINGS_FILE

    options_dict = read_file(path)
    setting = options_dict.get(setting_name, None)

    if subsetting_name is None:
        return setting
    
    if setting is None:
        return

    
    subsetting = setting.get(subsetting_name, None)
    return subsetting