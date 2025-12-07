from src.utils.security_policy_manager import security_policy_manager
from src.models.user_model import UserModel
from src.models.datoteka.datoteka_model import DatotekaModel
from src.utils.key_manager import key_manager
from src.utils.rsa_helper import RsaHelper
from src.utils.log_manager import log
from src.models.db import db
from datetime import datetime

class KeyRotationHelper():

    @staticmethod
    def rotate_keys(progress_callback=None) -> tuple[bool, str | None]:
        try:

            file_count = DatotekaModel.get_file_count()
            public_key, private_key = key_manager.generate_rsa_keypair()
            public_key_pem = public_key.decode('utf-8')
            old_private_key = key_manager.get_private_key()
            pdk = key_manager.get_pdk()
            files =  DatotekaModel.fetch_all() or []
            
            conn = db.get_connection()
            try:
                cursor = conn.cursor()

                current = 0
                for f in files:
                    dek_encrypted = bytes.fromhex(f["dek_encrypted"])
                    dek, err = RsaHelper.decrypt(dek_encrypted, old_private_key)
                    if err:
                        conn.rollback()
                        return False, f"Greška pri dekripciji DEK-a za datoteku s imenom {f['name']}: {err}"
                    
                    new_dek, err2 =  RsaHelper.encrypt(dek, public_key_pem)
                    dek = b'\x00' * len(dek)
                    del dek

                    if err2:
                        conn.rollback()
                        return False, f"Greška pri enkripciji DEK-a za datoteku s imenom {f['name']}: {err2}"
                    
                    cursor.execute(
                        "UPDATE file SET dek_encrypted = ? WHERE id = ?",
                        (new_dek.hex(), f["id"])
                    )

                    current += 1
                    if progress_callback:
                        progress_callback(current, file_count)
                
                bits = old_private_key.key_size
                bytes_len = (bits+7) // 8
                old_private_key = b'\x00' * bytes_len
                del old_private_key

                
                private_key_encrypted = key_manager.encrypt_private_key(private_key, pdk)
                
                pdk = b'\x00' * len(pdk)
                del pdk

                private_key = b'\x00' * len(private_key)
                del private_key

                now_iso = datetime.now().isoformat()
                user = UserModel().get_user()


                cursor.execute(
                    "UPDATE user SET public_key = ?, private_key_encrypted = ?, last_key_rotation = ? WHERE id = ?",
                    (public_key, private_key_encrypted, now_iso, user["id"])
                )

                conn.commit()
            except Exception as e:
                conn.rollback()
                return False, str(e)
            finally:
                conn.close()

            log("Rotacija ključeva uspješno dovršena.")
            return True, None
        
        except Exception as e:
            return False, str(e)
    
    
    @staticmethod
    def needs_rotation() -> bool:
        user =  UserModel().get_user()
        last_rotation = user.get("last_key_rotation")

        rotation_interval_days = security_policy_manager.get_policy_param("key_rotation_interval_days")
        if not last_rotation:
            return True
        
        days_since_rotation = (datetime.now() - datetime.fromisoformat(last_rotation)).days
        return days_since_rotation >= rotation_interval_days