from src.models.db import db

class PrimjerModel:
    @staticmethod
    def insert_text(tekst):
        query = "INSERT INTO test (text) VALUES (?)"
        return db.execute_query(query, (tekst,))

    @staticmethod
    def fetch_text_by_id(id):
        query = "SELECT * FROM test WHERE id = ?"
        return db.fetch_one(query, (id,))

    @staticmethod
    def fetch_all_texts():
        query = "SELECT * FROM test"
        return db.fetch_all(query)