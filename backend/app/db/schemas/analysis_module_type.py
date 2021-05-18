from sqlalchemy import func, Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.analysis_module_type_observable_type_mapping import analysis_module_type_observable_type_mapping


class AnalysisModuleType(Base):
    __tablename__ = "analysis_module_type"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    description = Column(String)

    manual = Column(Boolean, default=False, nullable=False)

    observable_types = relationship("ObservableType", secondary=analysis_module_type_observable_type_mapping)

    value = Column(String, nullable=False, unique=True, index=True)