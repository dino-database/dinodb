from fastapi import FastAPI
from api.routes import api_router
from loguru import logger
from dotenv import load_dotenv

import os
import uvicorn
import logging

app = FastAPI(
    title="DinoDB API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

load_dotenv()
db_version = os.getenv("DB_VERSION")

# Disable Uvicorn's default logging
logging.getLogger("uvicorn.access").propagate = False
logging.getLogger("uvicorn.error").propagate = False

# Set up Loguru as the logger
logger.remove()  # Remove default handler
logger.add("data/logs/dinodb.log", format="{time} {level} {message}", level="INFO", rotation="10 MB")

app.include_router(api_router)

if __name__ == "__main__":
    logger.info(f"DinoDB v{db_version} started...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None)  # Disable default logging config
