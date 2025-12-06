from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QWidget

from src.controllers.base_controller import BaseController
from src.views.prijava_registracija.login_view import LoginView
from src.utils.log_manager import log
from src.utils.password_manager import PasswordManager
from src.models.user_model import UserModel

class LoginController(BaseController):
    proceed = Signal()
    failed_attempts: int = 0
    lockout_counter: int = 0

    def __init__(self):
        super().__init__()
        self.user_model = UserModel()

        self._view = LoginView()
        self._view.setWindowTitle("Prijava")
        self._view.resize(400, 200)
        self._view.center()

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
            self._view.set_error_message("Neispravno korisničko ime ili lozinka!")
            return
        is_locked, remaining = self.user_model.is_locked_out(username)
        if is_locked:
            self.remaining_seconds = remaining
            self.lockout_counter = fetched_user.get('lockout_count', 0)
            self._view.login_button.setEnabled(False)
            self.countdown_timer.start(1000)
            self._update_countdown()
            return
        try:
            if PasswordManager.verify_user_credentials(fetched_user, password):
                self.user_model.update_login_attempt(username, success=True)
                log("Korisnik uspješno prijavljen!")
                self._view.set_error_message("")
                self.proceed.emit()
            else:
                self.user_model.update_login_attempt(username, success=False)
                log("Neispravno korisničko ime ili lozinka.")
                fetched_user = self.user_model.get_user_by_username(username)
                failed = fetched_user.get('failed_attempts', 0)
                
                if failed >= 3:
                    lockout_count = fetched_user.get('lockout_count', 0) + 1
                    wait_seconds = 60 * lockout_count
                    self.user_model.set_lockout(username, wait_seconds)
                    self.lockout_counter = lockout_count
                    self.start_counter()
                else:
                    self._view.set_error_message(
                        f"Neispravno korisničko ime ili lozinka. Broj preostalih pokušaja: {3 - failed}."
                    )
        except Exception as e:
            log(f"Neuspješna prijava: {e}")
            self._view.set_error_message(f"Neuspješna prijava: {e}.")
            return

    def start_counter(self) -> None:
        self.lockout_counter += 1
        self.remaining_seconds = 60 * self.lockout_counter

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