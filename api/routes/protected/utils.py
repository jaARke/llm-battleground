import os
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

# JWT Configuration
JWT_SECRET = os.getenv("NEXTAUTH_SECRET", "your-secret-key-here")
JWT_ALGORITHM = "HS256"

# Security scheme
security = HTTPBearer()


class User:
    def __init__(self, user_id: str, username: str, email: Optional[str] = None):
        self.user_id = user_id
        self.username = username
        self.email = email

    def dict(self):
        return {"user_id": self.user_id, "username": self.username, "email": self.email}


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    try:
        token = credentials.credentials

        print("Verifying token:", token)  # Debugging line
        print("Using JWT_SECRET:", JWT_SECRET)  # Debugging line

        # Decode the JWT token using the same secret as NextAuth
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # Extract user information
        username = payload.get("name")
        user_id = payload.get("sub")  # NextAuth uses 'sub' for user ID
        email = payload.get("email")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return User(user_id=user_id, username=username, email=email)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(user: User = Depends(verify_token)) -> User:
    return user
