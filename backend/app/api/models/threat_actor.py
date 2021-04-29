from pydantic import BaseModel, Field
from typing import Optional


class ThreatActor(BaseModel):
    """Represents a threat actor that can be applied to a node."""

    description: Optional[str] = Field(description="An optional human-readable description of the threat actor")

    id: int = Field(description="The ID of the threat actor")

    value: str = Field(description="The value of the threat actor")

    class Config:
        orm_mode = True