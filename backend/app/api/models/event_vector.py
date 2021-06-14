from pydantic import BaseModel, Field, StrictStr, validator
from typing import Optional
from uuid import UUID


class EventVectorBase(BaseModel):
    """Represents a vector that can be applied to an event to denote how the attack was initiated (email, usb, etc)."""

    description: Optional[StrictStr] = Field(description="An optional human-readable description of the event vector")

    uuid: Optional[UUID] = Field(description="The UUID of the event vector")

    value: StrictStr = Field(description="The value of the event vector")


class EventVectorCreate(EventVectorBase):
    pass


class EventVectorRead(EventVectorBase):
    uuid: UUID = Field(description="The UUID of the event vector")

    class Config:
        orm_mode = True


class EventVectorUpdate(EventVectorBase):
    value: Optional[StrictStr] = Field(description="The value of the event vector")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v
