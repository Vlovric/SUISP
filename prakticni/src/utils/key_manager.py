from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

from src.utils.security_policy_manager import security_policy_manager

class KeyManager:
    """ Singleton za generiranje i dohvacanje KEK-a"""
    _instance = None
    _kek = None

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

key_manager = KeyManager()