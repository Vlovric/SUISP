from src.models.db import db

class DatotekaModel:
    @staticmethod
    def fetch_all():
        query = "SELECT * FROM file"
        return db.fetch_all(query)
    
    @staticmethod
    def get_file(id):
        query = "SELECT * FROM file WHERE ID = ? LIMIT 1"
        return db.fetch_one(query, (id,))
    
    @staticmethod
    def insert_file_entry(name, path, is_binary, date_uploaded, dek_encrypted, hash):
        query = "INSERT INTO file (name, path, binary, date_uploaded, dek_encrypted, hash) VALUES (?, ?, ?, ?, ?, ?)"
        return db.execute_query(query, (name, path, is_binary, date_uploaded, dek_encrypted, hash))