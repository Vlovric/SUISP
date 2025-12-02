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
        # brojevi poola se izvlače iz security policy-a
        if any(char.islower() for char in password):
            pool_size += security_policy_manager.get_policy_param("password_char_pools")["lowercase"]
        if any(char.isupper() for char in password):
            pool_size += security_policy_manager.get_policy_param("password_char_pools")["uppercase"]
        if any(char.isdigit() for char in password):
            pool_size += security_policy_manager.get_policy_param("password_char_pools")["digits"]
        if any(char in security_policy_manager.get_policy_param("password_specilal_characters") for char in password):
            pool_size += security_policy_manager.get_policy_param("password_char_pools")["special"]
        
        if pool_size == 0:
            return 0.0
        
        entropy = len(password) * math.log2(pool_size)
        return entropy

    @staticmethod
    def validate_password_strength(password: str) -> str:
        """
        Validira jačinu lozinke prema pravilima iz security policy-a.
        Vraća poruku o greški ili 'sucessful_validation' ako je lozinka valjana.
        """
        min_length = security_policy_manager.get_policy_param("password_length_min")
        if len(password) < min_length:
            return "Lozinka mora imati najmanje {} znakova.".format(min_length)
        # Kako sam dodala nove parametre u policy, određene provjere se mogu "izgasiti" ako se stavi false u policy-u
        if security_policy_manager.get_policy_param("pasword_require_digits"):
            if not any(char.isdigit() for char in password):
                return "Lozinka mora sadržavati barem jedan broj."
        
        if security_policy_manager.get_policy_param("password_require_uppercase"):
            if not any(char.isupper() for char in password):
                return "Lozinka mora sadržavati barem jedno veliko slovo."
        
        if security_policy_manager.get_policy_param("password_require_lowercase"):
            if not any(char.islower() for char in password):
                return "Lozinka mora sadržavati barem jedno malo slovo."
        
        if security_policy_manager.get_policy_param("password_require_special_char"):
            special_chars = security_policy_manager.get_policy_param("password_specilal_characters")
            if not any(char in special_chars for char in password):
                return "Lozinka mora sadržavati barem jedan poseban znak ({}).".format(special_chars)
        
        entropy = PasswordManager.calculate_password_entropy(password)
        min_entropy = security_policy_manager.get_policy_param("password_entropy_min_bits")
        if entropy < min_entropy:
            return "Lozinka je preslaba. Entropija: {:.1f} bita (minimum: {} bita). Koristite dulju lozinku ili više različitih znakova.".format(
                entropy, min_entropy
            )
        
        return "sucessful_validation"


    @staticmethod
    def hash_password(mk: bytes, password_salt: str) -> str:
        iterations = security_policy_manager.get_policy_param("pbkdf2_iterations")
        hash_name = security_policy_manager.get_policy_param("pbkdf2_hash_name")

        # Hash lozinke za autentifikaciju, hashiramo sa saltom od MK-a
        password_hash = hashlib.pbkdf2_hmac(
            hash_name,
            mk,
            password_salt.encode('utf-8'),
            iterations
        )

        return password_hash.hex()
    @staticmethod
    def verify_user_credentials(fetched_user: dict, provided_password: str) -> bool:
        mk_generated = key_manager.generate_master_key(provided_password, fetched_user["mk_salt"])
        hashed_provided_password = PasswordManager.hash_password(mk_generated, provided_password)
        if hashed_provided_password == fetched_user["master_password_hash"]:
            if key_manager._pdk is None:
                key_manager.set_pdk(mk_generated, fetched_user["pdk_salt"])
            return True
        return False