from pydantic import BaseModel, Field


class ObservableType(BaseModel):
    """Represents a type of observable that the application knows about."""

    id: int = Field(description="The ID of the observable type")

    value: str = Field(description="The value of the observable type")

    class Config:
        orm_mode = True