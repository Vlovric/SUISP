from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QWidget

from src.controllers.base_controller import BaseController
from src.views.prijava_registracija.login_view import LoginView
from src.utils.log_manager import log
from src.utils.password_manager import PasswordManager
from src.models.user_model import UserModel

class LoginController(BaseController):
    # Signal koji se emitta kad je login successful
    proceed = Signal()
    failed_attempts: int = 0
    lockout_counter: int = 0

    def __init__(self):
        super().__init__()
        self.user_model = UserModel()

        self._view = LoginView()
        self._view.setWindowTitle("Login")
        self._view.resize(400, 200)

        self._view.login_button.clicked.connect(self._handle_login)

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self._update_countdown)
        self.remaining_seconds = 0

    @property
    def root_widget(self) -> QWidget:
        return self._view

    def _handle_login(self):
        username, password = self._view.get_credentials()

        fetched_user = self.user_model.get_user_by_username(username)
        if not fetched_user:
            self._view.set_error_message("Korisničko ime ne postoji!")
            return
        self._view.set_error_message("")
        try:
            if(self.failed_attempts >= 3):
                self.start_counter()
            else:
                if(PasswordManager.verify_user_credentials(fetched_user, password) == False):
                    self.failed_attempts += 1
                    log("Neuspješna prijava radi neispravne lozinke ili korisničkog imena.")
                    self._view.set_error_message("Neispravno korisničko ime ili lozinka.\n Broj preostalih pokušaja: {}.".format(4 - self.failed_attempts))
                    return
                else:
                    log("Korisnik uspješno prijavljen!")
                    self._view.set_error_message("")
                    self.proceed.emit()
                    return
        except Exception as e:
            log(f"Neuspješna prijava: {e}")
            self._view.set_error_message(f"Neuspješna prijava: {e}.")
            return

    def start_counter(self) -> None:
        self.lockout_counter += 1
        self.remaining_seconds = 60 * self.lockout_counter

        # Onemogući login button tokom odbrojavanja
        self._view.login_button.setEnabled(False)

        self.countdown_timer.start(1000)

        self._update_countdown()

    def _update_countdown(self) -> None:
        if self.remaining_seconds > 0:
            self._view.set_error_message(
                f"Previše neuspješnih pokušaja prijave.\n Pokušajte ponovno za {self.remaining_seconds} sekundi."
            )
            self.remaining_seconds -= 1
        else:
            self.countdown_timer.stop()
            self.failed_attempts = 0
            self._view.set_error_message("")
            self._view.login_button.setEnabled(True)