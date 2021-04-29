from datetime import datetime
from pydantic import BaseModel, Field

from api.models.observable_type import ObservableType


class Observable(BaseModel):
    """Represents a unique observable (based on the type+value)."""

    expires_on: datetime = Field(description="The time the observable will expire and no longer be included in observable detection exports")

    for_detection: bool = Field(description="Whether or not this observable should be included in the observable detection exports")

    id: int = Field(description="The ID of the observable")

    type: ObservableType = Field(description="The type of the observable")

    value: str = Field(description="The value of the observable")

    class Config:
        orm_mode = True