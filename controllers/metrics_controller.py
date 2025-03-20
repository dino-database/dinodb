from fastapi import APIRouter, HTTPException
from services.metrics_service import MetricsService
from utility.config import database_engine

router = APIRouter()
service = MetricsService(database_engine)

@router.get("/")
async def get_metrics():
    return service.get_metrics()

@router.get("/system")
async def get_system_metrics():
    return service.get_system_metrics()

@router.get("/database")
async def get_database_metrics():
    return service.get_database_metrics()