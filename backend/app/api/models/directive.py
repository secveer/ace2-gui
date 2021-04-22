from pydantic import BaseModel, Field
from typing import Optional


class Directive(BaseModel):
    """Represents a directive that can be applied to a node (typically an observable)."""

    description: Optional[str] = Field(description="An optional human-readable description of the directive")

    id: int = Field(description="The ID of the directive")

    value: str = Field(description="The value of the directive")

    class Config:
        orm_mode = True