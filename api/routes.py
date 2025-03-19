from fastapi import APIRouter

from controllers.data_controller import router as data_router
from controllers.metrics_controller import router as metrics_router

api_router = APIRouter()

api_router.include_router(data_router, prefix="/data", tags=["Data"])
api_router.include_router(metrics_router, prefix="/metrics", tags=["Metrics"])