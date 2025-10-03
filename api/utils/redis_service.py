import logging
import os
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Dict, Optional

import redis
from pydantic import BaseModel

from .exceptions import GameInProgressError, GameLimitExceededError, GameNotFoundError

logger = logging.getLogger(__name__)

client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True)


def reset_game_expiration(func: Callable) -> Callable:
    """
    Decorator that resets the expiration time for the game state object
    when get_game_state or set_game_state methods are called.
    """

    @wraps(func)
    def wrapper(self, user_email: str, *args, **kwargs):
        # Call the original function first
        result = func(self, user_email, *args, **kwargs)

        # Reset the expiration time for the game state key
        state_key = self.GAME_STATE_KEY.format(user_email=user_email)

        # Only reset expiration if the key exists
        if self.client.exists(state_key):
            self.client.expire(state_key, self.GAME_EXPIRATION_SECONDS)
            self.logger.debug(
                "Reset game expiration for user_email %s to %d seconds",
                user_email,
                self.GAME_EXPIRATION_SECONDS,
            )

        return result

    return wrapper


class RedisService(ABC):
    GAME_COUNT_KEY = "game_count:{user_email}"

    RATE_WINDOW_SECONDS = int(os.getenv("RATE_WINDOW_SECONDS", 86400))
    MAX_GAMES_PER_WINDOW = int(os.getenv("MAX_GAMES_PER_WINDOW", 5))

    def __init__(self, logger_instance: Optional[logging.Logger] = None) -> None:
        self.client = client
        self.logger = logger_instance or logger

    # Basic Redis operations
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

    def get_game_count(self, user_email: str) -> int:
        key = self.GAME_COUNT_KEY.format(user_email=user_email)

        count = self._get(key)
        return int(count) if count else 0

    def increment_game_count(self, user_email: str) -> int:
        key = self.GAME_COUNT_KEY.format(user_email=user_email)

        current_count = self.get_game_count(user_email)
        new_count = current_count + 1
        ttl = self.client.ttl(key)
        ttl = int(ttl) if isinstance(ttl, int) else self.RATE_WINDOW_SECONDS
        expiration = ttl if ttl > 0 else self.RATE_WINDOW_SECONDS

        if new_count > self.MAX_GAMES_PER_WINDOW:
            self.logger.warning("User %s has exceeded the maximum game limit", user_email)
            raise GameLimitExceededError(
                f"User {user_email} has exceeded the maximum of {self.MAX_GAMES_PER_WINDOW} games"
                f" in the last {self.RATE_WINDOW_SECONDS} seconds. The limit will reset in {ttl}"
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
        return count < self.MAX_GAMES_PER_WINDOW

    def clear_game_count(self, user_email: str) -> None:
        self.logger.info("Clearing game count for user %s", user_email)
        key = self.GAME_COUNT_KEY.format(user_email=user_email)
        self._remove(key)


class GameRedisService(RedisService, ABC):
    GAME_STATE_KEY = "game:null:state:{user_email}"
    GAME_EXPIRATION_SECONDS = int(os.getenv("GAME_EXPIRATION_SECONDS", 86400))

    @abstractmethod
    def _get_initial_game_state(self, user_email: str) -> BaseModel:
        """
        Subclasses must implement this method to return the specific initial game state model.
        """

    def _get_raw_game_state(self, user_email: str) -> Dict[str, Any]:
        state = self.client.hgetall(self.GAME_STATE_KEY.format(user_email=user_email))

        if state:
            self.logger.debug("Retrieved raw game state for user_email %s", user_email)
            return state  # type: ignore

        self.logger.error("Failed to get game state. No game found for user_email %s", user_email)
        raise GameNotFoundError("No game found for the provided user_email.")

    def check_has_active_game(self, user_email: str) -> bool:
        current_state = self.client.hgetall(self.GAME_STATE_KEY.format(user_email=user_email))
        return bool(current_state)

    def create_game(self, user_email: str) -> None:
        if self.check_has_active_game(user_email):
            self.logger.warning("User %s already has an active game of this type", user_email)
            raise GameInProgressError(
                f"User {user_email} already has an active game of this type.",
            )

        self.increment_game_count(user_email)

        state_key = self.GAME_STATE_KEY.format(user_email=user_email)
        initial_state = self._get_initial_game_state(user_email).model_dump()

        self.client.hset(state_key, mapping=initial_state)
        self.client.expire(state_key, self.GAME_EXPIRATION_SECONDS)
        self.logger.info(
            "Initialized game state for user_email %s with expiration %d seconds",
            user_email,
            self.GAME_EXPIRATION_SECONDS,
        )

    @abstractmethod
    def get_game_state(self, user_email: str) -> BaseModel:
        """
        Subclasses must implement this method to return the specific game state model.
        It should be decorated with @reset_game_expiration to ensure the expiration is reset
        each time the game state is accessed.
        """

    @reset_game_expiration
    def set_game_state(self, user_email: str, state: BaseModel) -> None:
        if not self.check_has_active_game(user_email):
            self.logger.error(
                "Attempted to set game state for user %s but no active game found", user_email
            )
            raise GameNotFoundError("No active game found for user.")

        state_key = self.GAME_STATE_KEY.format(user_email=user_email)
        self.client.hset(state_key, mapping=state.model_dump())
        self.logger.info("Updated game state for user_email %s", user_email)

    def end_game(self, user_email: str) -> None:
        if not self.check_has_active_game(user_email):
            self.logger.warning(
                "Attempted to end game for user %s but no active game found", user_email
            )
            raise GameNotFoundError("No active game found for user.")

        state_key = self.GAME_STATE_KEY.format(user_email=user_email)

        self._remove(state_key)

        self.logger.info("Ended game for user_email %s", user_email)
