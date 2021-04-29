from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
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

    risk_level_id = Column(Integer, ForeignKey("event_risk_level.id"))

    status = relationship("EventStatus")

    status_id = Column(Integer, ForeignKey("event_status.id"))

    type = relationship("EventType")

    type_id = Column(Integer, ForeignKey("event_type.id"))

    vectors = relationship("EventVector", secondary=event_vector_mapping)

    __mapper_args__ = {
        "polymorphic_identity": "event",
    }