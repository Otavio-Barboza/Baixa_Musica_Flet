# import de back-end
from core.settings.repository_settings import RepositorySettings

# imports gerais
from pathlib import Path


class SettingsManager:
    
    # validador do switch de ligar ou desligar o aparecer nome do link inserido
    _is_active_name_link: bool = True
    

    @classmethod
    def set_is_active_name_link(cls, value: bool):
        cls._is_active_name_link = value

    @classmethod
    def return_is_active_name_link(cls) -> bool:
        return cls._is_active_name_link
    
    @classmethod
    def update_is_active(cls):
        json_settings = cls.read_json()
        cls.set_is_active_name_link(
            value = json_settings.get("is_active_name_link")
        )

    @classmethod
    def read_json(cls) -> dict:
        return RepositorySettings.read()
    
    @classmethod
    def save_json(cls, data_create: None | bool = None):
        # if data_create is None:
        data: dict = RepositorySettings.format_json(cls._is_active_name_link)
        RepositorySettings.update(data)
        # else:
        #     RepositorySettings.update()