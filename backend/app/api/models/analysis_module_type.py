from pydantic import BaseModel, Field, StrictStr, StrictBool, validator
from typing import List, Optional
from uuid import UUID

from api.models.observable_type import ObservableTypeRead


class AnalysisModuleTypeBase(BaseModel):
    """Represents a type of analysis module registered with the core."""

    description: Optional[StrictStr] = Field(
        description="An optional human-readable description of the analysis module type"
    )

    uuid: Optional[UUID] = Field(description="The UUID of the analysis module type")

    manual: Optional[StrictBool] = Field(
        default=False,
        description="Whether or not this analysis module type runs in manual mode.",
    )

    # The default_factory parameter allows you to create an analysis module type without specifying the observable
    # types. This will automatically fill in the field with an empty list in that case.
    observable_types: Optional[List[StrictStr]] = Field(
        default_factory=list,
        description="""A list of observable types this analysis module type knows how to analyze.
        An empty list means it supports ALL observable types."""
    )

    value: StrictStr = Field(description="The value of the analysis module type")

    @validator("description", "value")
    def prevent_empty_string(cls, v):
        if isinstance(v, str):
            assert 0 < len(v), "Field can not be an empty string"
        return v

    @validator("observable_types")
    def prevent_empty_string_in_list(cls, v):
        assert all(0 < len(x) for x in v if isinstance(x, str)), "List can not have an empty string"
        return v

    @validator("manual", "observable_types", "uuid", "value")
    def prevent_none(cls, v):
        assert v is not None, "Field can not be None"
        return v


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
    value: Optional[StrictStr] = Field(description="The value of the analysis module type")