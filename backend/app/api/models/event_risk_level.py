from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from api.models import type_str, validators


class EventRiskLevelBase(BaseModel):
    """Represents a risk level that can be applied to an event to denote its severity."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the event risk level"
    )

    uuid: Optional[UUID] = Field(description="The UUID of the event risk level")

    value: type_str = Field(description="The value of the event risk level")

    _prevent_none: classmethod = validators.prevent_none("uuid", "value")


class EventRiskLevelCreate(EventRiskLevelBase):
    pass


class EventRiskLevelRead(EventRiskLevelBase):
    uuid: UUID = Field(description="The UUID of the event risk level")

    class Config:
        orm_mode = True


class EventRiskLevelUpdate(EventRiskLevelBase):
    value: Optional[type_str] = Field(description="The value of the event risk level")
