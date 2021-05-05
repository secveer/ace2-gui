from pydantic import BaseModel, Field
from typing import List, Optional

from api.models.observable_type import ObservableType


class AnalysisModuleType(BaseModel):
    """Represents a type of analysis module registered with the core."""

    description: Optional[str] = Field(description="An optional human-readable description of the analysis module type")

    id: int = Field(description="The ID of the analysis module type")

    manual: bool = Field("Whether or not this analysis module type runs in manual mode.")

    observable_types: List[ObservableType] = Field(description="A list of observable types this analysis module type knows how to analyze")

    value: str = Field(description="The value of the analysis module type")

    class Config:
        orm_mode = True