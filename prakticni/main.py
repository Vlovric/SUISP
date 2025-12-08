import sys
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import PySide6.QtSvg
from src.controllers.app_controller import AppController
from src.controllers.login_controller import LoginController
from src.controllers.registration_controller import RegistrationController
from src.models.user_model import UserModel
from src.models.db import db
from src.utils.key_manager import key_manager
from src.utils.single_application import SingleApplication
from src.utils.path_manager import path_manager

APP_ID = "secure.file.vault.app.suisp"

class App:
    def __init__(self):
        self.app = SingleApplication(sys.argv, APP_ID)
        if getattr(self.app, "is_running", False):
            print("Aplikacija je već pokrenuta!")
            sys.exit(0)

        db.init_db()

        try:
            icon_path = path_manager.get_resource_path("src/pic/app_icon.png")
            self.app.setWindowIcon(QIcon(str(icon_path)))
        except Exception as e:
            print(f"Ne mogu postaviti ikonu aplikacije: {e}")

        try:
            theme_path = path_manager.get_resource_path("src/views/themes/dark_theme.qss")
            with open(theme_path, "r") as f:
                self.app.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Nema datoteke teme")

        self.app.activateRequested.connect(self._activate_top_window)    
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
        self.main_window.logout_requested.connect(self._show_login_after_logout)
        self.main_window.show()
    
    def _show_login_after_logout(self):
        if hasattr(self, 'main_window'):
            self.main_window.close()
        self.current_controller = LoginController()
        self.current_controller.proceed.connect(self._show_main_app)
        self.current_controller.root_widget.show()

    def run(self):
        exit_code = self.app.exec()
        key_manager.clear_kek()
        sys.exit(exit_code)

    def _activate_top_window(self):
        win = getattr(self, "main_window", None)
        if win is None and hasattr(self, "current_controller"):
            win = self.current_controller.root_widget
        if not win:
            return
        if win.isMinimized():
            win.setWindowState(win.windowState() & ~Qt.WindowMinimized)
            win.showNormal()
        win.show()
        win.raise_()
        win.activateWindow()

if __name__ == "__main__":
    app = App()
    app.run()

    