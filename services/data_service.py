from engine.dino_engine import DinoEngine

class DataService:
    def __init__(self):
        self.engine = DinoEngine()

    def add_data(self, value: dict) -> str:
        return self.engine.add(value)
    
    def get_data(self, key: str) -> dict:
        return self.engine.search(key)
    
    def delete_data(self, key: str):
        self.engine.delete(key)