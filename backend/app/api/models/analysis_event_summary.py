from pydantic import BaseModel, Field
from typing import List, Optional


class AnalysisEventSummary(BaseModel):
    """Represents a summary of an analysis information to be displayed on an event page in the GUI."""

    detection_points: Optional[List[str]] = Field(description="An optional list of detection points found during analysis")

    