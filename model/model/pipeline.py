from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, func, text
from ..psql import Base


class PipelineItem(Base):
    __tablename__ = "pipeline"
    __table_args__ = {"schema": "pipeline_simple"}

    id = Column("id", Integer, primary_key=True, index=True)
    class_id = Column("class_id", Integer)
    method_id = Column("method_id", Integer)
    length = Column("length", Integer)
    max_iter = Column("max_iter", Integer)
    batch_size = Column("batch_size", Integer)
    alpha = Column("alpha", Float)
    gpu = Column("gpu", Boolean)
    created_at = Column(
        "created_at", DateTime, server_default=func.now(), nullable=False
    )
    ligand = Column("ligand", String(250), server_default=text("'none'"))
    receptor = Column("receptor", String(250), server_default=text("'none'"))
    dir_name = Column("dir_name", String(250), unique=True)
    status = Column("status", String)
    # name = Column("name", Integer, index=True)
    # antigen_id = Column("antigen_id", Integer)