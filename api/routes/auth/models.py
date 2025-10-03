from pydantic import BaseModel


class UserResponse(BaseModel):
    """Response model for user data"""

    user_id: str
    username: str
    email: str

    class Config:
        from_attributes = True