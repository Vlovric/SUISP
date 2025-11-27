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
            last_hash = self.get_log_hash(last_entry['timestamp'], last_entry['message'], last_entry['hash_prev'])

        current_time = str(datetime.now().isoformat())

        curr_hash = self.get_log_hash(current_time, message, last_hash)

        LogModel.insert_log_entry(current_time, message, curr_hash, last_hash)

    def get_log_hash(self, timestamp, message, hash_prev) -> str:
        new_row = f"{timestamp}|{message}|{hash_prev}"
        return hashlib.sha512(new_row.encode()).hexdigest()

    def validate_logs(self, logs) -> tuple[str, int]:
        prev_hash = ""

        for i in range(len(logs)):
            current_log = logs[i]
            current_log_hash = self.get_log_hash(current_log['timestamp'], current_log['message'], current_log['hash_prev'])
            if current_log_hash != current_log['hash_curr']:
                return f"Log zapisi nisu validni od zapisa s ID-om {current_log['id']} - nije validan hash tog zapisa.", i

            if i > 0:
                if prev_hash != current_log['hash_prev']:
                    return f"Log zapisi nisu validni od zapisa s ID-om {current_log['id']} - nije validan hash prethodnog zapisa.", i
                
            prev_hash = current_log_hash

        return "", -1

    def get_logs(self) -> tuple[str, str]:
        logs = LogModel.get_all_entries()
        error_message, error_id = self.validate_logs(logs)

        text = "ID | Vrijeme | Poruka\n\n"

        if len(error_message) > 0:
            text += f"ZAPISI SU MIJENJANI: {error_message}\n\n"
        else:
            text += f"Validnost svih zapisa provjerena je od strane aplikacije.\n\n"

        for i in range(len(logs)):
            log = logs[i]
            formatted_date = datetime.fromisoformat(log['timestamp']).strftime("%d.%m.%Y. %H:%M:%S")
            text += f"{log['id']} | {formatted_date} | {log['message']}"
            if (i == error_id):
                text += "  <--- POTENCIJALNE IZMJENE OD OVOG ZAPISA"
            text += "\n"

        return text, error_message

log_manager = LogManager()
log = log_manager.log