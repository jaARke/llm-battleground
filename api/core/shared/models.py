from typing import List

from pydantic import BaseModel, Field

from ...utils.enums import GameStatus


class AIModel(BaseModel):
    internal_name: str = Field(
        ..., description="Internal identifier for the AI model for use with Vercel's AI gateway"
    )
    display_name: str = Field(..., description="User-friendly name of the AI model")


class GameState(BaseModel):
    """Model representing the state of a Go Fish game"""

    user_email: str = Field(..., description="Email of the game host")
    start_time: str = Field(..., description="ISO 8601 timestamp when the game started")
    players: List[AIModel] = Field(..., description="List of AI models participating in the game")
    status: GameStatus = Field(..., description="Current state of the game")
