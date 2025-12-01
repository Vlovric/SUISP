from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey

from src.utils.security_policy_manager import security_policy_manager
from src.models.user_model import UserModel

class KeyManager:
    """ Singleton za generiranje i dohvacanje kljuceva"""
    _instance = None
    _kek = None
    _pdk = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KeyManager, cls).__new__(cls)
        return cls._instance
    
    def set_kek(self, password: str, salt: bytes):
        
        if self._kek is not None:
            raise Exception("KEK is already set.")
        
        if not isinstance(password, str) or not password:
            raise ValueError("Password must be a non-empty string.")
        
        key_length = security_policy_manager.get_policy_param("kek_key_length_bytes")
        scrypt_n = security_policy_manager.get_policy_param("scrypt_cost_param_n")
        scrypt_r = security_policy_manager.get_policy_param("scrypt_block_size_r")
        scrypt_p = security_policy_manager.get_policy_param("scrypt_parallelization_param_p")
        
        kdf = Scrypt(
            salt = salt,
            length = key_length, #256-bit kljuc
            n = scrypt_n, #CPU/memory cost parametar
            r= scrypt_r, # Velicina bloka
            p= scrypt_p, # Paralelizacija
            backend=default_backend()
        )

        self._kek = kdf.derive(password.encode('utf-8'))

    def get_kek(self) -> bytes:
        if self._kek is None:
            raise Exception("KEK is not set.")
        return self._kek
    
    def get_private_key(self) -> RSAPrivateKey:
        user = UserModel.get_user()
        if user is None:
            raise Exception("User is not set.")

        private_key_encrypted = user["private_key_encrypted"]
        if private_key_encrypted is None:
            raise Exception("Private key is not set.")

        pdk = self.get_pdk()
        private_key_bytes = self.decrypt_private_key(private_key_encrypted, pdk)
        
        try:
            return serialization.load_pem_private_key(
                private_key_bytes,
                password=None,
            )
        except Exception as e:
            raise Exception(f"Privatni ključ nije u ispravnom formatu: {e}")

    def get_public_key(self) -> str:
        user = UserModel.get_user()
        if user is None:
            raise Exception("User is not set.")
        
        return user["public_key"].decode("utf-8")

    def clear_kek(self):
        if self._kek is not None:
            self._kek = b'\x00' * len(self._kek) # overwritea kljuc u memoriji, temp solution
        self._kek = None

# Dio sa MK i PDK
    
    def derive_pdk(self, master_key: bytes, pdk_salt: str) -> bytes:
        """Derivira PDK iz MK-a za enkripciju privatnog ključa"""
        hash_name = security_policy_manager.get_policy_param("pbkdf2_hash_name")
    
        return hashlib.pbkdf2_hmac(
            hash_name,
            master_key,
            pdk_salt.encode(),
            1
        )

    def generate_master_key(self, password: str, mk_salt: str) -> bytes:
        """Derivira Master Key iz lozinke"""
        iterations = security_policy_manager.get_policy_param("pbkdf2_iterations")
        hash_name = security_policy_manager.get_policy_param("pbkdf2_hash_name")

        return hashlib.pbkdf2_hmac(
            hash_name,
            password.encode(),
            mk_salt.encode(),
            iterations # MK ima velik broj iteracija, a PDK će imati malu, jer nije potrebno više
        )

    def set_pdk(self, master_key: bytes, pdk_salt: str):
        """Postavlja PDK nakon derivacije iz MK-a"""
        if self._pdk is not None:
            raise Exception("PDK is already set.")
        
        self._pdk = self.derive_pdk(master_key, pdk_salt)
    
    def get_pdk(self) -> bytes:
        """Dohvaća PDK za enkripciju/dekripciju privatnog ključa"""
        if self._pdk is None:
            raise Exception("PDK is not set.")
        return self._pdk

    def clear_pdk(self):
        if self._pdk is not None:
            self._pdk = b'\x00' * len(self._pdk)
        self._pdk = None
    
    def clear_session(self):
        """Briše sve session ključeve"""
        self.clear_kek()
        self.clear_pdk()

    # TODO refaktorirati i ubaciti u RsaHelper - nakon što se login napravi
    def generate_rsa_keypair(self) -> tuple[bytes, bytes]:
        """Generira RSA par ključeva (4096-bit)"""
        # Generiraj RSA privatni ključ
        private_key = rsa.generate_private_key(
            public_exponent=security_policy_manager.get_policy_param("rsa_public_exponent"),  # Standardna vrijednost
            key_size=security_policy_manager.get_policy_param("rsa_key_size_bits"),  # Ili 3072/4096 za veću sigurnost
        )
        public_key = private_key.public_key()
        
        # Serializiraj privatni ključ (PEM format)
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serializiraj javni ključ (PEM format)
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return (public_key_bytes, private_key_bytes)
    
    def encrypt_private_key(self, private_key: bytes, pdk: bytes) -> str:
        """Enkriptira privatni ključ s PDK-om (AES-256-GCM)"""
        aesgcm = AESGCM(pdk)
        nonce = os.urandom(12)  # 96-bit nonce za GCM
        ciphertext = aesgcm.encrypt(nonce, private_key, None)
        return nonce.hex() + "$" + ciphertext.hex() 
        

    def decrypt_private_key(self, encrypted_private_key: str, pdk: bytes) -> bytes:
        """Dekriptira privatni ključ s PDK-om"""
        parts = encrypted_private_key.split("$")
        if len(parts) != 2:
            raise ValueError("Neispravan format enkriptiranog privatnog ključa.")
        nonce = bytes.fromhex(parts[0])
        ciphertext = bytes.fromhex(parts[1])

        aesgcm = AESGCM(pdk)
        try:
            private_key = aesgcm.decrypt(nonce, ciphertext, None)
            return private_key
        except Exception as e:
            raise ValueError("Neuspješna dekripcija privatnog ključa.") from e


key_manager = KeyManager()