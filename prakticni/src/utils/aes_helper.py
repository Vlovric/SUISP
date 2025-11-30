from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class AesHelper:
    @staticmethod
    def generate_key() -> str:
        return os.urandom(32).hex()

    @staticmethod
    def encrypt(plaintext: str | bytes, key_hex: str) -> tuple[bytes | None, str | None]:
        try:
            iv = os.urandom(12) # 96-bit za GCM
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
        
    def decrypt(ciphertext: bytes, key_hex: str) -> tuple[str | bytes | None, str | None]:
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
            try:
                return plaintext_bytes.decode("utf-8"), None
            except:
                return plaintext_bytes, None
        except:
            return None, "Došlo je do greške u dekripciji."