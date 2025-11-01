from redis.asyncio import Redis
from .redis_helper import redis_helper

async def clear_task_cache(date):
    redis: Redis = await redis_helper.get_client()
    cache_key = f'tasks:{date.isoformat()}'
    await redis.delete(cache_key)