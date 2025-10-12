from typing import List

from pydantic import BaseModel, Field

from ....core.gofish.models import GoFishGameParams
from ....core.shared.models import AIModel


class CreateGoFishGameRequest(BaseModel):
    """Request model for creating a Go Fish game"""

    players: List[AIModel] = Field(
        ..., description="List of AI models selected to participate in the game"
    )
    params: GoFishGameParams = Field(..., description="Game parameters")
