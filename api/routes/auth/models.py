from pydantic import BaseModel


class User(BaseModel):
    """Model for user data"""

    user_id: str
    username: str
    email: str
