from fastapi import Request, HTTPException
import time
from collections import defaultdict
import threading


class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
        self.lock = threading.Lock()

    async def __call__(self, request: Request):
        client_ip = request.client.host
        current_time = time.time()

        with self.lock:
            # Remove requests older than 1 minute
            self.requests[client_ip] = [
                t for t in self.requests[client_ip] if current_time - t < 60
            ]

            # Check if rate limit exceeded
            if len(self.requests[client_ip]) >= self.requests_per_minute:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "limit": self.requests_per_minute,
                        "per": "minute",
                        "retry_after": 60
                        - int(current_time - self.requests[client_ip][0]),
                    },
                )

            # Add current request timestamp
            self.requests[client_ip].append(current_time)

        return True


# Create instances with different limits for different endpoints
standard_limiter = RateLimiter(
    requests_per_minute=60
)  # 60 requests per minute for most endpoints
auth_limiter = RateLimiter(
    requests_per_minute=10
)  # 10 requests per minute for auth endpoints
search_limiter = RateLimiter(
    requests_per_minute=30
)  # 30 requests per minute for search endpoints
