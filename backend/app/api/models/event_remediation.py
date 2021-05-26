from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID


class EventRemediationBase(BaseModel):
    """Represents a remediation that can be applied to an event to denote which tasks were taken to clean up after the attack."""

    description: Optional[str] = Field(description="An optional human-readable description of the event remediation")

    uuid: Optional[UUID] = Field(description="The UUID of the event remediation")

    value: str = Field(description="The value of the event remediation")


class EventRemediationCreate(EventRemediationBase):
    pass


class EventRemediationRead(EventRemediationBase):
    uuid: UUID = Field(description="The UUID of the event remediation")

    class Config:
        orm_mode = True


class EventRemediationUpdate(EventRemediationBase):
    value: Optional[str] = Field(description="The value of the event remediation")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v