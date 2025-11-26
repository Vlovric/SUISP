from src.models.db import db

class LogModel:
    @staticmethod
    def get_last_entry():
        query = "SELECT * FROM log ORDER BY rowid DESC LIMIT 1"
        return db.fetch_one(query)

    @staticmethod
    def insert_log_entry(message, hash_curr, hash_prev):
        query = "INSERT INTO log (message, hash_curr, hash_prev) VALUES (?, ?, ?)"
        return db.execute_query(query, (message, hash_curr, hash_prev))
    
    @staticmethod
    def update_log_entry(id, hash_curr):
        query = "UPDATE log SET hash_curr = ? WHERE id = ?"
        return db.execute_query(query, (hash_curr, id))