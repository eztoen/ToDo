import hashlib
import time
from fastapi import Request, HTTPException, status
from functools import wraps


async def reset_rate_limit(request: Request, identifier: str = None):
    redis = request.app.state.redis
    
    if not identifier:
        identifier = api_key_identifier(request)
    
    key_data = f"{identifier}:{request.method}:{request.url.path}"
    key_hash = hashlib.md5(key_data.encode()).hexdigest()
    key = f"rate_limit:{key_hash}"
    
    await redis.delete(key)

def api_key_identifier(request: Request) -> str:
    api_key = (
        request.headers.get("X-API-Key") or
        request.headers.get("Authorization") or
        request.headers.get("X-API-Token")
    )
    
    if api_key and api_key.startswith("Bearer "):
        api_key = api_key[7:]
    
    if api_key:
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:16]
        return f"apikey:{key_hash}"

    return f"ip:{request.client.host}"

def rate_limiter(limit: int, period: int, identifier_fn=api_key_identifier):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            try:
                redis = request.app.state.redis
                
                if identifier_fn:
                    identifier = identifier_fn(request)
                else:
                    identifier = request.client.host
                
                key_data = f"{identifier}:{request.method}:{request.url.path}"
                key_hash = hashlib.md5(key_data.encode()).hexdigest()
                key = f"rate_limit:{key_hash}"
                
                async with redis.pipeline(transaction=True) as pipe:
                    try:
                        current_time = time.time()
                        pipe.zadd(key, {str(current_time): current_time})
                        
                        pipe.zremrangebyscore(key, 0, current_time - period)
                        
                        pipe.zcard(key)
                        
                        pipe.expire(key, period + 10)
                        
                        results = await pipe.execute()
                        request_count = results[2]
                        
                    except Exception as e:
                        return await func(request, *args, **kwargs)
                
                if request_count > limit:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail={
                            'error': 'Too many requests',
                            'limit': limit,
                            'period': period,
                            'retry_after': period
                        },
                        headers={'Retry-After': str(period)}
                    )
                
                return await func(request, *args, **kwargs)
                
            except HTTPException as e:
                if (e.status_code == 400 and 
                    "email already taken" in str(e.detail).lower()):
                    await reset_rate_limit(request, identifier)
                raise e
            
            except Exception as e:
                return await func(request, *args, **kwargs)
                
        return wrapper
    return decorator