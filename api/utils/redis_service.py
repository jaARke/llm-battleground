import logging
import os
from typing import Any, Dict, Optional

import redis

from .exceptions import GameLimitExceededError

logger = logging.getLogger(__name__)

client = redis.from_url(
    os.getenv("UPSTASH_REDIS_URL", "redis://localhost:6379"), decode_responses=True
)


class RedisService:
    GAME_COUNT_KEY = "game_count:{user_email}"
    """Key pattern for tracking the number of games started by a user in a time window"""

    MAX_GAME_COUNT = int(os.getenv("MAX_GAME_COUNT", 5))
    """Maximum number of games allowed per user in the defined time window (default: 5). Set to -1 for no limit."""

    GAME_COUNT_WINDOW_SECONDS = int(os.getenv("GAME_COUNT_WINDOW_SECONDS", 86400))
    """Time window in seconds for counting games (default: 24 hours)"""

    def __init__(self, logger_instance: Optional[logging.Logger] = None) -> None:
        self.client = client
        self.logger = logger_instance or logger

    def _ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except redis.ConnectionError:
            return False

    def _set(self, key: str, value: str, ex: int = 3600) -> bool:
        self.logger.debug("Setting key %s with expiration %d seconds", key, ex)
        return bool(self.client.set(name=key, value=value, ex=ex))

    def _get(self, key: str) -> Optional[str]:
        result = self.client.get(name=key)
        self.logger.debug("Getting key %s returned %s", key, result)
        return str(result) if result is not None else None

    def _remove(self, key: str) -> None:
        self.logger.debug("Removing key %s", key)
        self.client.delete(key)

    def _exists(self, key: str) -> bool:
        self.logger.debug("Checking existence of key %s", key)
        return self.client.exists(key)

    def _set_exp(self, key: str, ex: int) -> None:
        self.logger.debug("Setting expiration for key %s to %d seconds", key, ex)
        self.client.expire(name=key, time=ex)

    def _clear(self) -> None:
        for key in self.client.keys("*"):
            self.logger.debug("Removing key %s", key)
            self.client.delete(key)

    def get_game_count(self, user_email: str) -> int:
        key = self.GAME_COUNT_KEY.format(user_email=user_email)

        count = self._get(key)
        return int(count) if count else 0

    def increment_game_count(self, user_email: str) -> int:
        key = self.GAME_COUNT_KEY.format(user_email=user_email)

        current_count = self.get_game_count(user_email)
        new_count = current_count + 1
        ttl = self.client.ttl(key)
        ttl = int(ttl) if isinstance(ttl, int) else self.GAME_COUNT_WINDOW_SECONDS
        expiration = ttl if ttl > 0 else self.GAME_COUNT_WINDOW_SECONDS

        if self.MAX_GAME_COUNT >= 0 and new_count > self.MAX_GAME_COUNT:
            self.logger.warning("User %s has exceeded the maximum game limit", user_email)
            raise GameLimitExceededError(
                f"User {user_email} has exceeded the maximum of {self.MAX_GAME_COUNT} games in the"
                f" last {self.GAME_COUNT_WINDOW_SECONDS} seconds. The limit will reset in {ttl}"
                " seconds."
            )

        self.logger.info(
            "Incrementing game count for user %s to %d. Limit will reset in %d seconds",
            user_email,
            new_count,
            expiration,
        )
        self._set(key, str(new_count), ex=expiration)
        return new_count

    def check_game_count(self, user_email: str) -> bool:
        count = self.get_game_count(user_email)
        return count < self.MAX_GAME_COUNT

    def clear_game_count(self, user_email: str) -> None:
        self.logger.info("Clearing game count for user %s", user_email)
        key = self.GAME_COUNT_KEY.format(user_email=user_email)
        self._remove(key)
