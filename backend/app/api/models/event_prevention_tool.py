from pydantic import BaseModel, Field
from typing import Optional


class EventPreventionTool(BaseModel):
    """Represents a prevention tool that can be applied to an event to denote which tool or process stopped the attack."""

    description: Optional[str] = Field(description="An optional human-readable description of the prevention tool")

    id: int = Field(description="The ID of the prevention tool")

    value: str = Field(description="The value of the prevention tool")

    class Config:
        orm_mode = True