from sqlalchemy import Column, ForeignKey, Integer, Table

from db.database import Base


threat_threat_type_mapping = Table("threat_threat_type_mapping", Base.metadata,
    Column("threat_id", Integer, ForeignKey("threat.id"), index=True, primary_key=True),
    Column("threat_type_id", Integer, ForeignKey("threat_type.id"), primary_key=True)
)