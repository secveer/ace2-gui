from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

from api.models import type_str, validators


class NodeDirectiveBase(BaseModel):
    """Represents a node directive that can be applied to a node (typically an observable)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the node directive")

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the node directive")

    value: type_str = Field(description="The value of the node directive")


class NodeDirectiveCreate(NodeDirectiveBase):
    pass


class NodeDirectiveRead(NodeDirectiveBase):
    class Config:
        orm_mode = True


class NodeDirectiveUpdate(NodeDirectiveBase):
    value: Optional[type_str] = Field(description="The value of the node directive")

    _prevent_none: classmethod = validators.prevent_none("value")
