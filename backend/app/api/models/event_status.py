from pydantic import BaseModel, Field
from typing import Optional


class EventStatus(BaseModel):
    """Represents a status that can be applied to an event (open, closed, etc)."""

    description: Optional[str] = Field(description="An optional human-readable description of the status")

    id: int = Field(description="The ID of the status")

    value: str = Field(description="The value of the status")

    class Config:
        orm_mode = True