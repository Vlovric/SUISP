import sys
from PySide6.QtWidgets import QApplication
from src.controllers.app_controller import AppController
from src.controllers.login_controller import LoginController
from src.models.db import db

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        db.init_db()

        self.login_controller = LoginController()
        self.login_controller.proceed.connect(self._show_main_app)
        self.login_controller.root_widget.show()

    def _show_main_app(self):
        self.login_controller.root_widget.close()
        self.main_window = AppController()
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = App()
    app.run()

    