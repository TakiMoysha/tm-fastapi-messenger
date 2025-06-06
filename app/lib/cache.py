from cachebox import BaseCacheImpl, Cache
from typing import Protocol, runtime_checkable


__all__ = ("BaseCacheImpl", "CacheBoxCache")


class CacheBoxCache(Cache):
    @classmethod
    def default(cls):
        return cls(maxsize=0)
