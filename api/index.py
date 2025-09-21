from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.users import router as users_router
from .models import HealthCheckResponse

# Create FastAPI instance with custom docs and openapi url
app = FastAPI(
    title="LLM Battleground API",
    description="API for LLM Battleground application",
    version="0.2.0",
    docs_url="/api/py/docs",
    openapi_url="/api/py/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://llmbattles.jakerichard.tech"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users_router)


@app.get("/api/py/healthcheck", response_model=HealthCheckResponse, tags=["health"])
async def healthcheck():
    """
    Health check endpoint to verify API is running.
    """
    return HealthCheckResponse(status="OK", timestamp=datetime.utcnow())
