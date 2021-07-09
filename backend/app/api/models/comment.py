from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

from api.models import type_str
from api.models.user import UserRead


class CommentBase(BaseModel):
    """Represents a comment that can be added to a node."""

    insert_time: datetime = Field(default_factory=datetime.utcnow, description="The time the comment was made")

    node_uuid: UUID = Field(description="The UUID of the node associated with this comment")

    user: type_str = Field(description="The username that created the comment")

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the comment")

    value: type_str = Field(description="The value of the comment")


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    user: UserRead = Field(description="The user that created the comment")

    class Config:
        orm_mode = True


class CommentUpdate(BaseModel):
    # The only thing that makes sense to be able to update is the actual value of the comment.
    # Otherwise, you would delete the comment and create a new comment on a new node. Since value
    # is the only field to update, it does not use Optional like the other Pydantic models.
    value: type_str = Field(description="The value of the comment")
