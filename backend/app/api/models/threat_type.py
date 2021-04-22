from pydantic import BaseModel, Field
from typing import Optional


class ThreatType(BaseModel):
    """Represents a type that can be applied to a threat (fraud, keylogger, ransomware, etc)."""

    description: Optional[str] = Field(description="An optional human-readable description of the threat type")

    id: int = Field(description="The ID of the threat type")

    value: str = Field(description="The value of the threat type")

    class Config:
        orm_mode = True