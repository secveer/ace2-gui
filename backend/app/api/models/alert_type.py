from pydantic import BaseModel, Field, StrictStr, validator
from typing import Optional
from uuid import UUID


class AlertTypeBase(BaseModel):
    """Represents a type of alert."""

    description: Optional[StrictStr] = Field(description="An optional human-readable description of the alert type")

    uuid: Optional[UUID] = Field(description="The UUID of the alert type")

    value: StrictStr = Field(description="The value of the alert type")

    @validator("description", "value")
    def prevent_empty_string(cls, v):
        if isinstance(v, str):
            assert 0 < len(v), "Field can not be an empty string"
        return v

    @validator("uuid", "value")
    def prevent_none(cls, v):
        assert v is not None, "Field can not be None"
        return v


class AlertTypeCreate(AlertTypeBase):
    pass


class AlertTypeRead(AlertTypeBase):
    uuid: UUID = Field(description="The UUID of the alert type")

    class Config:
        orm_mode = True


class AlertTypeUpdate(AlertTypeBase):
    value: Optional[StrictStr] = Field(description="The value of the alert type")
