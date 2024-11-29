from pydantic import BaseModel
from typing import List

class HomeOutput(BaseModel):
    total_pipeline: list[int]
    page_size: int
    total_page: int
    page_num: int