from datetime import datetime
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QStackedWidget
from src.controllers.base_controller import BaseController
from src.utils.log_manager import log_manager
from src.utils.file_manager import file_manager
from src.utils.rsa_helper import RsaHelper

from src.views.izvoz_loga.audit_log_export_view import AuditLogExportView

class AuditLogExportController(BaseController):
    def __init__(self):
        super().__init__()

        self._stack = QStackedWidget()
        self.input_view = AuditLogExportView()

        self._stack.addWidget(self.input_view)

        self.input_view.submit_btn.clicked.connect(self.handle_submit)

    @property
    def root_widget(self) -> QWidget:
        return self._stack
    
    def reset(self):
        self.input_view.input_field.clear()
        self._stack.setCurrentIndex(0)

    def handle_submit(self):
        self.input_view.error_label.setText("")

        public_key = self.input_view.input_field.toPlainText()
        print(public_key)

        if (len(public_key) == 0):
            self.input_view.error_label.setText("Ključ nije unesen!")
            return
        
        log_text, error = log_manager.get_logs()
        if error:
            self.input_view.error_label.setText(error)

        encrypted_bytes, encryption_error = RsaHelper.encrypt(log_text, public_key)

        if encryption_error:
            self.input_view.error_label.setText(encryption_error)
            return

        now = datetime.now().isoformat()
        filename = f"audit_log_{datetime.fromisoformat(now).strftime('%Y-%m-%d_%H-%M-%S')}.bin"

        if not file_manager.open_file_download_dialog(self, "Izvezi", filename, encrypted_bytes):
            self.input_view.error_label.setText("Nije moguće spremiti datoteku s izvozom.")

    
        
        

