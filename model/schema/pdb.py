from pydantic import BaseModel
from typing import List

class PdbModel(BaseModel):
    peptide_id: int
    length: int
