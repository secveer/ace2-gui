from sqlalchemy import Column, ForeignKey, Integer, Table

from db.database import Base


analysis_module_type_observable_type_mapping = Table("analysis_module_type_observable_type_mapping", Base.metadata,
    Column("analysis_module_type_id", Integer, ForeignKey("analysis_module_type.id"), index=True, primary_key=True),
    Column("observable_type_id", Integer, ForeignKey("observable_type.id"), primary_key=True)
)