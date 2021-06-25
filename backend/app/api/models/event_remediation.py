from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

from api.models import type_str, validators


class EventRemediationBase(BaseModel):
    """Represents a remediation that can be applied to an event to denote which tasks were taken to clean up after
    the attack."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the event remediation"
    )

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the event remediation")

    value: type_str = Field(description="The value of the event remediation")


class EventRemediationCreate(EventRemediationBase):
    pass


class EventRemediationRead(EventRemediationBase):
    class Config:
        orm_mode = True


class EventRemediationUpdate(EventRemediationBase):
    value: Optional[type_str] = Field(description="The value of the event remediation")

    _prevent_none: classmethod = validators.prevent_none("value")
