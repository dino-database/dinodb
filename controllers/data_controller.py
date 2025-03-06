from fastapi import APIRouter, HTTPException
from services.data_service import DataService
from models.data_models import DataInsertRequest, DataResponse

router = APIRouter()
service = DataService()

@router.post("/add", response_model=DataResponse)
async def add_data(request: DataInsertRequest):
    key = service.add_data(request.value)
    return { "key": key, "value": request.value }

@router.get("/get/{key}", response_model=DataResponse)
async def get_data(key: str):
    value = service.get_data(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return { "key": key, "value": value }

@router.delete("/delete/{key}")
async def delete_data(key: str):
    service.delete_data(key)
    return { "message": f"deleted {key}" }