from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PySide6.QtCore import Qt

class RegistrationView(QWidget):
    def __init__(self): 
        super().__init__()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.register_button = QPushButton("Register")

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.error_label)  
        self.setLayout(layout)
    
    def get_credentials(self) -> tuple[str, str]:
        return (self.username_input.text(), self.password_input.text())

    def set_error_message(self, message: str):
        self.error_label.setText(message)