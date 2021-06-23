from pydantic import BaseModel, Field, StrictBool
from typing import List, Optional
from uuid import UUID

from api.models import type_str, validators
from api.models.observable_type import ObservableTypeRead


class AnalysisModuleTypeBase(BaseModel):
    """Represents a type of analysis module registered with the core."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the analysis module type"
    )

    uuid: Optional[UUID] = Field(description="The UUID of the analysis module type")

    manual: Optional[StrictBool] = Field(
        default=False,
        description="Whether or not this analysis module type runs in manual mode.",
    )

    # The default_factory parameter allows you to create an analysis module type without specifying the observable
    # types. This will automatically fill in the field with an empty list in that case.
    observable_types: Optional[List[type_str]] = Field(
        default_factory=list,
        description="""A list of observable types this analysis module type knows how to analyze.
        An empty list means it supports ALL observable types.""",
    )

    value: type_str = Field(description="The value of the analysis module type")

    _prevent_none: classmethod = validators.prevent_none("manual", "observable_types", "uuid", "value")


class AnalysisModuleTypeCreate(AnalysisModuleTypeBase):
    pass


class AnalysisModuleTypeRead(AnalysisModuleTypeBase):
    observable_types: List[ObservableTypeRead] = Field(
        description="""A list of observable types this analysis module type knows how to analyze.
        An empty list means it supports ALL observable types."""
    )

    uuid: UUID = Field(description="The UUID of the analysis module type")

    class Config:
        orm_mode = True


class AnalysisModuleTypeUpdate(AnalysisModuleTypeBase):
    value: Optional[type_str] = Field(description="The value of the analysis module type")
