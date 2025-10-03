from pydantic import BaseModel


class CreateGameResponse(BaseModel):
    """Response model for game creation"""

    game_id: str


class GameStateResponse(BaseModel):
    """Response model for game state"""
    
    state: dict