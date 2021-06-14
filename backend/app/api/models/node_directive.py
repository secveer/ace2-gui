from pydantic import BaseModel, Field, StrictStr, validator
from typing import Optional
from uuid import UUID


class NodeDirectiveBase(BaseModel):
    """Represents a node directive that can be applied to a node (typically an observable)."""

    description: Optional[StrictStr] = Field(description="An optional human-readable description of the node directive")

    uuid: Optional[UUID] = Field(description="The UUID of the node directive")

    value: StrictStr = Field(description="The value of the node directive")


class NodeDirectiveCreate(NodeDirectiveBase):
    pass


class NodeDirectiveRead(NodeDirectiveBase):
    uuid: UUID = Field(description="The UUID of the node directive")

    class Config:
        orm_mode = True


class NodeDirectiveUpdate(NodeDirectiveBase):
    value: Optional[StrictStr] = Field(description="The value of the node directive")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v
