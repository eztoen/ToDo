from redis.asyncio import Redis
from core.config import settings

class RedisHelper:
    def __init__(self):
        self.redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        
    async def get_client(self) -> Redis:
        return self.redis
    
    async def close(self):
        await self.redis.close
        
redis_helper = RedisHelper()