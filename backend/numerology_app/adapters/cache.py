from typing import Optional

class BaseCache:
    async def get(self, key: str) -> Optional[dict]: ...
    async def set(self, key: str, value: dict, ttl: int = 0) -> None: ...

class InMemoryCache(BaseCache):
    def __init__(self):
        self._store = {}

    async def get(self, key: str):
        return self._store.get(key)

    async def set(self, key: str, value: dict, ttl: int = 0):
        self._store[key] = value
