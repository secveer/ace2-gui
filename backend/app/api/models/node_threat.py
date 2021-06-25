from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

from api.models import type_list_str, type_str, validators
from api.models.node_threat_type import NodeThreatTypeRead


class NodeThreatBase(BaseModel):
    """Represents a threat that can be applied to a node to denote things like a family of malware or specific type
    of attack."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the threat"
    )

    types: type_list_str = Field(description="A list of types the threat represents")

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the threat")

    value: type_str = Field(description="The value of the threat")


class NodeThreatCreate(NodeThreatBase):
    pass


class NodeThreatRead(NodeThreatBase):
    types: List[NodeThreatTypeRead] = Field(description="A list of types the threat represents")

    class Config:
        orm_mode = True


class NodeThreatUpdate(NodeThreatBase):
    types: Optional[type_list_str] = Field(description="A list of types the threat represents")

    value: Optional[type_str] = Field(description="The value of the threat")

    _prevent_none: classmethod = validators.prevent_none("types", "value")
