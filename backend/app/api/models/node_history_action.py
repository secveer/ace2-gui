from pydantic import BaseModel, Field, StrictStr, validator
from typing import Optional
from uuid import UUID


class NodeHistoryActionBase(BaseModel):
    """Represents a historical action that can be performed on a node."""

    description: Optional[StrictStr] = Field(
        description="An optional human-readable description of the node history action"
    )

    uuid: Optional[UUID] = Field(description="The UUID of the node history action")

    value: StrictStr = Field(description="The value of the node history action")


class NodeHistoryActionCreate(NodeHistoryActionBase):
    pass


class NodeHistoryActionRead(NodeHistoryActionBase):
    uuid: UUID = Field(description="The UUID of the node history action")

    class Config:
        orm_mode = True


class NodeHistoryActionUpdate(NodeHistoryActionBase):
    value: Optional[StrictStr] = Field(description="The value of the node history action")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v
