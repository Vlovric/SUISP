from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
from src.utils.path_manager import path_manager

class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Korisničko ime")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Lozinka")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.toggle_password_action = QAction(self)
        icon_path = str(path_manager.get_resource_path("src/pic/view_dark.svg"))
        self.toggle_password_action.setIcon(QIcon(icon_path))
        self.toggle_password_action.triggered.connect(self.toggle_password_visibility)
        self.password_input.addAction(self.toggle_password_action, QLineEdit.ActionPosition.TrailingPosition)

        self.login_button = QPushButton("Prijavi se")
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)
        self.setLayout(layout)

    def get_credentials(self) -> tuple[str, str]:
        return (self.username_input.text(), self.password_input.text())

    def set_error_message(self, message: str):
        self.error_label.setText(message)

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_action.setIcon(QIcon("src/pic/hide_dark.svg"))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_action.setIcon(QIcon("src/pic/view_dark.svg"))

    def center(self):
        frame_gm = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frame_gm.moveCenter(screen)
        self.move(frame_gm.topLeft())