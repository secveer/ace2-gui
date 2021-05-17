from pydantic import BaseModel, Field
from typing import Optional


class DispositionBase(BaseModel):
    """Represents a disposition that can be applied to an alert to denote a status such as false positive or a stage in the cyber kill chain."""

    description: Optional[str] = Field(description="An optional human-readable description of the disposition")

    rank: int = Field(description="A numeric value used to sort the dispositions")

    value: str = Field(description="The value of the disposition")


class DispositionCreate(DispositionBase):
    pass


class DispositionRead(DispositionBase):
    id: int = Field(description="The ID of the disposition")

    class Config:
        orm_mode = True


class DispositionUpdate(DispositionBase):
    rank: Optional[int] = Field(description="A numeric value used to sort the dispositions")

    value: Optional[str] = Field(description="The value of the disposition")