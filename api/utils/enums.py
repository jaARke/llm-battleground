from enum import Enum


class GameType(str, Enum):
    GOFISH = "gofish"


class GameStatus(str, Enum):
    INITIALIZING = "initializing"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
