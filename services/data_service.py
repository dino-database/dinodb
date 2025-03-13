from engine.dino_engine import DinoEngine
from loguru import logger
from models.enums.query_enums import Operator, SortOrder
import os

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
    
    def query_data(self, request):
        # Get data from the SkipList
        data = []
        current = self.engine.sl.header.forward[0]
        while current:
            print(f"Found data: 'key': {current.key}, 'value': {current.value}")
            data.append({"key": current.key, "value": current.value})
            current = current.forward[0]

        # Get data from the SSTables
        sstable_data = self._get_data_from_sstables()
        data.extend(sstable_data)

        # Apply filters based on the request
        filtered_data = data
        for f in request.filters:
            if f.operator == Operator.EQUALS:
                filtered_data = [d for d in filtered_data if d.get(f.field) == f.value]
            elif f.operator == Operator.GREATER_THAN:
                filtered_data = [d for d in filtered_data if d.get(f.field, 0) > int(f.value)]
            elif f.operator == Operator.LESS_THAN:
                filtered_data = [d for d in filtered_data if d.get(f.field, 0) < int(f.value)]
            elif f.operator == Operator.CONTAINS:
                filtered_data = [d for d in filtered_data if f.value in d.get(f.field, '')]

        # Apply sorting if specified
        if request.sort:
            filtered_data.sort(
                key=lambda x: x.get(request.sort.field),
                reverse=request.sort.order == SortOrder.DESC
            )

        # Paginate the results
        start = request.page * request.size
        end = start + request.size
        logger.info(f"[+] Queryed data: {len(filtered_data)} entries returned")
        return filtered_data[start:end]
    
    def _get_data_from_sstables(self):
        # Get data from all SSTables
        data = []
        sstable_files = os.listdir(self.engine.sstable.base_dir)
        sstable_files.sort()
        for filename in sstable_files:
            if filename.endswith(".json"):
                sstable_data = self.engine.sstable.read_sstable(filename)
                data.extend(sstable_data)
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