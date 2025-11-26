import os
import binascii
from src.utils.security_policy_manager import security_policy_manager
import hashlib

class PasswordManager:

    @staticmethod
    def generate_salt() -> str:
        return binascii.hexlify(os.urandom(security_policy_manager.get_policy_param("pbkdf2_salt_length"))).decode()

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
        return "sucessful_validation"


    @staticmethod
    def hash_password(password: str, salt: str = None) -> str:
        if salt is None:
            salt = PasswordManager.generate_salt()
        
        iterations = security_policy_manager.get_policy_param("pbkdf2_iterations")
        hash_name = security_policy_manager.get_policy_param("pbkdf2_hash_name")

        password_hash = hashlib.pbkdf2_hmac(
            hash_name,
            password.encode(),
            salt.encode(),
            iterations
        )
        return f"{salt}${password_hash.hex()}"

    @staticmethod
    def verify_password(stored_password_hash: str, provided_password: str) -> bool:
        return stored_password_hash == PasswordManager.hash_password(provided_password)