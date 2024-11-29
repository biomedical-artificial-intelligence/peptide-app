from pydantic import BaseModel
from typing import List

class PipelineInput(BaseModel):
    class_id: int
    method_id: int
    antigen_id: int
    length: int
    max_count: int
    batch_size: int
    etc: str
    created_at: str

class PipeineOutput(BaseModel):
    pipeline_id: int
    target: str
    length: int
    now_iter: int