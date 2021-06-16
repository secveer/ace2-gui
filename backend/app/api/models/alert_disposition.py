from pydantic import BaseModel, Field, StrictInt, StrictStr, validator
from typing import Optional
from uuid import UUID


class AlertDispositionBase(BaseModel):
    """Represents a disposition that can be applied to an alert to denote a status such as false positive or a stage
    in the cyber kill chain."""

    uuid: Optional[UUID] = Field(description="The UUID of the disposition")

    description: Optional[StrictStr] = Field(description="An optional human-readable description of the disposition")

    rank: StrictInt = Field(description="A numeric value used to sort the dispositions")

    value: StrictStr = Field(description="The value of the disposition")

    @validator("description", "value")
    def prevent_empty_string(cls, v):
        if isinstance(v, str):
            assert 0 < len(v), "Field can not be an empty string"
        return v

    @validator("rank", "uuid", "value")
    def prevent_none(cls, v):
        assert v is not None, "Field can not be None"
        return v


class AlertDispositionCreate(AlertDispositionBase):
    pass


class AlertDispositionRead(AlertDispositionBase):
    uuid: UUID = Field(description="The UUID of the disposition")

    class Config:
        orm_mode = True


class AlertDispositionUpdate(AlertDispositionBase):
    rank: Optional[StrictInt] = Field(description="A numeric value used to sort the dispositions")

    value: Optional[StrictStr] = Field(description="The value of the disposition")
