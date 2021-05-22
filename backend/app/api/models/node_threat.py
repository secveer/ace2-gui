from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

from api.models.node_threat_type import NodeThreatTypeRead


class NodeThreatBase(BaseModel):
    """Represents a threat that can be applied to a node to denote things like a family of malware or specific type of attack."""

    description: Optional[str] = Field(description="An optional human-readable description of the threat")

    types: List[str] = Field(description="A list of types the threat represents")

    uuid: Optional[UUID] = Field(description="The UUID of the threat")

    value: str = Field(description="The value of the threat")


class NodeThreatCreate(NodeThreatBase):
    pass


class NodeThreatRead(NodeThreatBase):
    types: List[NodeThreatTypeRead] = Field(description="A list of types the threat represents")

    uuid: UUID = Field(description="The UUID of the threat")

    class Config:
        orm_mode = True


class NodeThreatUpdate(NodeThreatBase):
    types: Optional[List[str]] = Field(description="A list of types the threat represents")

    value: Optional[str] = Field(description="The value of the threat")