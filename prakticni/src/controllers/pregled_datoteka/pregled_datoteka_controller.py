from PySide6.QtWidgets import QWidget, QStackedWidget
from src.controllers.base_controller import BaseController
from src.views.pregled_datoteka.pregled_datoteka_view import PregledDatotekaView

class PregledDatotekaController(BaseController):
    def __init__(self):
        super().__init__()

        self._stack = QStackedWidget()
        self.view = PregledDatotekaView()

        self._stack.addWidget(self.view)

        # self.view.import_btn.clicked.connect(self.handle_new_file)

    @property
    def root_widget(self) -> QWidget:
        return self._stack
    
    def reset(self):
        self._stack.setCurrentIndex(0)
    
    def handle_new_file(self):
        # TODO implementirati
        print("Novi file se handlea!")