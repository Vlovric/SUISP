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
    def insert_file_entry(name, encrypted_name, path, is_binary, date_uploaded, dek_encrypted, hash):
        query = "INSERT INTO file (name, encrypted_name, path, binary, date_uploaded, dek_encrypted, hash) VALUES (?, ?, ?, ?, ?, ?, ?)"
        return db.execute_query(query, (name, encrypted_name, path, is_binary, date_uploaded, dek_encrypted, hash))
    
    @staticmethod
    def fetch_by_id(file_id):
        query = "SELECT * FROM file WHERE id = ?"
        return db.fetch_one(query, (file_id,))
    
    @staticmethod
    def delete_file_by_id(file_id):
        query = "DELETE FROM file WHERE id = ?"
        return db.execute_query(query, (file_id,))
    
    @staticmethod
    def set_file_lock(file_id, locked, new_path):
        query = "UPDATE file SET locked = ?, path = ? WHERE id = ?"
        return db.execute_query(query, (locked, new_path, file_id))
    
    @staticmethod
    def update_file_lock(file_id, path, hash, date_modified):
        query = "UPDATE file SET path = ?, hash = ?, locked = ?, date_modified = ? WHERE id = ?"
        return db.execute_query(query, (path, hash, 1, date_modified, file_id))
    
    @staticmethod
    def get_file_count():
        query = "SELECT COUNT(*) as count FROM file"
        result = db.fetch_one(query)
        return result["count"] if result else 0
    
    @staticmethod
    def fetch_all():
        query = "SELECT * FROM file"
        return db.fetch_all(query)
