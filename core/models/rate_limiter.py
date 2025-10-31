import time
from fastapi import Request, HTTPException, status
from functools import wraps

def rate_limiter(limit: int, period: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            redis = request.app.state.redis
            ip = request.client.host
            now = int(time.time())
            
            key = f"rate:{ip}:{request.url.path}:{now // period}"
            count = await redis.incr(key)
            
            if count == 1:
                await redis.expire(key, period)
                
            if count > limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail='Too many request. Please try again later',
                )
                
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator