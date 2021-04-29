from pydantic import BaseModel, Field


class NodeHistoryAction(BaseModel):
    """Represents a historical action that can be performed on a node."""

    id: int = Field(description="The ID of the action")

    value: str = Field(description="The value of the action")

    class Config:
        orm_mode = True