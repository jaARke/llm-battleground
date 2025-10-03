from pydantic import BaseModel, Field

from ...utils import GameState


class GoFishGameState(BaseModel):
    """Model representing the state of a Go Fish game"""

    user_email: str = Field(..., description="Email of the game host")
    start_time: str = Field(..., description="ISO 8601 timestamp when the game started")
    state: GameState = Field(..., description="Current state of the game")
