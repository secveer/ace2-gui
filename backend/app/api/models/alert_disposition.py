from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID


class AlertDispositionBase(BaseModel):
    """Represents a disposition that can be applied to an alert to denote a status such as false positive or a stage in the cyber kill chain."""

    uuid: Optional[UUID] = Field(description="The UUID of the disposition")

    description: Optional[str] = Field(description="An optional human-readable description of the disposition")

    rank: int = Field(description="A numeric value used to sort the dispositions")

    value: str = Field(description="The value of the disposition")


class AlertDispositionCreate(AlertDispositionBase):
    pass


class AlertDispositionRead(AlertDispositionBase):
    uuid: UUID = Field(description="The UUID of the disposition")

    class Config:
        orm_mode = True


class AlertDispositionUpdate(AlertDispositionBase):
    rank: Optional[int] = Field(description="A numeric value used to sort the dispositions")

    value: Optional[str] = Field(description="The value of the disposition")

    @validator("rank")
    def prevent_none_rank(cls, v):
        assert v is not None, "rank may not be None"
        return v

    @validator("value")
    def prevent_none(cls, v):
        assert v is not None, "value may not be None"
        return v