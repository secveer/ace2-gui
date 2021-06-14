from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID


class AlertTypeBase(BaseModel):
    """Represents a type of alert."""

    description: Optional[str] = Field(description="An optional human-readable description of the alert type")

    uuid: Optional[UUID] = Field(description="The UUID of the alert type")

    value: str = Field(description="The value of the alert type")


class AlertTypeCreate(AlertTypeBase):
    pass


class AlertTypeRead(AlertTypeBase):
    uuid: UUID = Field(description="The UUID of the alert type")

    class Config:
        orm_mode = True


class AlertTypeUpdate(AlertTypeBase):
    value: Optional[str] = Field(description="The value of the alert type")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v
