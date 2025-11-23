import sys
from PySide6.QtWidgets import QApplication
from src.models.db import db
from src.controllers.primjer_controller import PrimjerController

if __name__ == "__main__":
    db.init_db()

    app = QApplication(sys.argv)

    window = PrimjerController()
    window.show()

    sys.exit(app.exec())