from email.mime import message
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        self.login_button = QPushButton("Login")

        layout = QVBoxLayout()
        layout.addWidget(self.login_button)
        self.setLayout(layout)




"""
AI slop primjer cisto za neke dobre prakse ko error messages i funkcije za dohvacanje inputa

class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        # --- Create UI Elements ---
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password) # Hides password text

        self.login_button = QPushButton("Login")
        
        self.error_label = QLabel("") # To show login errors
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Create Layout ---
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter Your Credentials"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def get_credentials(self) -> tuple[str, str]:
        return (self.username_input.text(), self.password_input.text())

    def set_error_message(self, message: str):
        self.error_label.setText(message)
"""