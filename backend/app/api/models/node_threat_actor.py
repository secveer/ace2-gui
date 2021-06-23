from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from api.models import type_str, validators


class NodeThreatActorBase(BaseModel):
    """Represents a threat actor that can be applied to a node."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the node threat actor"
    )

    uuid: Optional[UUID] = Field(description="The UUID of the node threat actor")

    value: type_str = Field(description="The value of the node threat actor")

    _prevent_none: classmethod = validators.prevent_none("uuid", "value")


class NodeThreatActorCreate(NodeThreatActorBase):
    pass


class NodeThreatActorRead(NodeThreatActorBase):
    uuid: UUID = Field(description="The UUID of the node threat actor")

    class Config:
        orm_mode = True


class NodeThreatActorUpdate(NodeThreatActorBase):
    value: Optional[type_str] = Field(description="The value of the node threat actor")
