from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from db.schemas.analysis_observable_instance_mapping import (
    analysis_observable_instance_mapping,
)
from db.schemas.node import Node


class Analysis(Node):
    __tablename__ = "analysis"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    analysis_module_type = relationship("AnalysisModuleType")

    analysis_module_type_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis_module_type.uuid"))

    details = Column(JSONB)

    error_message = Column(String)

    event_summary = Column(JSONB)

    module_extended_version = Column(String)

    module_version = Column(String)

    observables = relationship("ObservableInstance", secondary=analysis_observable_instance_mapping)

    stack_trace = Column(String)

    summary = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "analysis",
    }
