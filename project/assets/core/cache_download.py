from urllib.parse import urlparse

class CacheDownload:

    _cache_downloads: list[str] = []

    @classmethod
    def _validate_url(cls, url: str | None) -> bool:
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
    def _atualizar_downloads(cls, url_list: list):
        for url in url_list:
            if (
                url not in cls._cache_downloads 
                 and 
                cls._validate_url(url)
            ):
                cls._cache_downloads.append(url)

    @classmethod
    def add_download(cls, url_list: list):
        # if cls._validate_url(url_list = url_list):
        cls._atualizar_downloads(url_list = url_list)
        print(cls._cache_downloads)