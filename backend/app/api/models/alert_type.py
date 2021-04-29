from pydantic import BaseModel, Field
from typing import Optional


class AlertType(BaseModel):
    """Represents a type of alert."""

    description: Optional[str] = Field(description="An optional human-readable description of the alert type")

    id: int = Field(description="The ID of the alert type")

    value: str = Field(description="The value of the alert type")

    class Config:
        orm_mode = True