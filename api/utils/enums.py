from enum import Enum

class GameType(str, Enum):
    GOFISH = "gofish"


class RedisKeys(str, Enum):
    GOFISH_PREFIX = "gofish:"

    GAME_COUNT_PREFIX = "game_count:"
    GAME_STATE_PREFIX = "game_state:"

    ONGOING_GAME_ID_PREFIX = "ongoing_game:"