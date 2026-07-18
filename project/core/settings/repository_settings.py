# import de back-end
from core.utils.path import AppPaths

# import geral
import json

class RepositorySettings:
    @classmethod    
    def _read_json(cls):
        with open(AppPaths.JSON_SETTINGS, "r", encoding = "utf-8") as js:
            return json.load(js)

    @classmethod    
    def _update_json(cls, data: dict):
        with open(AppPaths.JSON_SETTINGS, "w", encoding = "utf-8") as js:
            json.dump(data, js, ensure_ascii = False, indent = 4)

    @classmethod    
    def read(cls):
        return cls._read_json()
    
    @classmethod    
    def update(cls, data: dict):
        cls._update_json(data)

    @classmethod
    def format_json(cls, value: bool) -> dict:
        return {
            "is_active_name_link" : value
        }