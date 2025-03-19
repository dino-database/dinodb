from fastapi import APIRouter, HTTPException
from services.metrics_service import MetricsService

router = APIRouter()
service = MetricsService()

@router.get("/")
async def get_metrics():
    return service.get_metrics()