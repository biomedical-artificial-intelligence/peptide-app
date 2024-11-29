from sqlalchemy import Column, Integer, String, DateTime, Float, func
from ..psql import Base


class ResultItem(Base):
    __tablename__ = "result"
    __table_args__ = {"schema": "pipeline_simple"}
    id = Column("id", Integer, primary_key=True, index=True)
    pipeline_id = Column("pipeline_id", Integer)
    receptor = Column("receptor", String(100))
    ligand = Column("ligand", String(100))
    method = Column("method", Integer)
    iter = Column("iter", Integer)
    first = Column("first", Float)
    second = Column("second", Float)
    third = Column("third", Float)
    fourth = Column("fourth", Integer)
    fifth = Column("fifth", Integer)
    sixth = Column("sixth", Integer)
    score = Column("score", Float)
    sequence = Column("sequence", String)
    batch = Column("batch", Integer)
    created_at = Column(
        "created_at", DateTime, server_default=func.now(), nullable=False
    )