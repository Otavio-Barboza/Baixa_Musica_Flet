from urllib.parse import urlparse

class CacheDownload:

    _cache_downloads: set[str] = set()


    # Métodos internos
    @classmethod
    def _validate_url(cls, url: str | None) -> bool:
        """
        _summary_: Função simples para verificação se é uma url verdadeira ou não, assim retornando True se for uma url e False para caso não seja;

        Args:
            url (str | None): A url padrão é um string, mas em casos que acontecer algum erro e receber um None, será validada nesta função.

        Returns:
            bool: True ou False
        """

        if url is None:
            return False
        
        if not isinstance(url, str):
            return False
        
        if not url.strip():
            return False
        
        result = urlparse(url)

        return (
            result.scheme in ("http", "https")
            and bool(result.netloc)
        )
    
    @classmethod
    def _remove_url(cls, url: str):
        if cls._validate_url(url):
            cls._cache_downloads.remove(url)
    

    # Métodos externos
    @classmethod
    def add_download(cls, urls: list[str]) -> list[str]:
        """
        _summary_: Função para realizar a adição das novas urls ao _cache_downloads, validando cada uma antes de adicionar. Essa função retorna a list[str] para ser usada na função _add_download_container no main.py, isso para evitar duplicatas ou inconsistência de dados adicionados _cache_downloads;

        Args:
            urls (list[str]): Lista com as urls.

        Returns:
            list[str]: Retorna uma lista com as urls.
        """

        added_urls: list[str] = []

        for url in urls:
            if (
                cls._validate_url(url)
                and url not in cls._cache_downloads
            ):
                cls._cache_downloads.add(url)
                added_urls.append(url)
        
        print(cls._cache_downloads)
        return added_urls
    
    @classmethod
    def remove_download(cls, url_to_remove: str):
        cls._remove_url(url_to_remove)
        print(cls._cache_downloads)
    
    @classmethod
    def clear_cache_downloads(cls):
        cls._cache_downloads.clear()

    @classmethod
    def return_cache_downloads(cls) -> list[str]:
        return list(cls._cache_downloads)