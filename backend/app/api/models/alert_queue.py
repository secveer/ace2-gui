from pydantic import BaseModel, Field, StrictStr, validator
from typing import Optional
from uuid import UUID


class AlertQueueBase(BaseModel):
    """Represents an alert queue used to filter alerts (typically by an analyst's job function)."""

    uuid: Optional[UUID] = Field(description="The UUID of the alert queue")

    description: Optional[StrictStr] = Field(description="An optional human-readable description of the alert queue")

    value: StrictStr = Field(description="The value of the alert queue")

    @validator("description", "value")
    def prevent_empty_string(cls, v):
        if isinstance(v, str):
            assert 0 < len(v), "Field can not be an empty string"
        return v

    @validator("uuid", "value")
    def prevent_none(cls, v):
        assert v is not None, "Field can not be None"
        return v


class AlertQueueCreate(AlertQueueBase):
    pass


class AlertQueueRead(AlertQueueBase):
    uuid: UUID = Field(description="The UUID of the alert queue")

    class Config:
        orm_mode = True


class AlertQueueUpdate(AlertQueueBase):
    value: Optional[StrictStr] = Field(description="The value of the alert queue")
