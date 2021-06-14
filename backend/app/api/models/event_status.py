from pydantic import BaseModel, Field, StrictStr, validator
from typing import Optional
from uuid import UUID


class EventStatusBase(BaseModel):
    """Represents a status that can be applied to an event (open, closed, etc)."""

    description: Optional[StrictStr] = Field(description="An optional human-readable description of the event status")

    uuid: Optional[UUID] = Field(description="The UUID of the event status")

    value: StrictStr = Field(description="The value of the event status")


class EventStatusCreate(EventStatusBase):
    pass


class EventStatusRead(EventStatusBase):
    uuid: UUID = Field(description="The UUID of the event status")

    class Config:
        orm_mode = True


class EventStatusUpdate(EventStatusBase):
    value: Optional[StrictStr] = Field(description="The value of the event status")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v
