from fastapi import APIRouter, Depends, HTTPException

from ....core.gofish import gofish_redis_service
from ....core.gofish.models import GoFishGameState
from ....utils import (
    GameInProgressError,
    GameLimitExceededError,
    GameNotFoundError,
)
from ...auth.utils import User, get_current_user

router = APIRouter(prefix="/api/py/game/gofish", tags=["gofish"])


@router.get("/create", status_code=204)
async def create_game(
    current_user: User = Depends(get_current_user),
) -> None:
    try:
        gofish_redis_service.create_game(current_user.email)
    except GameInProgressError as e:
        raise HTTPException(status_code=409, detail="Game already in progress")
    except GameLimitExceededError as e:
        raise HTTPException(status_code=429, detail=str(e))


@router.get("/state", response_model=GoFishGameState)
async def get_game_state(current_user: User = Depends(get_current_user)) -> GoFishGameState:
    try:
        return gofish_redis_service.get_game_state(current_user.email)
    except GameNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/end", status_code=204)
async def end_game(current_user: User = Depends(get_current_user)) -> None:
    try:
        gofish_redis_service.end_game(current_user.email)
    except GameNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
