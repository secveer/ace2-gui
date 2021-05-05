from pydantic import BaseModel, Field
from typing import Optional


class EventRemediation(BaseModel):
    """Represents a remediation that can be applied to an event to denote which tasks were taken to clean up after the attack."""

    description: Optional[str] = Field(description="An optional human-readable description of the remediation")

    id: int = Field(description="The ID of the remediation")

    value: str = Field(description="The value of the remediation")

    class Config:
        orm_mode = True