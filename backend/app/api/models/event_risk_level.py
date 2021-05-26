from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID


class EventRiskLevelBase(BaseModel):
    """Represents a risk level that can be applied to an event to denote its severity."""

    description: Optional[str] = Field(description="An optional human-readable description of the event risk level")

    uuid: Optional[UUID] = Field(description="The UUID of the event risk level")

    value: str = Field(description="The value of the event risk level")


class EventRiskLevelCreate(EventRiskLevelBase):
    pass


class EventRiskLevelRead(EventRiskLevelBase):
    uuid: UUID = Field(description="The UUID of the event risk level")

    class Config:
        orm_mode = True


class EventRiskLevelUpdate(EventRiskLevelBase):
    value: Optional[str] = Field(description="The value of the event risk level")

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v