from src.controllers.base_controller import BaseController
from src.utils.key_rotation_helper import KeyRotationHelper
from src.models.datoteka.datoteka_model import DatotekaModel
from src.views.key_rotation_dialog import KeyRotationDialog
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtWidgets import QMessageBox

class KeyRotationWorker(QObject):
    progress = Signal(int, int)
    finished = Signal(bool, str)

    def run(self):
        def cb(current, total):
            self.progress.emit(current, total)
        success, error = KeyRotationHelper.rotate_keys(progress_callback=cb)
        self.finished.emit(success, error or "")

class KeyRotationController(BaseController):
    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        self.dialog = None
        self.thread = None
        self.worker = None

    def start_key_rotation(self):
        total_files = DatotekaModel.get_file_count()
        
        self.dialog = KeyRotationDialog(total_files, parent=self.parent)

        self.thread = QThread(self.parent)
        self.worker = KeyRotationWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.dialog.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.dialog.show()
        self.thread.start()

    def on_finished(self, success: bool, error_message: str):
        if self.dialog is not None:
            self.dialog.close()
            self.dialog = None
        if success:
            QMessageBox.information(self.parent, "Rotacija ključeva", "Rotacija ključeva je uspješno dovršena.")
        else:
            QMessageBox.critical(self.parent, "Rotacija ključeva", f"Došlo je do pogreške tijekom rotacije ključeva: {error_message}")
