from datetime import datetime
from pydantic import BaseModel, Field

from api.models.user import User


class Comment(BaseModel):
    """Represents a role that can be applied to a user."""

    id: int = Field(description="The ID of the role")

    insert_time: datetime = Field(description="The time the comment was made")

    user: User = Field(description="The user that created the comment")

    value: str = Field(description="The value of the comment")

    class Config:
        orm_mode = True