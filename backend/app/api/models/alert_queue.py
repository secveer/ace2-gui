from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from api.models import type_str, validators


class AlertQueueBase(BaseModel):
    """Represents an alert queue used to filter alerts (typically by an analyst's job function)."""

    uuid: Optional[UUID] = Field(description="The UUID of the alert queue")

    description: Optional[type_str] = Field(description="An optional human-readable description of the alert queue")

    value: type_str = Field(description="The value of the alert queue")

    _prevent_none: classmethod = validators.prevent_none("uuid", "value")


class AlertQueueCreate(AlertQueueBase):
    pass


class AlertQueueRead(AlertQueueBase):
    uuid: UUID = Field(description="The UUID of the alert queue")

    class Config:
        orm_mode = True


class AlertQueueUpdate(AlertQueueBase):
    value: Optional[type_str] = Field(description="The value of the alert queue")
