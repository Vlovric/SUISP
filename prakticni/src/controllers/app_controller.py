from PySide6.QtWidgets import QMainWindow, QStackedWidget, QToolBar
from PySide6.QtGui import QAction

from functools import partial
from src.controllers.primjer.primjer_controller import PrimjerController

class AppController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure File Vault")
        self.resize(800, 600)

        # Kreiramo toolbar za navigaciju
        nav_bar = QToolBar("Navigation")
        nav_bar.setMovable(False)
        self.addToolBar(nav_bar)

        # Kreiramo stack widget za content ekrana
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.controllers = {}

        # OVAKO registriramo nove kontrolere za svaki feature koji zelimo na navigaciji na main menu
        self._register_controller("primjer", PrimjerController())
        primjer_action = QAction("Primjer", self)
        primjer_action.triggered.connect(partial(self._show_controller, "primjer"))
        nav_bar.addAction(primjer_action)

        # Palimo prvi controller tj. inicijalni ekran
        self._show_controller("primjer")

    def _register_controller(self, name: str, controller):
        self.controllers[name] = controller
        self.stack.addWidget(controller.root_widget)

    def _show_controller(self, name: str):
        ctrl = self.controllers.get(name)
        if not ctrl:
            return
        
        ctrl.reset()

        index = self.stack.indexOf(ctrl.root_widget)
        if index != -1:
            self.stack.setCurrentIndex(index)