import json
import logging

from pydantic import BaseModel
from redis.asyncio import Redis


class RedisRepository:
    def __init__(self, redis: Redis):
        self.cache = redis

    async def clear_cache(self, path: str) -> None:
        keys = await self.cache.keys(f"{path}*")
        if not keys:
            logging.warning("cache keys to clear not found")
            return
        logging.info(f"cache keys to clear found")
        await self.cache.delete(keys)

    async def get_cache(self, path: str):
        try:
            value = await self.cache.get(path)
            if value:
                logging.info(f"cache found {path}, value={value}")
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Error getting cache: {e}")
            return None

    async def set_cache(self, path: str, value: BaseModel) -> None:
        json_value = json.dumps(value.model_dump())
        await self.cache.setex(path, 3600, json_value)
        logging.info(f"value={json_value} is cached")