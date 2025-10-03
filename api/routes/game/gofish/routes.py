from fastapi import APIRouter, Depends, HTTPException

from ....services import redis_service, GameLimitExceededError, GameInProgressError, GameNotFoundError
from ...auth.utils import User, get_current_user
from .models import CreateGameResponse, GameStateResponse
from ....utils import GameType

router = APIRouter(prefix="/api/py/game/gofish", tags=["gofish"])


@router.get("/create", response_model=CreateGameResponse)
async def create_game(current_user: User = Depends(get_current_user)) -> CreateGameResponse:
    try:
        game_id = redis_service.create_game(current_user.email, GameType.GOFISH)
        return CreateGameResponse(game_id=game_id)
    except GameInProgressError as e:
        return CreateGameResponse(game_id=e.game_id)
    except GameLimitExceededError as e:
        raise HTTPException(status_code=429, detail=str(e))


@router.get("/state", response_model=GameStateResponse)
async def get_game_state(game_id: str, current_user: User = Depends(get_current_user)) -> GameStateResponse:
    try:
        as_dict = redis_service.get_game_state(game_id, GameType.GOFISH)
        return GameStateResponse(**as_dict)
    except GameNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/end")
async def end_game(current_user: User = Depends(get_current_user)) -> None:
    try:
        redis_service.end_game(current_user.email, GameType.GOFISH)
    except GameNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
