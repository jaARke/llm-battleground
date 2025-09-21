from datetime import datetime

from fastapi import APIRouter

from .models import HealthCheckResponse

router = APIRouter(prefix="/api/py", tags=["health"])


@router.get("/healthcheck", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(
        status="OK",
        timestamp=datetime.utcnow(),
    )
