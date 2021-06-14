from pydantic import BaseModel, Field, StrictStr, validator
from typing import Optional
from uuid import UUID


class NodeTagBase(BaseModel):
    """Represents a tag that can be applied to a node (observable instance, analysis, alert, event, user)."""

    description: Optional[StrictStr] = Field(description="An optional human-readable description of the node tag")

    uuid: Optional[UUID] = Field(description="The UUID of the node tag")

    value: StrictStr = Field(description="The value of the node tag")


class NodeTagCreate(NodeTagBase):
    pass


class NodeTagRead(NodeTagBase):
    uuid: UUID = Field(description="The UUID of the node tag")

    class Config:
        orm_mode = True


class NodeTagUpdate(NodeTagBase):
    value: Optional[StrictStr] = Field(description="The value of the node tag")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v
