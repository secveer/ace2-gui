from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

from api.models import type_str, validators


class EventPreventionToolBase(BaseModel):
    """Represents a prevention tool that can be applied to an event to denote which tool or process stopped the
    attack."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the event prevention tool"
    )

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the event prevention tool")

    value: type_str = Field(description="The value of the event prevention tool")


class EventPreventionToolCreate(EventPreventionToolBase):
    pass


class EventPreventionToolRead(EventPreventionToolBase):
    class Config:
        orm_mode = True


class EventPreventionToolUpdate(EventPreventionToolBase):
    value: Optional[type_str] = Field(description="The value of the event prevention tool")

    _prevent_none: classmethod = validators.prevent_none("value")
