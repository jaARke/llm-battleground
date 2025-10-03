import logging
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from .models import User

# JWT Configuration
JWT_SECRET = os.getenv("NEXTAUTH_SECRET", None)
JWT_ALGORITHM = "HS256"

# Security scheme
security = HTTPBearer()

logger = logging.getLogger(__name__)


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    if JWT_SECRET is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT secret not configured",
        )
    try:
        token = credentials.credentials

        # Decode the JWT token using the same secret as NextAuth
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # Extract user information
        username = payload.get("name")
        user_id = payload.get("sub")  # NextAuth uses 'sub' for user ID
        email = payload.get("email")

        if username is None or user_id is None or email is None:
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
