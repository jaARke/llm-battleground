from datetime import datetime

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """Response model for health check"""

    status: str
    timestamp: datetime
