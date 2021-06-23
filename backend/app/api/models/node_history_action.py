from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from api.models import type_str, validators


class NodeHistoryActionBase(BaseModel):
    """Represents a historical action that can be performed on a node."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the node history action"
    )

    uuid: Optional[UUID] = Field(description="The UUID of the node history action")

    value: type_str = Field(description="The value of the node history action")

    _prevent_none: classmethod = validators.prevent_none("uuid", "value")


class NodeHistoryActionCreate(NodeHistoryActionBase):
    pass


class NodeHistoryActionRead(NodeHistoryActionBase):
    uuid: UUID = Field(description="The UUID of the node history action")

    class Config:
        orm_mode = True


class NodeHistoryActionUpdate(NodeHistoryActionBase):
    value: Optional[type_str] = Field(description="The value of the node history action")
