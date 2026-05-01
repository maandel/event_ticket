import redis.asyncio as aioredis

from app.core.config import settings


class RedisCache:
    def __init__(self) -> None:
        self._client: aioredis.Redis | None = None

    async def connect(self) -> None:
        self._client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )

    async def disconnect(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    def _check(self) -> aioredis.Redis:
        if self._client is None:
            raise RuntimeError("Redis client is not connected")
        return self._client

    async def get(self, key: str) -> str | None:
        return await self._check().get(key)

    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        await self._check().setex(key, ttl, value)

    async def delete(self, key: str) -> None:
        await self._check().delete(key)

    async def exists(self, key: str) -> bool:
        return bool(await self._check().exists(key))

    async def incr(self, key: str) -> int:
        return await self._check().incr(key)

    async def expire(self, key: str, seconds: int) -> None:
        await self._check().expire(key, seconds)


cache = RedisCache()
