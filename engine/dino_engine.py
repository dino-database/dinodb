from .internal._skip_list import SkipList
from .internal._sstable import SSTable
from .cache._wal import WriteAheadLog
import uuid
import os

class DinoEngine:
    def __init__(self, max_memtable_size=10*1024*1024):
        self.sl = SkipList()
        self.wal = WriteAheadLog()
        self.sstable = SSTable()
        self.max_memtable_size = max_memtable_size
        self.recover()

    def add(self, val, key=None):
        if key is None:
            key = str(uuid.uuid4())

        self.wal.write_log('insert', key, val)
        self.sl.insert(val, key)
        
        if self.sl.total_memory_usage() > self.max_memtable_size:
            self.flush_memtable_to_sstable()

        return key
    
    def search(self, key):
        # first check in the memtable
        result = self.sl.search(key)
        if result:
            return result
        
        return self.search_in_sstables(key)
    
    def get_entries_count(self):
        entries = 0

        # memtable
        current = self.sl.header.forward[0]
        while current:
            entries += 1
            current = current.forward[0]

        # sstables
        sstable_files = os.listdir(self.sstable.base_dir)
        for file in sstable_files:
            # TODO: count the entries in the sstable
            pass

        return entries

    def update(self, key, val):
        current_value = self.search(key)

        if not current_value:
            return False
                
        self.wal.write_log('update', key, current_value)
        self.sl.insert(val, key)

        return True

    
    def delete(self, key):
        self.wal.write_log('delete', key)
        self.sl.delete(key)

        # flush to sstable if memtable is full
        if self.sl.total_memory_usage() > self.max_memtable_size:
            self.flush_memtable_to_sstable()

    def recover(self):
        if os.path.exists(self.wal.log_file) and os.path.getsize(self.wal.log_file) > 0:
            self.wal.recover_from_log(self)

        self.recover_from_sstables()

    def flush_memtable_to_sstable(self):
        # Convert Memtable to a sorted list of kv pairs
        data = []
        current = self.sl.header.forward[0]
        while current:
            data.append({"key": current.key, "value": current.value})
            current = current.forward[0]

        # Wrte the data to an SSTable
        self.sstable.write_sstable(data)

        # Clear the memtable after flush
        self.sl = SkipList()

    def recover_from_sstables(self):
        sstable_files = os.listdir(self.sstable.base_dir)
        sstable_files.sort()
        for filename in sstable_files:
            if filename.endswith(".json"):
                data = self.sstable.read_sstable(filename)
                for entry in data:
                    self.sl.insert(entry["value"], entry["key"])
    
    def search_in_sstables(self, key):
        sstable_files = os.listdir(self.sstable.base_dir)
        sstable_files.sort()
        for filename in sstable_files:
            if filename.endswith(".json"):
                data = self.sstable.read_sstable(filename)
                for entry in data:
                    if entry["key"] == key:
                        return entry["value"]
                    
        return None

    def memory_usage(self):
        return self.sl.total_memory_usage()