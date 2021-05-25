from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID


class NodeThreatActorBase(BaseModel):
    """Represents a threat actor that can be applied to a node."""

    description: Optional[str] = Field(description="An optional human-readable description of the node threat actor")

    uuid: Optional[UUID] = Field(description="The UUID of the node threat actor")

    value: str = Field(description="The value of the node threat actor")


class NodeThreatActorCreate(NodeThreatActorBase):
    pass


class NodeThreatActorRead(NodeThreatActorBase):
    uuid: UUID = Field(description="The UUID of the node threat actor")

    class Config:
        orm_mode = True


class NodeThreatActorUpdate(NodeThreatActorBase):
    value: Optional[str] = Field(description="The value of the node threat actor")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v