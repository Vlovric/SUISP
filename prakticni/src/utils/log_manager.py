from src.models.log_model import LogModel
from cryptography.hazmat.primitives import hashes
import string
import random

class LogManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
        return cls._instance
    
    def log(self, message):
        digest = hashes.Hash(hashes.SHA512())

        last_entry = LogModel.get_last_entry()
        last_hash = ''

        if (last_entry is None):
            last_hash = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(128))
        else:
            row = last_entry["time"] + last_entry["message"] + last_entry["hash_prev"]
            digest.update(row.encode())
            bytes = digest.finalize()
            last_hash = bytes.hex()

        LogModel.insert_log_entry(message, "", last_hash)
        new_entry = LogModel.get_last_entry()

        digest = hashes.Hash(hashes.SHA512())
        row = new_entry["time"] + new_entry["message"] + new_entry["hash_prev"]
        digest.update(row.encode())
        bytes = digest.finalize()

        LogModel.update_log_entry(new_entry["id"], bytes.hex())

log_manager = LogManager()
log = log_manager.log