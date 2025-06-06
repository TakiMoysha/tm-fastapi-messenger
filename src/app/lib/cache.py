from cachebox import Cache
from typing import Protocol, runtime_checkable


@runtime_checkable
class ICache(Protocol):
    def get(self, key): ...
    def set(self, key, value): ...
    def delete(self, key): ...

class OnlyDevInMemoryCache(ICache):
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def delete(self, key):
        if key not in self.cache:
            return

        del self.cache[key]


class CacheBoxCache(Cache): ...
