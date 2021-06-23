from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from api.models import type_str, validators


class EventPreventionToolBase(BaseModel):
    """Represents a prevention tool that can be applied to an event to denote which tool or process stopped the
    attack."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the event prevention tool"
    )

    uuid: Optional[UUID] = Field(description="The UUID of the event prevention tool")

    value: type_str = Field(description="The value of the event prevention tool")

    _prevent_none: classmethod = validators.prevent_none("uuid", "value")


class EventPreventionToolCreate(EventPreventionToolBase):
    pass


class EventPreventionToolRead(EventPreventionToolBase):
    uuid: UUID = Field(description="The UUID of the event prevention tool")

    class Config:
        orm_mode = True


class EventPreventionToolUpdate(EventPreventionToolBase):
    value: Optional[type_str] = Field(description="The value of the event prevention tool")
