from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

from src.utils.security_policy_manager import security_policy_manager

class KeyManager:
    """ Singleton za generiranje i dohvacanje kljuceva"""
    _instance = None
    _kek = None
    _master_key = None

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
    
    def clear_kek(self):
        if self._kek is not None:
            self._kek = b'\x00' * len(self._kek) # overwritea kljuc u memoriji, temp solution
        self._kek = None

    def generate_ecc_keypair(self) -> tuple[str, bytes]:
        """Generira ECC X25519 par ključeva"""
        from cryptography.hazmat.primitives.asymmetric import x25519
        
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        # Serialize za spremanje da ne vraćamo objekt od X25519PrivateKey klase
        private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
        )
        public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
        )
        
        return (public_key_bytes, private_key_bytes)

# Dio sa MK,PDK i enkripcijom/dekripcijom privatnog ključa
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

    def derive_pdk(self, master_key: bytes, pdk_salt: str) -> bytes:
        """Derivira PDK iz MK-a za enkripciju privatnog ključa"""
        hash_name = security_policy_manager.get_policy_param("pbkdf2_hash_name")
    
        return hashlib.pbkdf2_hmac(
            hash_name,
            master_key,
            pdk_salt.encode(),
            1
        )

    def derive_master_key(self, password: str, mk_salt: str) -> bytes:
        """Derivira Master Key iz lozinke"""
        iterations = security_policy_manager.get_policy_param("pbkdf2_iterations")
        hash_name = security_policy_manager.get_policy_param("pbkdf2_hash_name")

        return hashlib.pbkdf2_hmac(
            hash_name,
            password.encode(),
            mk_salt.encode(),
            iterations
        )
    def set_master_key(self, password: str, mk_salt: str):
        """Postavlja Master Key nakon uspješne prijave korisnika"""
        if self._master_key is not None:
            raise Exception("Master Key is already set.")
        
        self._master_key = self.derive_master_key(password, mk_salt)
    
    def get_master_key(self) -> bytes:
        """Dohvaća Master Key za deriviranje PDK-a"""
        if self._master_key is None:
            raise Exception("Master Key is not set.")
        return self._master_key
    
    def clear_master_key(self):
        """Briše Master Key pri odjavi korisnika"""
        if self._master_key is not None:
            self._master_key = b'\x00' * len(self._master_key)
        self._master_key = None
    
    def clear_session(self):
        """Briše sve session ključeve"""
        self.clear_kek()
        self.clear_master_key()

key_manager = KeyManager()