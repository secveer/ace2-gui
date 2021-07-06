from pydantic import Field, Json, StrictBool
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic.main import BaseModel

from api.models import type_str, validators
from api.models.analysis_module_type import AnalysisModuleTypeRead
from api.models.node import NodeRead
from api.models.observable_instance import ObservableInstanceRead


class AnalysisBase(BaseModel):
    """Represents an individual analysis that was performed."""

    analysis_module_type: Optional[UUID] = Field(
        description="""The UUID of the analysis module type that was used to perform this analysis. This can be NULL in
            the case of manually created alerts."""
    )

    details: Optional[Json] = Field(description="A JSON representation of the details produced by the analysis")

    # Any UUIDs given in this field when updating will be added to the existing ones and will not replace them.
    discovered_observables: Optional[List[UUID]] = Field(
        default_factory=list,
        description="A list of observable instance UUIDs discovered while performing this analysis"
    )

    error_message: Optional[type_str] = Field(description="An optional error message that occurred during analysis")

    # TODO - save for the end, still need to flesh out this functionality
    # event_summary: Optional[AnalysisEventSummary] = Field(
    #     description="""Optional summary information to display on an event page if this analysis is ever added to an
    #     event"""
    # )

    manual: StrictBool = Field(
        default=False, description="Whether or not this analysis was manually created by an analyst"
    )

    stack_trace: Optional[type_str] = Field(description="An optional stack trace that occurred during analysis")

    summary: Optional[type_str] = Field(description="A short summary/description of what this analysis did or found")

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the analysis")


class AnalysisCreate(AnalysisBase):
    pass


class AnalysisRead(AnalysisBase, NodeRead):
    analysis_module_type: Optional[AnalysisModuleTypeRead] = Field(
        description="The analysis module type that was used to perform this analysis"
    )

    details: Optional[dict] = Field(description="A JSON representation of the details produced by the analysis")

    discovered_observables: List[ObservableInstanceRead] = Field(
        description="A list of observable instances discovered while performing this analysis"
    )

    class Config:
        orm_mode = True


class AnalysisUpdate(AnalysisBase):
    _prevent_none: classmethod = validators.prevent_none("details", "discovered_observables", "summary")


class DiscoveredObservable(BaseModel):
    """Represents the UUID of an observable discovered during analysis."""

    uuid: UUID = Field(description="The UUID of the observable instance discovered during analysis")
