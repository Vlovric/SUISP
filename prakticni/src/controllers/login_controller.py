from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from src.controllers.base_controller import BaseController
from src.views.prijava_registracija.login_view import LoginView

class LoginController(BaseController):
    # Signal koji se emitta kad je login successful
    proceed = Signal()

    def __init__(self):
        super().__init__()

        self._view = LoginView()
        self._view.setWindowTitle("Login")
        self._view.resize(400, 200)

        self._view.login_button.clicked.connect(self._handle_login)
    
    @property
    def root_widget(self) -> QWidget:
        return self._view
    
    def _handle_login(self):
        self.proceed.emit()