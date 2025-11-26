from typing import Literal
from src.models.log_model import LogModel
from datetime import datetime
import hashlib

class LogManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance
    
    def log(self, message):
        last_entry = LogModel.get_last_entry()
        last_hash = ''

        if (last_entry is None):
            last_hash = "0" * 128
        else:
            row = f"{last_entry['timestamp']}|{last_entry['message']}|{last_entry['hash_prev']}"
            last_hash = hashlib.sha512(row.encode()).hexdigest()

        current_time = str(datetime.now().isoformat())

        new_row = f"{current_time}|{message}|{last_hash}"
        curr_hash = hashlib.sha512(new_row.encode()).hexdigest()

        LogModel.insert_log_entry(current_time, message, curr_hash, last_hash)

log_manager = LogManager()
log = log_manager.log