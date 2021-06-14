from pydantic import BaseModel, Field
from typing import Optional


class FeedbackType(BaseModel):
    """Represents a type of feedback that can be applied to a node history entry."""

    description: Optional[str] = Field(description="An optional human-readable description of the role")

    icon: str = Field(description="A unicode character for an emoji to visually represent the type of feedback")

    id: int = Field(description="The ID of the role")

    value: str = Field(description="The value of the role")

    class Config:
        orm_mode = True
