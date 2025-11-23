import sys
from PySide6.QtWidgets import QApplication
from src.controllers.app_controller import AppController
from src.models.db import db


if __name__ == "__main__":
    db.init_db()

    app = QApplication(sys.argv)
    win = AppController()
    win.show()
    sys.exit(app.exec())

    