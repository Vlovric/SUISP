from src.models.db import db

class LogModel:
    @staticmethod
    def get_last_entry():
        query = "SELECT * FROM log ORDER BY rowid DESC LIMIT 1"
        return db.fetch_one(query)

    @staticmethod
    def insert_log_entry(timestamp, message, hash_curr, hash_prev):
        query = "INSERT INTO log (timestamp, message, hash_curr, hash_prev) VALUES (?, ?, ?, ?)"
        return db.execute_query(query, (timestamp, message, hash_curr, hash_prev))