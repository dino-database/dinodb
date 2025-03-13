from fastapi import APIRouter, HTTPException
from services.data_service import DataService
from models.data_models import DataInsertRequest, DataResponse
from models.query_model import QueryRequest

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

@router.post("/query")
async def query_data(request: QueryRequest):
    try:
        result = service.query_data(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying data: {str(e)}")


@router.patch("/update/{key}", response_model=DataResponse)
async def update_data(key: str, request: DataInsertRequest):
    updated = service.update_data(key, request.value)
    if updated:
        return { "key": key, "value": request.value }
    raise HTTPException(status_code=404, detail="Unable to update the data")

@router.delete("/delete/{key}")
async def delete_data(key: str):
    service.delete_data(key)
    return { "message": f"deleted {key}" }