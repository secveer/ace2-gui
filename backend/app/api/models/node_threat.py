from pydantic import BaseModel, Field, StrictStr, validator
from typing import List, Optional
from uuid import UUID

from api.models.node_threat_type import NodeThreatTypeRead


class NodeThreatBase(BaseModel):
    """Represents a threat that can be applied to a node to denote things like a family of malware or specific type
    of attack."""

    description: Optional[StrictStr] = Field(description="An optional human-readable description of the threat")

    types: List[StrictStr] = Field(description="A list of types the threat represents")

    uuid: Optional[UUID] = Field(description="The UUID of the threat")

    value: StrictStr = Field(description="The value of the threat")

    @validator("types")
    def prevent_empty(cls, v):
        assert len(v), "types may not be empty"
        return v


class NodeThreatCreate(NodeThreatBase):
    pass


class NodeThreatRead(NodeThreatBase):
    types: List[NodeThreatTypeRead] = Field(description="A list of types the threat represents")

    uuid: UUID = Field(description="The UUID of the threat")

    class Config:
        orm_mode = True


class NodeThreatUpdate(NodeThreatBase):
    types: Optional[List[StrictStr]] = Field(description="A list of types the threat represents")

    value: Optional[StrictStr] = Field(description="The value of the threat")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v
