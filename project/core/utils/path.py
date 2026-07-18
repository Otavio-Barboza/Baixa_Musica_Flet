# imports gerais
from pathlib import Path
import os


class AppPaths:
    LOCAL_APP_DATA: Path = Path(os.environ["LOCALAPPDATA"])

    BAIXA_MUSICA: Path = LOCAL_APP_DATA / "Baixa Musica"

    JSON_SETTINGS = BAIXA_MUSICA / "settings.json"