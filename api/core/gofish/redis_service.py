import datetime
import logging
from typing import List

from ...utils.enums import GameStatus
from ..shared import GameRedisService, reset_game_expiration
from ..shared.models import AIModel
from .models import GoFishGameParams, GoFishGameState

logger = logging.getLogger(__name__)


class GoFishRedisService(GameRedisService):
    GAME_STATE_KEY = "game_state:go_fish:{user_email}"
    """Key pattern for storing Go Fish game state per user"""

    def __init__(self) -> None:
        super().__init__(logger_instance=logger)

    def _get_initial_game_state(
        self, user_email: str, players: List[AIModel], params: GoFishGameParams
    ) -> GoFishGameState:
        logger.debug("Generating initial game state for user_email %s", user_email)
        return GoFishGameState(
            user_email=user_email,
            start_time=datetime.datetime.utcnow().isoformat() + "Z",
            players=players,
            status=GameStatus.IN_PROGRESS,
            params=params,
        )

    @reset_game_expiration
    def get_game_state(self, user_email: str) -> GoFishGameState:
        raw_state = self._get_raw_game_state(user_email)
        logger.info("Retrieved parsed game state for user_email %s", user_email)
        return GoFishGameState.model_validate_json(raw_state)


redis_service = GoFishRedisService()
