from pydantic import BaseModel, Field
from typing import Optional


class Role(BaseModel):
    """Represents a role that can be assigned to a user."""

    description: Optional[str] = Field(description="An optional human-readable description of the role")

    id: int = Field(description="The ID of the role")

    value: str = Field(description="The value of the role")

    class Config:
        orm_mode = True