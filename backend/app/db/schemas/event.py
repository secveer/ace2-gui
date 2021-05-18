from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.schemas.event_prevention_tool_mapping import event_prevention_tool_mapping
from db.schemas.event_remediation_mapping import event_remediation_mapping
from db.schemas.event_vector_mapping import event_vector_mapping
from db.schemas.helpers import utcnow
from db.schemas.node import Node


class Event(Node):
    __tablename__ = "event"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    alert_time = Column(DateTime)

    alerts = relationship("Alert", primaryjoin="Alert.event_uuid == Event.uuid")

    contain_time = Column(DateTime)

    creation_time = Column(DateTime, server_default=utcnow())

    disposition_time = Column(DateTime)

    event_time = Column(DateTime)

    name = Column(String)

    ownership_time = Column(DateTime)

    prevention_tools = relationship("EventPreventionTool", secondary=event_prevention_tool_mapping)

    remediation_time = Column(DateTime)

    remediations = relationship("EventRemediation", secondary=event_remediation_mapping)

    risk_level = relationship("EventRiskLevel")

    risk_level_uuid = Column(UUID(as_uuid=True), ForeignKey("event_risk_level.uuid"))

    status = relationship("EventStatus")

    status_uuid = Column(UUID(as_uuid=True), ForeignKey("event_status.uuid"))

    type = relationship("EventType")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("event_type.uuid"))

    vectors = relationship("EventVector", secondary=event_vector_mapping)

    __mapper_args__ = {
        "polymorphic_identity": "event",
    }