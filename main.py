from fastapi import FastAPI
from api.routes import api_router
from loguru import logger
from dotenv import load_dotenv

import os
import sys
import uvicorn
import logging

load_dotenv()

db_version = os.getenv("DB_VERSION")
stage = os.getenv("STAGE", "PROD")

app = FastAPI(
    title="DinoDB API",
    version=db_version,
    docs_url=None if stage == "PROD" else "/docs",
    redoc_url=None if stage == "PROD" else "/redoc"
)

# Disable Uvicorn's default logging
logging.getLogger("uvicorn.access").propagate = False
logging.getLogger("uvicorn.error").propagate = False

# Set up Loguru as the logger
logger.remove()  # Remove default handler

# Add file logging
logger.add("data/logs/dinodb.log", 
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", 
           level="INFO", 
           rotation="10 MB")

# Add console logging
logger.add(sys.stderr, 
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>", 
           level="INFO")

app.include_router(api_router)

if __name__ == "__main__":
    logger.info(f"DinoDB v{db_version} started...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None)  # Disable default logging config