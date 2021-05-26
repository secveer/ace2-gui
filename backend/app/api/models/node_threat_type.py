from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID


class NodeThreatTypeBase(BaseModel):
    """Represents a type that can be applied to a threat (fraud, keylogger, ransomware, etc)."""

    description: Optional[str] = Field(description="An optional human-readable description of the node threat type")

    uuid: Optional[UUID] = Field(description="The UUID of the node threat type")

    value: str = Field(description="The value of the node threat type")


class NodeThreatTypeCreate(NodeThreatTypeBase):
    pass


class NodeThreatTypeRead(NodeThreatTypeBase):
    uuid: UUID = Field(description="The UUID of the node threat type")

    class Config:
        orm_mode = True


class NodeThreatTypeUpdate(NodeThreatTypeBase):
    value: Optional[str] = Field(description="The value of the node threat type")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v