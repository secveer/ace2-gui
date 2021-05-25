from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID


class EventTypeBase(BaseModel):
    """Represents a type that can be applied to an event (phishing, host compromise, etc)."""

    description: Optional[str] = Field(description="An optional human-readable description of the event type")

    uuid: Optional[UUID] = Field(description="The UUID of the event type")

    value: str = Field(description="The value of the event type")


class EventTypeCreate(EventTypeBase):
    pass


class EventTypeRead(EventTypeBase):
    uuid: UUID = Field(description="The UUID of the event type")

    class Config:
        orm_mode = True


class EventTypeUpdate(EventTypeBase):
    value: Optional[str] = Field(description="The value of the event type")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v