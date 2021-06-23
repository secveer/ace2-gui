from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from api.models import type_str, validators


class NodeThreatTypeBase(BaseModel):
    """Represents a type that can be applied to a threat (fraud, keylogger, ransomware, etc)."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the node threat type"
    )

    uuid: Optional[UUID] = Field(description="The UUID of the node threat type")

    value: type_str = Field(description="The value of the node threat type")

    _prevent_none: classmethod = validators.prevent_none("uuid", "value")


class NodeThreatTypeCreate(NodeThreatTypeBase):
    pass


class NodeThreatTypeRead(NodeThreatTypeBase):
    uuid: UUID = Field(description="The UUID of the node threat type")

    class Config:
        orm_mode = True


class NodeThreatTypeUpdate(NodeThreatTypeBase):
    value: Optional[type_str] = Field(description="The value of the node threat type")
