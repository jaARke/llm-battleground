from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    """Response model for user data"""

    user_id: str
    username: str
    email: Optional[str] = None

    class Config:
        from_attributes = True


class ProtectedResponse(BaseModel):
    """Response model for protected routes"""

    message: str
    user: UserResponse
    timestamp: datetime
