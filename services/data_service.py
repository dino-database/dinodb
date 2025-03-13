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
    
    def update_data(self, key, value: dict) -> bool:
        updated = self.engine.update(key, value)
        if updated:
            logger.info(f"[+] Updated data for: {key}")
            return True
        return False

    def delete_data(self, key: str):
        self.engine.delete(key)
        logger.info(f"[-] Deleted data for: {key}")