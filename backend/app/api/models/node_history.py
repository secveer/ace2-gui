from datetime import datetime
from pydantic import BaseModel, Field, Json, UUID4

from api.models.node import Node
from api.models.node_history_action import NodeHistoryAction
from api.models.user import User


class NodeHistory(BaseModel):
    """Represents a historical action performed on a node."""

    id: int = Field(description="The ID of the historical action")

    action: NodeHistoryAction = Field(description="The action that was performed")

    action_user: User = Field(description="The user that performed the action")

    after: Json = Field(description="The JSON representation of the node after the action was performed")

    before: Json = Field(description="The JSON representation of the node before the action was performed")

    node: Node = Field(description="The node on which the action was performed")

    timestamp: datetime = Field(description="The time the action was performed")

    class Config:
        orm_mode = True