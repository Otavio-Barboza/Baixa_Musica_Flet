from pathlib import Path
import yt_dlp
import os

def obter_ffmpeg():
    BASE_DIR = Path(__file__).resolve().parent.parent
    FFMPEG_PATH = BASE_DIR / "ffmpeg"

    print(FFMPEG_PATH)
    print(os.path.exists(FFMPEG_PATH))
    
    return FFMPEG_PATH


def baixar_via_ffmpeg(
    url: str, 
    pasta_destino: str = r"C:\Users\barbo\Music", 
    cookies: str | None = None
) -> str:
    """
        Baixa o áudio de um vídeo do YouTube em formato MP3.
        Usa client Android e valida o download para evitar falso sucesso.
    """

    
    os.makedirs(pasta_destino, exist_ok = True)

    opcoes = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(pasta_destino, "%(title)s.%(ext)s"),
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
        "ffmpeg_location": obter_ffmpeg()
    }

    if cookies and os.path.exists(cookies):
        opcoes["cookiefile"] = cookies

    try:
        print("Iniciando yt-dlp")
        
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url, download=True)
            nome_arquivo = ydl.prepare_filename(info)
            nome_mp3 = os.path.splitext(nome_arquivo)[0] + ".mp3"

        if os.path.exists(nome_mp3):
            print(f"\n✅ Download concluído com sucesso!")
            print(f"📂 Arquivo salvo em: {os.path.abspath(nome_mp3)}")
            return f'✅ Download concluído com sucesso!\n📂 Arquivo salvo em: {os.path.abspath(nome_mp3)}'
        else:
            print("\n❌ Erro: o áudio não foi salvo. Provável bloqueio (403).")
            print("💡 Tente atualizar o yt-dlp ou usar cookies do navegador.")
            return '❌ Erro: o áudio não foi salvo. Provável bloqueio (403).\n💡 Tente atualizar o yt-dlp ou usar cookies do navegador.'
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Falha no download: {e}")
        print("💡 Tente atualizar o yt-dlp: pip install -U yt-dlp")
        return "💡 Tente atualizar o yt-dlp: pip install -U yt-dlp"
    except Exception as e:
        print(f"\n⚠️ Erro inesperado: {e}")
        return f"\n⚠️ Erro inesperado: {e}"