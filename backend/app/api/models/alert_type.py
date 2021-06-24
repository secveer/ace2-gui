from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

from api.models import type_str, validators


class AlertTypeBase(BaseModel):
    """Represents a type of alert."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the alert type")

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the alert type")

    value: type_str = Field(description="The value of the alert type")


class AlertTypeCreate(AlertTypeBase):
    pass


class AlertTypeRead(AlertTypeBase):
    class Config:
        orm_mode = True


class AlertTypeUpdate(AlertTypeBase):
    value: Optional[type_str] = Field(description="The value of the alert type")

    _prevent_none: classmethod = validators.prevent_none("value")
