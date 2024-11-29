from sqlalchemy import Column, Integer, String, DateTime, Float, func
from ..psql import Base


class PipelineStatusItem(Base):
    __tablename__ = "pipeline_status"
    __table_args__ = {"schema": "pipeline_simple"}
    id = Column("id", Integer, primary_key=True, index=True)
    pipeline_id = Column("pipeline_id", Integer)
    iter = Column("iter", Integer)
    step = Column("step", Integer)