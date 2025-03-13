from pydantic import BaseModel
from typing import List, Optional
from .enums.query_enums import Operator, SortOrder 

class Filter(BaseModel):
    field: str
    operator: Operator
    value: str

class Sort(BaseModel):
    field: str
    order: SortOrder

class QueryRequest(BaseModel):
    filters: List[Filter]
    sort: Optional[Sort] = None
    page: int = 0
    size: int = 20