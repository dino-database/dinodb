import psutil
import os
import time
from pathlib import Path
from utility import config

class MetricsService:
    def __init__(self, engine):
        self.engine = engine

    def _system_metrics(self):
        memory_info = psutil.virtual_memory()
        cpu_usage = psutil.cpu_percent(interval=1)
        disk_info = psutil.disk_usage("/")

        return {
            "memory_used_mb": memory_info.used / (1024 ** 2),
            "memory_avaliable_mb": memory_info.available / (1024 ** 2),
            "cpu_usage_percent": cpu_usage,
            "disk_used_gb": disk_info.used / (1024 ** 3),
            "disk_free_gb": disk_info.free / (1024 ** 3),
            "uptime_seconds": round(time.time() - config.db_start_time, 2)
        }
    
    def _database_metrics(self):

        wal_size = self.engine.memory_usage()
        memtable_size = "temp"
        sstable_count = "temp"

        return {
            "total_entries": "temp", # memtable_size + sum(len(db.sstable.read_sstable(f"sstable_{i}.json")) for i in range(sstable_count)),
            "wal_file_size_bytes": wal_size,
            "memtable_size": memtable_size,
            "sstable_file_count": sstable_count,
        }

    def get_metrics(self):

        return { 
            "database_metrics": self._database_metrics(), 
            "system_metrics": self._system_metrics() 
        }
    
    def get_system_metrics(self):
        
        return {
            "system_metrics": self._system_metrics()
        }
    
    def get_database_metrics(self):
        
        return {
            "database_metrics": self._database_metrics()
        }
        
        
        # Database Metrics
        #wal_size = os.path.getsize("wal.log") if os.path.exists("wal.log") else 0
        #memtable_size = len(db.sl)  # Assuming 'db.sl' is your MemTable (SkipList)
        #sstable_count = len([f for f in Path(".").glob("sstable_*.json")])

        # return {
            # "database_metrics": {
            #     "total_entries": memtable_size + sum(len(db.sstable.read_sstable(f"sstable_{i}.json")) for i in range(sstable_count)),
            #     "wal_file_size_bytes": wal_size,
            #     "memtable_size": memtable_size,
            #     "sstable_file_count": sstable_count,
            # },