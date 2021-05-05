from pydantic import BaseModel, Field


class Tag(BaseModel):
    """Represents a tag that can be applied to a node (observable instance, analysis, alert, event, user)."""

    id: int = Field(description="The ID of the tag")

    value: str = Field(description="The value of the tag")

    class Config:
        orm_mode = True