from pydantic import BaseModel, Field
from typing import Optional


class EventRiskLevel(BaseModel):
    """Represents a risk level that can be applied to an event to denote its severity."""

    description: Optional[str] = Field(description="An optional human-readable description of the risk level")

    id: int = Field(description="The ID of the risk level")

    value: str = Field(description="The value of the risk level")

    class Config:
        orm_mode = True