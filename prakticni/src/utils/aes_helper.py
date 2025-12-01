from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from src.utils.security_policy_manager import security_policy_manager
import os

class AesHelper:
    @staticmethod
    def generate_key() -> str:
        key_bytes = security_policy_manager.get_policy_param("aes_gcm_key_length_bytes")
        return os.urandom(key_bytes).hex()

    @staticmethod
    def encrypt(plaintext: str | bytes, key_hex: str) -> tuple[bytes | None, str | None]:
        try:
            iv_bytes = security_policy_manager.get_policy_param("aes_gcm_iv_length_bytes")
            iv = os.urandom(iv_bytes)
            encryptor = Cipher(
                algorithms.AES(bytes.fromhex(key_hex)),
                modes.GCM(iv),
                backend = default_backend()
            ).encryptor()

            encoded = None
            if isinstance(plaintext, str):
                encoded = plaintext.encode()
            else:
                encoded = plaintext

            ciphertext = encryptor.update(encoded) + encryptor.finalize()
            result = iv + encryptor.tag + ciphertext
            return result, None
        except Exception as e:
            print(e)
            return None, "Došlo je do greške u enkripciji."
        
    def decrypt(ciphertext: bytes, key_hex: str, is_binary: None | bool = None) -> tuple[str | bytes | None, str | None]:
        try:
            iv_bytes = security_policy_manager.get_policy_param("aes_gcm_iv_length_bytes")
            tag_bytes = security_policy_manager.get_policy_param("aes_gcm_tag_length_bytes")
            iv = ciphertext[:iv_bytes]
            tag = ciphertext[iv_bytes:iv_bytes + tag_bytes]
            actual_ct = ciphertext[iv_bytes + tag_bytes:]

            decryptor = Cipher(
                algorithms.AES(bytes.fromhex(key_hex)),
                modes.GCM(iv, tag),
                backend = default_backend()
            ).decryptor()

            plaintext_bytes = decryptor.update(actual_ct) + decryptor.finalize()

            if is_binary is not None:
                if is_binary:
                    return plaintext_bytes, None
                else:
                    return plaintext_bytes.decode("utf-8"), None
            else:
                try:
                    return plaintext_bytes.decode("utf-8"), None
                except:
                    return plaintext_bytes, None
        except:
            return None, "Došlo je do greške u dekripciji."