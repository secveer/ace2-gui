from sqlalchemy import func, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.node_directive_mapping import node_directive_mapping
from db.schemas.node_tag_mapping import node_tag_mapping
from db.schemas.node_threat_mapping import node_threat_mapping


# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#joined-table-inheritance
class Node(Base):
    __tablename__ = "node"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    comments = relationship("Comment")

    directives = relationship("Directive", secondary=node_directive_mapping)

    node_type = Column(String)
    
    tags = relationship("Tag", secondary=node_tag_mapping)

    threat_actor = relationship("ThreatActor")

    threat_actor_id = Column(Integer, ForeignKey("threat_actor.id"))

    threats = relationship("Threat", secondary=node_threat_mapping)

    __mapper_args__ = {
        "polymorphic_identity": "node",
        "polymorphic_on": node_type
    }