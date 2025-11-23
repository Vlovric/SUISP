from PySide6.QtWidgets import QMainWindow, QStackedWidget

from src.controllers.primjer.primjer_controller import PrimjerController

class AppController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure File Vault")
        self.resize(600, 400)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Registriramo individualne controllere
        self.controllers = {}
        self._register_controller("primjer", PrimjerController())

        # Palimo prvi controller tj. inicijalni ekran
        self.show_controller("primjer")

    def _register_controller(self, name: str, controller):
        self.controllers[name] = controller
        self.stack.addWidget(controller.root_widget)

    def show_controller(self, name: str):
        ctrl = self.controllers.get(name)
        if not ctrl:
            return
        index = self.stack.indexOf(ctrl.root_widget)
        if index != -1:
            self.stack.setCurrentIndex(index)