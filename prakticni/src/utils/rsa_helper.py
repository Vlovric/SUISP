from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class RsaHelper:
    @staticmethod
    def encrypt(plaintext: str, public_key_str: str) -> tuple[bytes | None, str | None]:
        public_key = None
        
        try:
            public_key = serialization.load_pem_public_key(public_key_str.encode())
        except:
            return None, "Javni ključ nije u ispravnom formatu."
        
        try:
            ciphertext =  public_key.encrypt(
                plaintext.encode(),
                padding.OAEP(
                    mgf = padding.MGF1(algorithm = hashes.SHA256()),
                    algorithm = hashes.SHA256(),
                    label = None
                )
            )
            return ciphertext, None
        except:
            return None, "Došlo je do greške u enkripciji."
        
    @staticmethod
    def decrypt(ciphertext: bytes, private_key_str: str) -> tuple[str | None, str | None]:
        private_key = None

        try:
            private_key = serialization.load_pem_private_key(private_key_str.encode(), password = None)
        except Exception as e:
            return None, f"Privatni ključ nije u ispravnom formatu: {str(e)}"
        
        try:
            plaintext_bytes = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf = padding.MGF1(algorithm = hashes.SHA256()),
                    algorithm = hashes.SHA256(),
                    label = None
                )
            )

            return plaintext_bytes.decode("utf-8"), None
        except:
            return None, "Došlo je do greške u dekripciji."