from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from src.controllers.base_controller import BaseController
from src.views.prijava_registracija.registration_view import RegistrationView
from src.utils.password_manager import PasswordManager
from src.models.user_model import UserModel

class RegistrationController(BaseController):
    # Signal koji se emitta kad je login successful
    proceed = Signal()

    def __init__(self):
        super().__init__()
        self.user_model = UserModel()

        self._view = RegistrationView()
        self._view.setWindowTitle("Registration")
        self._view.resize(400, 200)

        self._view.register_button.clicked.connect(self._handle_registration)
    
    @property
    def root_widget(self) -> QWidget:
        return self._view
    
    def _handle_registration(self):
            username, password = self._view.get_credentials()
            self._view.set_error_message("")

            if not username or not password:
                self._view.set_error_message("Username and password are required!")
                return

            jeValidna = PasswordManager.validate_password_strength(password)
            if jeValidna != "sucessful_validation":
                self._view.set_error_message(jeValidna)  # Prikaži specifičnu grešku
                return

            try:
                salt = PasswordManager.generate_salt()
                password_hash = PasswordManager.hash_password(password, salt)
                success = self.user_model.register_user(username, password_hash, salt)
                
                if success:
                    self._view.set_error_message("")
                    self.proceed.emit()
                else:
                    self._view.set_error_message("Registration failed!")
            except Exception as e:
                self._view.set_error_message(str(e))