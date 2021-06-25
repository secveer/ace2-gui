from pydantic import BaseModel, Field, StrictBool
from typing import List, Optional
from uuid import UUID, uuid4

from api.models import type_str, validators
from api.models.observable_type import ObservableTypeRead


class AnalysisModuleTypeBase(BaseModel):
    """Represents a type of analysis module registered with the core."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the analysis module type"
    )

    manual: StrictBool = Field(
        default=False,
        description="Whether or not this analysis module type runs in manual mode.",
    )

    observable_types: List[type_str] = Field(
        default_factory=list,
        description="""A list of observable types this analysis module type knows how to analyze.
        An empty list means it supports ALL observable types.""",
    )

    uuid: UUID = Field(default_factory=uuid4, description="The UUID of the analysis module type")

    value: type_str = Field(description="The value of the analysis module type")


class AnalysisModuleTypeCreate(AnalysisModuleTypeBase):
    pass


class AnalysisModuleTypeRead(AnalysisModuleTypeBase):
    observable_types: List[ObservableTypeRead] = Field(
        description="""A list of observable types this analysis module type knows how to analyze.
        An empty list means it supports ALL observable types."""
    )

    class Config:
        orm_mode = True


class AnalysisModuleTypeUpdate(AnalysisModuleTypeBase):
    manual: Optional[StrictBool] = Field(
        description="Whether or not this analysis module type runs in manual mode.",
    )

    observable_types: Optional[List[type_str]] = Field(
        description="""A list of observable types this analysis module type knows how to analyze.
        An empty list means it supports ALL observable types.""",
    )

    value: Optional[type_str] = Field(description="The value of the analysis module type")

    _prevent_none: classmethod = validators.prevent_none("manual", "observable_types", "value")
