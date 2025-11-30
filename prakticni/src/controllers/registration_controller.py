from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from src.utils.key_manager import key_manager
from src.controllers.base_controller import BaseController
from src.views.prijava_registracija.registration_view import RegistrationView
from src.utils.log_manager import log
from src.utils.password_manager import PasswordManager
from src.models.user_model import UserModel

class RegistrationController(BaseController):
    # Signal koji se emitta kad je login successful
    proceed = Signal()

    def __init__(self):
        super().__init__()

        self._view = RegistrationView()
        self._view.setWindowTitle("Registracija korisnika")
        self._view.resize(400, 200)

        self._view.register_button.clicked.connect(self._handle_registration)
    
    @property
    def root_widget(self) -> QWidget:
        return self._view
    
    def _handle_registration(self):
            username, password = self._view.get_credentials()
            mk_salt = PasswordManager.generate_salt()
            pdk_salt = PasswordManager.generate_salt()
            self._view.set_error_message("")

            if not username or not password:
                self._view.set_error_message("Username and password are required!")
                return

            jeValidna = PasswordManager.validate_password_strength(password)
            if jeValidna != "sucessful_validation":
                self._view.set_error_message(jeValidna)  # Prikaži specifičnu grešku
                return

            try:
                master_key = key_manager.generate_master_key(password, mk_salt)
                key_manager.set_pdk(master_key, pdk_salt)
                pdk = key_manager.get_pdk()
                master_password_hash = PasswordManager.hash_password(master_key, password)
                
                public_key, private_key = key_manager.generate_rsa_keypair()
                private_key_encrypted = key_manager.encrypt_private_key(private_key, pdk)
                success = UserModel.register_user(username, master_password_hash, mk_salt, pdk_salt, public_key, private_key_encrypted)
                
                if success:
                    log("Korisnik uspješno registriran.")
                    self._view.set_error_message("")
                    self.proceed.emit()
                else:
                    log("Registracija korisnika nije uspjela.")
                    self._view.set_error_message("Registracija korisnika nije uspjela.")
            except Exception as e:
                self._view.set_error_message(str(e))

    