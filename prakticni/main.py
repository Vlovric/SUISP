import sys
from PySide6.QtWidgets import QApplication
from pathlib import Path
from src.controllers.app_controller import AppController
from src.controllers.login_controller import LoginController
from src.controllers.registration_controller import RegistrationController
from src.models.user_model import UserModel
from src.models.db import db
from src.utils.key_manager import key_manager
import os # TODO MAKNI

class App:
    def __init__(self):
        # TODO MAKNI
        try:
            os.remove("data/baza.db")
        except:
            print("")
        # KRAJ MAKNI

        self.app = QApplication(sys.argv)
        db.init_db()

        try:
            theme_path = Path(__file__).parent / "src" / "views" / "themes" / "dark_theme.qss"
            with open(theme_path, "r") as f:
                self.app.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Nema filea teme")
        ## provjera jesmo li se registirali prvi put
        if UserModel.has_user("user"):
            self.current_controller = LoginController()
            self.current_controller.proceed.connect(self._show_main_app)
            self.current_controller.root_widget.show()
        else:
            self.current_controller = RegistrationController()
            self.current_controller.proceed.connect(self._show_main_app)
            self.current_controller.root_widget.show()

    def _show_main_app(self):
        self.current_controller.root_widget.close()
        self.main_window = AppController()
        self.main_window.show()

    def run(self):
        exit_code = self.app.exec()
        key_manager.clear_kek()
        sys.exit(exit_code)

if __name__ == "__main__":
    app = App()
    app.run()

    