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
    def _atualizar_downloads(cls, url: str):
        if url not in cls._cache_downloads:
            cls._cache_downloads.append(url)

    @classmethod
    def add_download(cls, url: str):
        if cls._validate_url(url = url):
            cls._atualizar_downloads(url = url)

        print(cls._cache_downloads)