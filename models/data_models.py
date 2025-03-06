from pydantic import BaseModel
from typing import Optional

class DataInsertRequest(BaseModel):
    value: dict # JSON data

class DataResponse(BaseModel):
    key: str
    value: Optional[dict]

