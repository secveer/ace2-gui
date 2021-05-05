from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.analysis_module_type_observable_type_mapping import analysis_module_type_observable_type_mapping


class AnalysisModuleType(Base):
    __tablename__ = "analysis_module_type"

    id = Column(Integer, primary_key=True)

    description = Column(String)

    manual = Column(Boolean, default=False, nullable=False)

    observable_types = relationship("ObservableType", secondary=analysis_module_type_observable_type_mapping)

    value = Column(String, nullable=False, unique=True, index=True)