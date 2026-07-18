from core.download.cache.cache_download import CacheDownload
from core.download.queue.queue_download import download_queue

class ControllerDownload:

    # Manipulação: registro e notificação de callbacks.
    _callbacks = {
        "snack_bar_information" : [],
        "add_download" : [],
        "downloaded_text" : [],
        "title_download" : [],
        "update_container_download" : [],
        "update_progress_bar" : [],
        "clear_containers" : [],
        "path_download_saved" : [],
        "state_button" : []
    }

    @classmethod
    def register_callback(cls, event: str, callback: callable):
        cls._callbacks[event].append(callback)

    @classmethod
    def notify_callback(cls, data, event: str):
        for callback in cls._callbacks[event]:
            callback(data)


    # Funções do app com gerenciamento centralizado em ControllerDownload.
    @classmethod
    def add_url_to_download(cls, urls: list[str]) -> list[str]:
        urls_to_download =  CacheDownload.add_download(urls)
        download_queue.add(urls_to_download)

        cls.notify_callback(
            event = "add_download", data = urls_to_download
        )
        cls.notify_callback(
            event = "downloaded_text", data = download_queue.return_queue_information()
        )

    @classmethod
    def remove_url_to_download(cls, url: str):
        CacheDownload.remove_download(url)
        download_queue.remove(url)

        cls.notify_callback(
            event = "downloaded_text", data = download_queue.return_queue_information()
        )

    
    # Comandos de Download
    @classmethod
    def start_downloads_queue(cls):
        cls.notify_callback(
            event = "title_download",
            data = "Baixando seus MP3..."
        )        
        
        download_queue.set_is_running(True)
        download_queue.start()

    @classmethod
    def clear_downloads(cls):
        download_queue.clear_queue()
        CacheDownload.clear_cache_downloads()
        cls.notify_callback(
            event = "clear_containers",
            data = None
        )

    @classmethod
    def return_title_video(cls, url: str) -> str:
        from core.download.model.download import download
        return download.return_title_video(url)