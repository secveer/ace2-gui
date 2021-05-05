from pydantic import BaseModel, Field
from typing import Optional


class EventVector(BaseModel):
    """Represents a vector that can be applied to an event to denote how the attack was initiated (email, usb, etc)."""

    description: Optional[str] = Field(description="An optional human-readable description of the vector")

    id: int = Field(description="The ID of the vector")

    value: str = Field(description="The value of the vector")

    class Config:
        orm_mode = True