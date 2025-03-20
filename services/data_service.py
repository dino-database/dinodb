from engine.dino_engine import DinoEngine
from loguru import logger
from models.enums.query_enums import Operator, SortOrder
import os

class DataService:
    def __init__(self, engine):
        self.engine = engine
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
            data.append({"key": current.key, "value": current.value})
            current = current.forward[0]

        # Get data from the SSTables
        sstable_data = self._get_data_from_sstables()
        data.extend(sstable_data)

        filtered_data = data
        for f in request.filters:
            field = f.field
            operator = f.operator
            filter_value = f.value

            # Check if the field exists and handle None values
            for d in filtered_data:
                field_value = d.get(field)

                # If the field does not exist or is None, skip this entry
                if field_value is None:
                    continue

                # Convert filter_value to the appropriate type based on the field type (e.g., integer, float, string)
                if isinstance(field_value, str) and isinstance(filter_value, str):
                    # No conversion needed for string-based fields
                    field_value = field_value
                elif isinstance(field_value, (int, float)) and isinstance(filter_value, str):
                    # Try to convert filter_value to number if needed
                    try:
                        filter_value = int(filter_value) if isinstance(field_value, int) else float(filter_value)
                    except ValueError:
                        continue  # Skip if conversion fails

                if operator == "EQUALS":
                    filtered_data = [d for d in filtered_data if d.get(field) == filter_value]
                elif operator == "GREATER_THAN":
                    # Handle GREATER_THAN (check if field_value is greater than filter_value)
                    filtered_data = [d for d in filtered_data if field_value > filter_value]
                elif operator == "LESS_THAN":
                    # Handle LESS_THAN (check if field_value is less than filter_value)
                    filtered_data = [d for d in filtered_data if field_value < filter_value]
                elif operator == "CONTAINS":
                    # Handle CONTAINS (check if filter_value is contained in field_value for string fields)
                    filtered_data = [d for d in filtered_data if filter_value in str(field_value)]

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