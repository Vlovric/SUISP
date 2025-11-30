from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class AesHelper:
    @staticmethod
    def generate_key() -> str:
        return os.urandom(32).hex()

    @staticmethod
    def encrypt(plaintext: str, key_hex: str) -> tuple[bytes | None, str | None]:
        try:
            iv = os.urandom(12) # 96-bit za GCM
            encryptor = Cipher(
                algorithms.AES(bytes.fromhex(key_hex)),
                modes.GCM(iv),
                backend = default_backend()
            ).encryptor()

            ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
            result = iv + encryptor.tag + ciphertext
            return result, None
        except:
            return None, "Došlo je do greške u enkripciji."
        
    def decrypt(ciphertext: bytes, key_hex: str) -> tuple[str | None, str | None]:
        try:
            iv = ciphertext[:12] # 96-bit za GCM
            tag = ciphertext[12:28]
            actual_ct = ciphertext[28:]

            decryptor = Cipher(
                algorithms.AES(bytes.fromhex(key_hex)),
                modes.GCM(iv, tag),
                backend = default_backend()
            ).decryptor()

            plaintext_bytes = decryptor.update(actual_ct) + decryptor.finalize()
            return plaintext_bytes.decode("utf-8"), None
        except:
            return None, "Došlo je do greške u dekripciji."