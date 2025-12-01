from src.models.db import db
from datetime import datetime, timedelta

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
        
    def get_user_by_username(self, username: str) -> dict | None:
        query = "SELECT * FROM user WHERE username = ?"
        return db.fetch_one(query, (username,))

    def update_login_attempt(self, username: str, success: bool) -> bool:
        """Ažurira broj neuspjelih pokušaja prijave"""
        if success:
            query = "UPDATE user SET failed_attempts = 0, lockout_until = NULL WHERE username = ?"
        else:
            query = """
                UPDATE user 
                SET failed_attempts = failed_attempts + 1 
                WHERE username = ?
            """
        try:
            db.execute_query(query, (username,))
            return True
        except Exception as e:
            print(f"Greška pri ažuriranju pokušaja prijave: {e}")
            return False

    def set_lockout(self, username: str, lockout_seconds: int) -> bool:
        """Postavlja lockout za korisnika"""
        lockout_until = datetime.now() + timedelta(seconds=lockout_seconds)
        query = """
            UPDATE user 
            SET lockout_count = lockout_count + 1,
                lockout_until = ?
            WHERE username = ?
        """
        try:
            db.execute_query(query, (lockout_until.isoformat(), username))
            return True
        except Exception as e:
            print(f"Greška pri postavljanju lockout-a: {e}")
            return False

    def is_locked_out(self, username: str) -> tuple[bool, int]:
        """Provjerava je li korisnik blokiran. Vraća (is_locked, remaining_seconds)"""
        from datetime import datetime
        user = self.get_user_by_username(username)
        if not user or not user.get('lockout_until'):
            return False, 0
        
        lockout_until = datetime.fromisoformat(user['lockout_until'])
        now = datetime.now()
        
        if now < lockout_until:
            remaining = int((lockout_until - now).total_seconds())
            return True, remaining
        else:
            # Lockout je istekao, resetiraj
            self.update_login_attempt(username, success=True)
            return False, 0