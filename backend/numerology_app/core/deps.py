from .config import settings, Settings
from ..adapters.cache import InMemoryCache

_cache = InMemoryCache()

def get_settings() -> Settings:
    return settings

def get_cache():
    return _cache
