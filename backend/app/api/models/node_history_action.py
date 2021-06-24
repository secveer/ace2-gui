from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

from api.models import type_str, validators


class NodeHistoryActionBase(BaseModel):
    """Represents a historical action that can be performed on a node."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the node history action"
    )

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the node history action")

    value: type_str = Field(description="The value of the node history action")


class NodeHistoryActionCreate(NodeHistoryActionBase):
    pass


class NodeHistoryActionRead(NodeHistoryActionBase):
    class Config:
        orm_mode = True


class NodeHistoryActionUpdate(NodeHistoryActionBase):
    value: Optional[type_str] = Field(description="The value of the node history action")

    _prevent_none: classmethod = validators.prevent_none("value")
