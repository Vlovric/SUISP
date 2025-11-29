import os
import binascii
import hashlib
from src.utils.key_manager import key_manager
from src.utils.security_policy_manager import security_policy_manager
import math

class PasswordManager:

    @staticmethod
    def generate_salt() -> str:
        return binascii.hexlify(os.urandom(security_policy_manager.get_policy_param("pbkdf2_salt_length"))).decode()

    @staticmethod
    def calculate_password_entropy(password: str) -> float:
        """
        Računa entropiju lozinke u bitovima.
        
        Entropija = log₂(pool_size^password_length) = password_length * log₂(pool_size)
        """
        if not password:
            return 0.0
        
        pool_size = 0
        
        if any(char.islower() for char in password):
            pool_size += 26
        if any(char.isupper() for char in password):
            pool_size += 26
        if any(char.isdigit() for char in password):
            pool_size += 10
        if any(char in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for char in password):
            pool_size += 32
        
        if pool_size == 0:
            return 0.0
        
        entropy = len(password) * math.log2(pool_size)
        return entropy

    @staticmethod
    ## Mora biti minimalno jedan broj, jedno veliko slovo, jedno malo slovo i posedni znak
    def validate_password_strength(password: str) -> str:
        if len(password) < security_policy_manager.get_policy_param("password_length_min"):
            return "Lozinka mora imati najmanje {} znakova.".format(
                security_policy_manager.get_policy_param("password_length_min")
            )
        if not any(char.isdigit() for char in password):
            return "Lozinka mora sadržavati barem jedan broj."
        if not any(char.isupper() for char in password):
            return "Lozinka mora sadržavati barem jedno veliko slovo."
        if not any(char.islower() for char in password):
            return "Lozinka mora sadržavati barem jedno malo slovo."
        if not any(char in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for char in password):
            return "Lozinka mora sadržavati barem jedan poseban znak."
        
        # Provjera entropije (trebam li ovo eksli????)
        entropy = PasswordManager.calculate_password_entropy(password)
        min_entropy = security_policy_manager.get_policy_param("password_entropy_min_bits")
        if entropy < min_entropy:
            return "Lozinka je preslaba. Entropija: {:.1f} bita (minimum: {} bita). Koristite dulju lozinku ili više različitih znakova.".format(
                entropy, min_entropy
            )
        
        return "sucessful_validation"


    @staticmethod
    def hash_password(mk: bytes, password_salt: str) -> str:
        hash_name = security_policy_manager.get_policy_param("pbkdf2_hash_name")

        # Hash lozinke za autentifikaciju, hashiramo sa saltom od MK-a
        password_hash = hashlib.pbkdf2_hmac(
            hash_name,
            mk.encode('utf-8'),
            password_salt.encode('utf-8'),
            1
        )

        return password_hash.hex()
    @staticmethod
    def verify_password(stored_password_hash: str, provided_password: str) -> bool:
        # implemetacija za login funkcionalnost
            return False