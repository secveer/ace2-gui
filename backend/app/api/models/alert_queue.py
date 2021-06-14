from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID


class AlertQueueBase(BaseModel):
    """Represents an alert queue used to filter alerts (typically by an analyst's job function)."""

    uuid: Optional[UUID] = Field(description="The UUID of the alert queue")

    description: Optional[str] = Field(description="An optional human-readable description of the alert queue")

    value: str = Field(description="The value of the alert queue")


class AlertQueueCreate(AlertQueueBase):
    pass


class AlertQueueRead(AlertQueueBase):
    uuid: UUID = Field(description="The UUID of the alert queue")

    class Config:
        orm_mode = True


class AlertQueueUpdate(AlertQueueBase):
    value: Optional[str] = Field(description="The value of the alert queue")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v
