from typing import List

from ..shared.models import AIModel


class GameAlreadyCompletedError(Exception):
    """Exception raised when an action is attempted on a completed game."""

    pass


class InvalidGameStateError(Exception):
    """Exception raised when the game state is invalid or corrupted."""

    pass


class RoundDoesNotExistError(Exception):
    """Exception raised when a specified round does not exist in the game history."""

    pass


class PlayerNotFoundError(Exception):
    """Exception raised when a player is not found in the game state."""

    def __init__(self, message: str, available_players: List[AIModel]) -> None:
        super().__init__(message)
        self.available_players = available_players


class CatchExceedsPondTotalError(Exception):
    """Exception raised when a player tries to catch more fish than are available in the pond."""

    def __init__(self, message: str, available_fish: int) -> None:
        super().__init__(message)
        self.available_fish = available_fish


class CatchExceedsRoundLimitError(Exception):
    """Exception raised when a player tries to catch more fish than the round's catch limit."""

    def __init__(self, message: str, round_limit: int) -> None:
        super().__init__(message)
        self.round_limit = round_limit


class SharingExceedsPossessionError(Exception):
    """Exception raised when a player tries to share more fish than they possess."""

    def __init__(self, message: str, available_fish: int) -> None:
        super().__init__(message)
        self.available_fish = available_fish
