from src.models.db import db

class DatotekaModel:
    @staticmethod
    def fetch_all_locked():
        query = "SELECT * FROM file WHERE locked = 1"
        return db.fetch_all(query)
    
    @staticmethod
    def fetch_all_unlocked():
        query = "SELECT * FROM file WHERE locked = 0"
        return db.fetch_all(query)
    
    @staticmethod
    def insert_file_entry(name, path, is_binary, date_uploaded, dek_encrypted, hash):
        query = "INSERT INTO file (name, path, binary, date_uploaded, dek_encrypted, hash) VALUES (?, ?, ?, ?, ?, ?)"
        return db.execute_query(query, (name, path, is_binary, date_uploaded, dek_encrypted, hash))
    
    @staticmethod
    def fetch_by_id(file_id):
        query = "SELECT * FROM file WHERE id = ?"
        return db.fetch_one(query, (file_id,))
    
    @staticmethod
    def set_file_lock(file_id, locked, new_path):
        query = "UPDATE file SET locked = ?, path = ? WHERE id = ?"
        return db.execute_query(query, (locked, new_path, file_id))