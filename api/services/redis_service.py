import json
import logging
import os
import uuid
from typing import Any, Dict, Optional

import redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ..utils import GameType, RedisKeys

GAMETYPE_TO_PREFIX = {
    GameType.GOFISH: RedisKeys.GOFISH_PREFIX,
}

class GameLimitExceededError(Exception):
    pass

class GameInProgressError(Exception):
    def __init__(self, game_id: str):
        self.game_id = game_id
        super().__init__(f"User already has an active game with ID {game_id}.")

class GameNotFoundError(Exception):
    pass


class RedisService:
    def __init__(self, cxn_str: str) -> None:
        self.client = redis.from_url(cxn_str, decode_responses=True)

    def _ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except redis.ConnectionError:
            return False
    
    def _set(self, key: str, value: str, ex: int = 3600) -> bool:
        return bool(self.client.set(name=key, value=value, ex=ex))

    def _get(self, key: str) -> Optional[str]:
        result = self.client.get(name=key)
        return str(result) if result is not None else None
    
    def _remove(self, key: str) -> None:
        self.client.delete(key)
    
    def _check_game_counts(self, user_email: str, game_type: GameType) -> None:
        total_key = f"{RedisKeys.GAME_COUNT_PREFIX.value}{user_email}"
        game_key = f"{GAMETYPE_TO_PREFIX[game_type].value}{RedisKeys.ONGOING_GAME_ID_PREFIX.value}{user_email}"

        logger.info(f"Checking game counts for user {user_email} and game_type={game_type}. game_key={game_key}, total_key={total_key}")

        # Retrieve current counts
        total_count = self._get(total_key)
        game_id = self._get(game_key)

        total_count = int(total_count) if total_count else 0
        game_exists = game_id is not None
        logger.info(f"User {user_email} has {total_count} total games and game_exists={game_exists} for game_type={game_type} (game_id={game_id})")

        # Enforce limits
        if total_count >= 90:
            logger.warning(f"User {user_email} has exceeded the maximum number of active games.")
            raise GameLimitExceededError("User has exceeded the maximum number of active games.")
        if game_exists:
            logger.warning(f"User {user_email} already has an active game with ID {game_id}")
            raise GameInProgressError(game_id)
        
        # Update the count
        logger.info(f"Incrementing total game count for user {user_email} to {total_count + 1}")
        self._set(total_key, str(total_count + 1))

    def create_game(self, user_email: str, game_type: GameType) -> str:
        self._check_game_counts(user_email, game_type)

        game_id = str(uuid.uuid4())

        # Set ongoing game ID for user
        ongoing_game_key = f"{GAMETYPE_TO_PREFIX[game_type].value}{RedisKeys.ONGOING_GAME_ID_PREFIX.value}{user_email}"
        logger.info(f"Setting ongoing game for user {user_email} with game_id {game_id} at key {ongoing_game_key}")
        self._set(ongoing_game_key, game_id)
        
        # Set initial game state
        state_key = f"{GAMETYPE_TO_PREFIX[game_type].value}{RedisKeys.GAME_STATE_PREFIX.value}{game_id}"
        initial_state = {
            "id": game_id,
            "host": user_email,
            "state": "initializing",
        }
        self.client.hset(state_key, mapping=initial_state)
        return game_id

    def get_game_state(self, game_id: str, game_type: GameType) -> Dict[str, Any]:
        key = f"{GAMETYPE_TO_PREFIX[game_type].value}{RedisKeys.GAME_STATE_PREFIX.value}{game_id}"
        state = self.client.hgetall(key)

        logger.info(f"Retrieved state for key {key}: {state}")

        if state:
            return {"state": state}

        raise GameNotFoundError("No game found with the provided ID.")
    
    def end_game(self, user_email: str, game_type: GameType) -> None:
        game_key = f"{GAMETYPE_TO_PREFIX[game_type].value}{RedisKeys.ONGOING_GAME_ID_PREFIX.value}{user_email}"
        game_id = self._get(game_key)

        if game_id is None:
            logger.warning(f"Attempted to end game for user {user_email} but no active game found.")
            raise GameNotFoundError("No active game found for user.")
        
        state_key = f"{GAMETYPE_TO_PREFIX[game_type].value}{RedisKeys.GAME_STATE_PREFIX.value}{game_id}"

        self._remove(state_key)
        self._remove(game_key)

        logger.info(f"Ended game {game_id} for user {user_email}.")



redis_service = RedisService(cxn_str=os.getenv("REDIS_URL", "redis://localhost:6379"))
