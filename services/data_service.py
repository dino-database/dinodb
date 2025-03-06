from engine.dino_engine import DinoEngine
from loguru import logger

class DataService:
    def __init__(self):
        self.engine = DinoEngine()
        logger.info("Engine created...")

    def add_data(self, value: dict) -> str:
        key = self.engine.add(value)
        logger.info(f"[+] New value added: {key}")
        return key

    def get_data(self, key: str) -> dict:
        data = self.engine.search(key)
        if data:
            logger.info(f"[+] Value found for key: {key}")
        return data
    
    def delete_data(self, key: str):
        self.engine.delete(key)
        logger.info(f"[-] Deleted data for: {key}")