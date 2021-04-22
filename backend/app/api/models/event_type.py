from pydantic import BaseModel, Field
from typing import Optional


class EventType(BaseModel):
    """Represents a type that can be applied to an event (phishing, host compromise, etc)."""

    description: Optional[str] = Field(description="An optional human-readable description of the type")

    id: int = Field(description="The ID of the type")

    value: str = Field(description="The value of the type")

    class Config:
        orm_mode = True