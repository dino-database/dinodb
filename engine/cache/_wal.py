import os
import json
import uuid

from loguru import logger

class WriteAheadLog:
    def __init__(self, log_file="data/cache/wal.log", max_size=10*1024*1024):
        self.log_file = log_file
        self.max_size = max_size

    def write_log(self, operation, key, value=None):
        log_entry = {
            'operation': operation,
            'key': str(key),
            'value': value
        }

        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) >= self.max_size:
            self._rotate_log()
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            f.flush()
            os.fsync(f.fileno())

    def _rotate_log(self):
        base, ext = os.path.splitext(self.log_file)
        for i in range(1, 1000):
            rotated_log = f"{base}.{i}{ext}"
            if not os.path.exists(rotated_log):
                os.rename(self.log_file, rotated_log)
                break

    def _read_log(self):
        log_entries = []

        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    log_entries.append(json.loads(line.strip()))
        except FileNotFoundError:
            pass
        return log_entries
    
    def recover_from_log(self, engine):
        
        logger.info("Loading data from WAL...")

        if not os.path.exists(self.log_file):
            return
        
        processed_keys = set()

        try:
            with open(self.log_file, 'r') as f:
                log_entries = [json.loads(line.strip()) for line in f]

            for entry in log_entries:
                key = entry["key"]

                try:
                    key = uuid.UUID(key)
                except ValueError:
                    pass

                if key in processed_keys:
                    continue

                operation = entry["operation"]
                value = entry.get("value")

                if operation == "insert":
                    engine.sl.insert(value, key)
                elif operation == "delete":
                    engine.sl.delete(key)
                elif operation == "update":
                    engine.sl.insert(value, key)

                processed_keys.add(key)

        except Exception as e:
            print(f"Error recovering from WAL: {e}")