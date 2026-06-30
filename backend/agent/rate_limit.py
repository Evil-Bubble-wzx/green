"""
Simple in-memory rate limiter for the chat endpoint.
Not persistent — resets on server restart.
"""

import time
from collections import defaultdict
from threading import Lock

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._clients: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()

    def is_allowed(self, client_id: str) -> bool:
        """Check if client is under the rate limit. Thread-safe."""
        now = time.time()
        with self._lock:
            # Remove expired entries
            self._clients[client_id] = [
                t for t in self._clients[client_id] if now - t < self.window
            ]
            if len(self._clients[client_id]) >= self.max_requests:
                return False
            self._clients[client_id].append(now)
            return True

    def remaining(self, client_id: str) -> int:
        now = time.time()
        with self._lock:
            self._clients[client_id] = [
                t for t in self._clients[client_id] if now - t < self.window
            ]
            return max(0, self.max_requests - len(self._clients[client_id]))


# Global instance: 10 requests per 60 seconds per IP
chat_limiter = RateLimiter(max_requests=10, window_seconds=60)
