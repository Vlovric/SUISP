from src.controllers.base_controller import BaseController
from src.views.zakljucavanje_datoteke.unlocked_files_view import UnlockedFilesView
from src.models.datoteka.datoteka_model import DatotekaModel

from PyQt5.QtWidgets import QStackedWidget, QWidget
from functools import partial

class UnlockedFilesController(BaseController):
    def __init__(self):
        super().__init__()

        self._stack = QStackedWidget()
        self.view = UnlockedFilesView()
        self._stack.addWidget(self.view)

        self.load_files()

    @property
    def root_widget(self) -> QWidget:
        return self._stack
    
    def reset(self):
        self.load_files()
        self._stack.setCurrentIndex(0)
    
    def load_files(self):
        files = DatotekaModel.fetch_all_unlocked()
        self.view.set_files(files)
        self.connect_buttons()
    
    def connect_buttons(self):
        for lock_btn in self.view.lock_buttons:
            btn, file_id = lock_btn
            btn.clicked.connect(partial(self.handle_lock, file_id))

    def handle_lock(self, file_id):
        return
    