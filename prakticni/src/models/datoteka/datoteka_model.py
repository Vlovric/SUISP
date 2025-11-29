from src.models.db import db

class DatotekaModel:
    @staticmethod
    def fetch_all():
        query = "SELECT * FROM datoteka"
        return db.fetch_all(query)