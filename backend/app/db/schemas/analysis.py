from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from db.schemas.analysis_observable_instance_mapping import analysis_observable_instance_mapping
from db.schemas.node import Node


class Analysis(Node):
    __tablename__ = "analysis"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    analysis_module_type = relationship("AnalysisModuleType")

    analysis_module_type_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis_module_type.uuid"))

    details = Column(JSONB)

    discovered_observables = relationship("ObservableInstance", secondary=analysis_observable_instance_mapping)

    error_message = Column(String)

    # Commenting this out until this functionality is fleshed out
    # event_summary = Column(JSONB)

    manual = Column(Boolean, default=False, nullable=False)

    stack_trace = Column(String)

    summary = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "analysis",
    }
