import os
from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable

from ...utils import RedisService
from ...utils.exceptions import GameInProgressError, GameNotFoundError
from .models import GameState


def reset_game_expiration(func: Callable) -> Callable:
    """
    Decorator that resets the expiration time for the game state object
    when get_game_state or set_game_state methods are called.
    """

    @wraps(func)
    def wrapper(self: "GameRedisService", user_email: str, *args, **kwargs):
        # Call the original function first
        result = func(self, user_email, *args, **kwargs)

        # Reset the expiration time for the game state key
        state_key = self.GAME_STATE_KEY.format(user_email=user_email)

        # Only reset expiration if the key exists
        if self._exists(state_key):
            self._set_exp(state_key, self.GAME_EXPIRATION_SECONDS)

        return result

    return wrapper


class GameRedisService(RedisService, ABC):
    GAME_STATE_KEY = "game_state:game_name_here:{user_email}"
    """Key pattern for storing game-specific state per user. Subclasses must override."""

    GAME_EXPIRATION_SECONDS = int(os.getenv("GAME_EXPIRATION_SECONDS", 86400))
    """Per-game expiration time in seconds (default: 24 hours). Subclasses may override."""

    @abstractmethod
    def _get_initial_game_state(self, user_email: str, *args, **kwargs) -> GameState:
        """
        Subclasses must implement this method to return the specific initial game state model.
        """

    def _get_raw_game_state(self, user_email: str) -> str:
        state = self._get(self.GAME_STATE_KEY.format(user_email=user_email))

        if state:
            self.logger.debug("Retrieved raw game state for user_email %s", user_email)
            return state

        self.logger.error("Failed to get game state. No game found for user_email %s", user_email)
        raise GameNotFoundError("No game found for the provided user_email.")

    def check_has_active_game(self, user_email: str) -> bool:
        return self._exists(self.GAME_STATE_KEY.format(user_email=user_email))

    def create_game(self, user_email: str, *args, **kwargs) -> GameState:
        if self.check_has_active_game(user_email):
            self.logger.warning("User %s already has an active game of this type", user_email)
            raise GameInProgressError(
                f"User {user_email} already has an active game of this type.",
            )

        self.increment_game_count(user_email)

        state_key = self.GAME_STATE_KEY.format(user_email=user_email)
        initial_state = self._get_initial_game_state(user_email, *args, **kwargs)
        initial_state_dumped = initial_state.model_dump_json()

        self._set(state_key, initial_state_dumped, ex=self.GAME_EXPIRATION_SECONDS)
        self.logger.info(
            "Initialized game state for user_email %s with expiration %d seconds",
            user_email,
            self.GAME_EXPIRATION_SECONDS,
        )

        return initial_state

    @abstractmethod
    def get_game_state(self, user_email: str) -> GameState:
        """
        Subclasses must implement this method to return the specific game state model.
        The @reset_game_expiration decorator should be applied in the subclass.
        """

    @reset_game_expiration
    def set_game_state(self, user_email: str, state: GameState) -> None:
        if not self.check_has_active_game(user_email):
            self.logger.error(
                "Attempted to set game state for user %s but no active game found", user_email
            )
            raise GameNotFoundError("No active game found for user.")

        state_key = self.GAME_STATE_KEY.format(user_email=user_email)
        self._set(state_key, state.model_dump_json())
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
