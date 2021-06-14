from pydantic import Field, Json
from typing import List, Optional

from api.models.analysis_event_summary import AnalysisEventSummary
from api.models.analysis_module_type import AnalysisModuleType
from api.models.node import Node
from api.models.observable_instance import ObservableInstance


class Analysis(Node):
    """Represents an individual analysis that was performed."""

    analysis_module_type: AnalysisModuleType = Field(
        description="The analysis module type that was used to perform this analysis"
    )

    details: Json = Field(description="The details produced for the analysis")

    error_message: Optional[str] = Field(description="An optional error message that occurred during analysis")

    event_summary: Optional[AnalysisEventSummary] = Field(
        description="""Optional summary information to display on an event page if this analysis is ever added to an
        event"""
    )

    module_extended_version: Optional[str] = Field(
        description="An optional extended version of the analysis module that performed this analysis"
    )

    module_version: str = Field(description="The version of the analysis module that performed this analysis")

    observables: Optional[List[ObservableInstance]] = Field(
        description="An optional list of observables discovered while performing this analysis"
    )

    stack_trace: Optional[str] = Field(description="An optional stack trace that occurred during analysis")

    summary: str = Field(description="A short summary/description of what this analysis did or found")

    class Config:
        orm_mode = True
