from pathlib import Path
import yt_dlp
import os

def _get_ffmpeg():
    BASE_DIR = Path(__file__).resolve().parent.parent
    FFMPEG_PATH = BASE_DIR / "ffmpeg"
    return FFMPEG_PATH


def baixar_via_ffmpeg(
    url: str, 
    destination_path: str = r"C:\Users\barbo\Music", 
    cookies: str | None = None
) -> str:
    """
        Baixa o áudio de um vídeo do YouTube em formato MP3.
        Usa client Android e valida o download para evitar falso sucesso.
    """
    
    os.makedirs(destination_path, exist_ok = True)

    options = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(destination_path, "%(title)s.%(ext)s"),
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
        "ffmpeg_location": _get_ffmpeg()
    }

    if cookies and os.path.exists(cookies):
        options["cookiefile"] = cookies

    try:
        print("Iniciando yt-dlp")
        
        with yt_dlp.YoutubeDL(options) as ydl:
            information = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(information)
            mp3_name = os.path.splitext(file_name)[0] + ".mp3"

        if os.path.exists(mp3_name):
            return f'Arquivo salvo em: {os.path.abspath(mp3_name)}'
        else:
            print("\nErro: o áudio não foi salvo. Provável bloqueio (403).")
            return 'Áudio não salvo, tente o download novamente!'
    except yt_dlp.utils.DownloadError as utils:
        print(f"\nFalha no download: {utils}")
        return "Falha no download, tente novamente!"
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        return "Erro não identificado, tente novamente!"