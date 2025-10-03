import datetime
import logging
import os

from ...utils import GameRedisService
from ...utils.redis_service import reset_game_expiration
from .models import GameState, GoFishGameState

logger = logging.getLogger(__name__)


class GoFishRedisService(GameRedisService):
    GAME_STATE_KEY = "game:gofish:state:{user_email}"
    GAME_EXPIRATION_SECONDS = int(os.getenv("GOFISH_GAME_EXPIRATION_SECONDS", 86400))

    def __init__(self) -> None:
        super().__init__(logger_instance=logger)

    def _get_initial_game_state(self, user_email: str) -> GoFishGameState:
        logger.debug("Generating initial game state for user_email %s", user_email)
        return GoFishGameState(
            user_email=user_email,
            start_time=datetime.datetime.utcnow().isoformat() + "Z",
            state=GameState.INITIALIZING,
        )

    @reset_game_expiration
    def get_game_state(self, user_email: str) -> GoFishGameState:
        raw_state = self._get_raw_game_state(user_email)
        logger.info("Retrieved game state for user_email %s", user_email)
        return GoFishGameState(**raw_state)


redis_service = GoFishRedisService()
