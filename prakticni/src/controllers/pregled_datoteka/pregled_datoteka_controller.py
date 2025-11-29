from PySide6.QtWidgets import QWidget, QStackedWidget
from src.models.datoteka.datoteka_model import DatotekaModel
from src.controllers.base_controller import BaseController
from src.views.pregled_datoteka.pregled_datoteka_view import PregledDatotekaView

class PregledDatotekaController(BaseController):
    def __init__(self):
        super().__init__()

        self._stack = QStackedWidget()
        self.view = PregledDatotekaView()
        self._stack.addWidget(self.view)

        self.load_files()

        self.view.import_btn.clicked.connect(self.handle_new_file)

    @property
    def root_widget(self) -> QWidget:
        return self._stack
    
    def reset(self):
        self.load_files()
        self._stack.setCurrentIndex(0)

    def load_files(self):
        files = DatotekaModel.fetch_all()
        self.view.set_files(files)
    
    def handle_new_file(self):
        # TODO implementirati
        print("Novi file se handlea!")

    def handle_export(self, id):
        # TODO implementirati
        print(f"Export {id} se handlea!")

    def handle_delete(self, id):
        # TODO implementirati
        print(f"Brisanje {id} se handlea!")

    def handle_share(self, id):
        # TODO implementirati
        print(f"Dijeljenje {id} se handlea!")