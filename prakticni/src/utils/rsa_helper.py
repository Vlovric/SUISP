from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey

class RsaHelper:
    @staticmethod
    def encrypt(plaintext: str, key: str | RSAPublicKey) -> tuple[bytes | None, str | None]:
        public_key = None
        
        if isinstance(key, str):
            try:
                public_key = serialization.load_pem_public_key(key.encode())
            except:
                return None, "Javni ključ nije u ispravnom formatu."
        else:
            public_key = key
        
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
    def decrypt(ciphertext: bytes, key: str | RSAPrivateKey) -> tuple[str | None, str | None]:
        private_key = None

        if isinstance(key, str):
            try:
                private_key = serialization.load_pem_private_key(key.encode(), password = None)
            except:
                return None, f"Privatni ključ nije u ispravnom formatu."
        else:
            private_key = key
        
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