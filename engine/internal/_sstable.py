import os
import json

class SSTable:
    def __init__(self, base_dir="../data/sstables", file_prefix="sstable"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.file_prefix = file_prefix
        self.counter = 0
        self.current_file = None

    def _generate_filename(self):
        return f"{self.base_dir}/{self.file_prefix}_{self.counter}.json"
    
    def write_sstable(self, data):
        filename = self._generate_filename()
        with open(filename, 'w') as f:
            json.dump(data, f)
        self.counter += 1
        return filename
    
    def read_sstable(self, filename):
        dir = f"{self.base_dir}/{filename}"
        with open(dir, 'r') as f:
            return json.load(f)