from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class NodeTagBase(BaseModel):
    """Represents a tag that can be applied to a node (observable instance, analysis, alert, event, user)."""

    description: Optional[str] = Field(description="An optional human-readable description of the node tag")

    uuid: Optional[UUID] = Field(description="The UUID of the node tag")

    value: str = Field(description="The value of the node tag")


class NodeTagCreate(NodeTagBase):
    pass


class NodeTagRead(NodeTagBase):
    uuid: UUID = Field(description="The UUID of the node tag")

    class Config:
        orm_mode = True


class NodeTagUpdate(NodeTagBase):
    value: Optional[str] = Field(description="The value of the node tag")