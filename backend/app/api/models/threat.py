from pydantic import BaseModel, Field
from typing import Optional

from api.models.threat_type import ThreatType


class Threat(BaseModel):
    """Represents a threat that can be applied to a node to denote things like a family of malware or specific type of attack."""

    description: Optional[str] = Field(description="An optional human-readable description of the threat")

    id: int = Field(description="The ID of the threat")

    type: ThreatType = Field(description="The type of the threat")

    value: str = Field(description="The value of the threat")

    class Config:
        orm_mode = True