from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from api.models import type_str, validators


class EventTypeBase(BaseModel):
    """Represents a type that can be applied to an event (phishing, host compromise, etc)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the event type")

    uuid: Optional[UUID] = Field(description="The UUID of the event type")

    value: type_str = Field(description="The value of the event type")

    _prevent_none: classmethod = validators.prevent_none("uuid", "value")


class EventTypeCreate(EventTypeBase):
    pass


class EventTypeRead(EventTypeBase):
    uuid: UUID = Field(description="The UUID of the event type")

    class Config:
        orm_mode = True


class EventTypeUpdate(EventTypeBase):
    value: Optional[type_str] = Field(description="The value of the event type")
