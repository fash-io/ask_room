# app/ratelimiter.py
import time
from fastapi import Request, HTTPException, status
from starlette.datastructures import State
from aioredis import Redis


class RateLimiter:
    def __init__(self, times: int, seconds: int):
        """
        :param times:    max number of requests
        :param seconds:  per this many seconds
        """
        self.times = times
        self.seconds = seconds

    async def __call__(self, request: Request):
        # Pull Redis client out of app.state
        redis: Redis = request.app.state.redis  
        client_ip = request.client.host
        # You can also scope per-endpoint:
        route = request.url.path
        key = f"rate:{client_ip}:{route}"

        # Current window count
        count = await redis.incr(key)
        if count == 1:
            # First hit in this window—set TTL
            await redis.expire(key, self.seconds)

        if count > self.times:
            # Too many
            ttl = await redis.ttl(key)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": self.times,
                    "per": f"{self.seconds} seconds",
                    "retry_after": ttl,
                },
            )
        # Otherwise: allow
        return True
