from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID


class EventPreventionToolBase(BaseModel):
    """Represents a prevention tool that can be applied to an event to denote which tool or process stopped the attack."""

    description: Optional[str] = Field(description="An optional human-readable description of the event prevention tool")

    uuid: Optional[UUID] = Field(description="The UUID of the event prevention tool")

    value: str = Field(description="The value of the event prevention tool")


class EventPreventionToolCreate(EventPreventionToolBase):
    pass


class EventPreventionToolRead(EventPreventionToolBase):
    uuid: UUID = Field(description="The UUID of the event prevention tool")

    class Config:
        orm_mode = True


class EventPreventionToolUpdate(EventPreventionToolBase):
    value: Optional[str] = Field(description="The value of the event prevention tool")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v