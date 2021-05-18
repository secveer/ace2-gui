from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class DirectiveBase(BaseModel):
    """Represents a directive that can be applied to a node (typically an observable)."""

    description: Optional[str] = Field(description="An optional human-readable description of the directive")

    uuid: Optional[UUID] = Field(description="The UUID of the directive")

    value: str = Field(description="The value of the directive")


class DirectiveCreate(DirectiveBase):
    pass


class DirectiveRead(DirectiveBase):
    uuid: UUID = Field(description="The UUID of the directive")

    class Config:
        orm_mode = True


class DirectiveUpdate(DirectiveBase):
    value: Optional[str] = Field(description="The value of the directive")