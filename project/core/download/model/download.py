from pathlib import Path
import yt_dlp
import os

class Download:
    def __init__(self):
        self._FFMPEG_PATH = Path(__file__).resolve().parents[3] / "assets" / "ffmpeg"
        self._path = None

    # Utilidades dos métodos internos da classe
    def set_path(self, path: str):
        self._path = path


    # Função de download
    def download(
        self,
        url: str, 
        cookies: str | None = None
    ) -> bool:
        """
        _summary_: (
            Baixa o áudio de um vídeo do YouTube em formato MP3;
            Usa client Android e valida o download para evitar falso sucesso;
        )

        Returns:
            str: Texto informativo referente à conclusão ou erro no download do MP3.
        """

        from core.download.controller.controller_download import ControllerDownload

        if self._path is None:
            return
        
        os.makedirs(self._path, exist_ok = True)

        options = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(self._path, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "nocheckcertificate": True,
            "geo_bypass": True,
            "quiet": False,
            # Client Android resolve 403 na maioria dos casos
            "extractor_args": {"youtube": {"player_client": ["android"]}},
            "http_headers": {
                "User-Agent": "com.google.android.youtube/19.09.37 (Linux; U; Android 13)",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
            },
            "postprocessors": [{
                "key": "FFmpegExtractAudio", 
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "ffmpeg_location": self._FFMPEG_PATH
        }

        if cookies and os.path.exists(cookies):
            options["cookiefile"] = cookies

        try:            
            with yt_dlp.YoutubeDL(options) as ydl:
                information = ydl.extract_info(url, download = True)
                file_name = ydl.prepare_filename(information)
                mp3_name = os.path.splitext(file_name)[0] + ".mp3"

            if os.path.exists(mp3_name):
                ControllerDownload.notify_callback(
                    event = "path_download_saved",
                    data = f"Salvo em: {mp3_name}"
                )
                return True
            else:
                ControllerDownload.notify_callback(
                    event = "snack_bar_information",
                    data = f"erro no download: {mp3_name}, tente novamente!"
                )
                return False
        except yt_dlp.utils.DownloadError as utils:
            print(f"\nFalha no download: {utils}")
            ControllerDownload.notify_callback(
                event = "snack_bar_information",
                data = f"erro no download: {mp3_name}, tente novamente!"
            )
            return False
        except Exception as e:
            print(f"\nErro inesperado: {e}")
            ControllerDownload.notify_callback(
                event = "snack_bar_information",
                data = f"erro inesperado no download: {mp3_name}, tente novamente!"
            )
            return False
    
    def return_title_video(self, url: str) -> str:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)
        return info["title"]

download = Download()
print(download._FFMPEG_PATH)