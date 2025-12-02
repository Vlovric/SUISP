from src.controllers.base_controller import BaseController
from src.views.zakljucavanje_datoteke.unlocked_files_view import UnlockedFilesView
from src.models.datoteka.datoteka_model import DatotekaModel
from src.utils.file_manager import file_manager

from PySide6.QtWidgets import QStackedWidget, QWidget
from functools import partial
import hashlib

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
        file = DatotekaModel.fetch_by_id(file_id)
        if not file:
            self.view.error_label.setText("Datoteka nije pronađena u bazi.")
            return
        
        file_content = file_manager.read_file(file["path"])
        if file_content is None:
            self.view.error_label.setText("Pogreška pri čitanju datoteke.")
            return
        
        # if file["binary"]:
        #     file_hash = hashlib.sha512(file_content).hexdigest()
        # else:
        #     file_hash = hashlib.sha512(file_content.encode()).hexdigest()

        # moram ko david napravit proces al overwriteat postojecu kriptiranu datoteku
        

        return
    