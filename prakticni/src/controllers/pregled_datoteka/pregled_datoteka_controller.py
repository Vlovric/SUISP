from PySide6.QtWidgets import QWidget, QStackedWidget
from src.models.datoteka.datoteka_model import DatotekaModel
from src.controllers.base_controller import BaseController
from src.views.pregled_datoteka.pregled_datoteka_view import PregledDatotekaView
from functools import partial
from src.utils.file_manager import file_manager
from src.utils.key_manager import key_manager

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

    # Učitava datoteke iz baze (pozivati npr. kod dodavanja nove ili brisanja kako bi se osvježio popis)
    def load_files(self):
        files = DatotekaModel.fetch_all()
        self.view.set_files(files)
        self.connect_buttons()

    # Povezuje sve gumbove sa handlerima
    def connect_buttons(self):
        for export_btn in self.view.export_buttons:
            btn, file_id = export_btn
            btn.clicked.connect(partial(self.handle_export, file_id))

        for delete_btn in self.view.delete_buttons:
            btn, file_id = delete_btn
            btn.clicked.connect(partial(self.handle_delete, file_id))

        for share_btn in self.view.share_buttons:
            btn, file_id = share_btn
            btn.clicked.connect(partial(self.handle_share, file_id))
    
    def handle_new_file(self):
        file = file_manager.select_file_dialog(self)
        if file == None:
            return
        
        kek = key_manager.get_private_key()

        # TODO generiraj DEK

        # TODO generiraj random naziv za datoteku

        # TODO kriptiraj datoteku

        # TODO spremi datoteku

        # TODO dodaj zapis u bazu

        self.reset()

    def handle_export(self, id):
        # TODO implementirati
        print(f"Export zapisa s {id} se handlea!")
        self.reset()

    def handle_delete(self, id):
        # TODO implementirati
        print(f"Brisanje zapisa s {id} se handlea!")
        self.reset()

    def handle_share(self, id):
        # TODO implementirati
        print(f"Dijeljenje zapisa s {id} se handlea!")
        self.reset()