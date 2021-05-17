from pydantic import BaseModel, Field
from typing import Optional


class AlertQueueBase(BaseModel):
    """Represents an alert queue used to filter alerts (typically by an analyst's job function)."""

    description: Optional[str] = Field(description="An optional human-readable description of the alert queue")

    value: str = Field(description="The value of the alert queue")


class AlertQueueCreate(AlertQueueBase):
    pass


class AlertQueueRead(AlertQueueBase):
    id: int = Field(description="The ID of the alert queue")

    class Config:
        orm_mode = True


class AlertQueueUpdate(AlertQueueBase):
    value: Optional[str] = Field(description="The value of the alert queue")