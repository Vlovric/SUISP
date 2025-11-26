from src.models.db import db

class UserModel:
    @staticmethod
    def has_user(table_name):
        """Provjerava postoji li barem jedan korisnik u bazi"""
        return db.has_any(table_name)

    def register_user(self, username: str, password_hash: str, salt: str) -> bool:
        """Registrira novog korisnika u bazu podataka"""
        query = "INSERT INTO user (username, password_hash, salt) VALUES (?, ?, ?)"
        try:
            db.execute_query(query, (username, password_hash, salt))
            return True
        except Exception as e:
            print(f"Greška pri registraciji korisnika: {e}")
            return False