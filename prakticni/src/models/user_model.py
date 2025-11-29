from src.models.db import db

class UserModel:
    @staticmethod
    def has_user(table_name):
        """Provjerava postoji li barem jedan korisnik u bazi"""
        return db.has_any(table_name)

    def register_user(
        self, 
        username: str, 
        master_password_hash: str, 
        mk_salt: str,
        pdk_salt: str,
        public_key: str,  # hex/base64 encoded
        encrypted_private_key: str  # hex/base64 encoded
    ) -> bool:
        query = """
            INSERT INTO user 
            (username, master_password_hash, mk_salt, pdk_salt, public_key, private_key_encrypted) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            db.execute_query(query, (
                username, 
                master_password_hash, 
                mk_salt, 
                pdk_salt, 
                public_key, 
                encrypted_private_key
            ))
            return True
        except Exception as e:
            print(f"Greška pri registraciji korisnika: {e}")
            return False