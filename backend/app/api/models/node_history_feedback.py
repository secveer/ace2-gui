from datetime import datetime
from pydantic import BaseModel, Field

from api.models.feedback_type import FeedbackType
from api.models.node_history import NodeHistory
from api.models.user import User


class NodeHistoryFeedback(BaseModel):
    """Represents feedback that can be given to a historical node action."""

    id: int = Field(description="The ID of the feedback")

    feedback_type: FeedbackType = Field(description="The type of feedback that was given")

    node_history: NodeHistory = Field(description="The historical action on which the feedback was given")

    timestamp: datetime = Field(description="The time at which the feedback was given")

    user: User = Field(description="The user that gave the feedback")

    class Config:
        orm_mode = True
