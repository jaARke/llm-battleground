from datetime import datetime
from fastapi import APIRouter, Depends
from ..auth import get_current_user, User
from ..models import ProtectedResponse, UserResponse

router = APIRouter(prefix="/api/py", tags=["users"])


@router.get("/protected", response_model=ProtectedResponse)
async def protected_route(current_user: User = Depends(get_current_user)):
    return ProtectedResponse(
        message="This is a protected route!",
        user=UserResponse(**current_user.dict()),
        timestamp=datetime.utcnow(),
    )
