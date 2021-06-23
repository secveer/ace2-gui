from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from api.models import type_int, type_str, validators


class AlertDispositionBase(BaseModel):
    """Represents a disposition that can be applied to an alert to denote a status such as false positive or a stage
    in the cyber kill chain."""

    uuid: Optional[UUID] = Field(description="The UUID of the disposition")

    description: Optional[type_str] = Field(description="An optional human-readable description of the disposition")

    rank: type_int = Field(description="An integer value used to sort the dispositions")

    value: type_str = Field(description="The value of the disposition")

    _prevent_none: classmethod = validators.prevent_none("rank", "uuid", "value")


class AlertDispositionCreate(AlertDispositionBase):
    pass


class AlertDispositionRead(AlertDispositionBase):
    uuid: UUID = Field(description="The UUID of the disposition")

    class Config:
        orm_mode = True


class AlertDispositionUpdate(AlertDispositionBase):
    rank: Optional[type_int] = Field(description="An integer value used to sort the dispositions")

    value: Optional[type_str] = Field(description="The value of the disposition")
