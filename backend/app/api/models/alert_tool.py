from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

from api.models import type_str, validators


class AlertToolBase(BaseModel):
    """Represents a type of alert."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the alert tool")

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the alert tool")

    value: type_str = Field(description="The value of the alert tool")


class AlertToolCreate(AlertToolBase):
    pass


class AlertToolRead(AlertToolBase):
    class Config:
        orm_mode = True


class AlertToolUpdate(AlertToolBase):
    value: Optional[type_str] = Field(description="The value of the alert tool")

    _prevent_none: classmethod = validators.prevent_none("value")
