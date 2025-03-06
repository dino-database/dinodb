from fastapi import APIRouter
from controllers.data_controller import router as data_router

api_router = APIRouter()
api_router.include_router(data_router, prefix="/data", tags=["Data"])