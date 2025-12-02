from datetime import datetime
from PySide6.QtWidgets import QWidget, QStackedWidget, QApplication
from src.controllers.base_controller import BaseController
from src.utils.log_manager import log_manager
from src.utils.file_manager import file_manager
from src.utils.rsa_helper import RsaHelper
from src.utils.aes_helper import AesHelper
from src.utils.key_manager import key_manager
import hashlib

from src.views.izvoz_loga.audit_log_export_view import AuditLogExportView

class AuditLogExportController(BaseController):
    def __init__(self):
        super().__init__()

        self._stack = QStackedWidget()
        self.input_view = AuditLogExportView()

        self._stack.addWidget(self.input_view)

        self.input_view.submit_btn.clicked.connect(self.handle_submit)
        self.input_view.copy_btn.clicked.connect(self.copy_public_key)
        self.input_view.copy_btn.hide()

    @property
    def root_widget(self) -> QWidget:
        return self._stack
    
    def reset(self):
        self.input_view.input_field.clear()
        self._stack.setCurrentIndex(0)

    def handle_submit(self):
        self.input_view.error_label.setText("")
        self.input_view.success_label.setText("")
        self.input_view.copy_btn.hide()

        public_key = self.input_view.input_field.toPlainText()

        if (len(public_key) == 0):
            self.input_view.error_label.setText("Ključ nije unesen!")
            return
        
        log_text, error = log_manager.get_logs()
        if error:
            self.input_view.error_label.setText(error)
            return

        now = datetime.now().isoformat()
        filename = f"audit_log_{datetime.fromisoformat(now).strftime('%Y-%m-%d_%H-%M-%S')}.bin"

        aes_key = AesHelper.generate_key()

        aes_error = self.encrypt_and_save(log_text, aes_key, filename)

        if aes_error:
            self.input_view.error_label.setText(aes_error)
            return

        key_filename = f"audit_log_key_{datetime.fromisoformat(now).strftime('%Y-%m-%d_%H-%M-%S')}.bin"
        rsa_error = self.save_key(aes_key, public_key, key_filename)

        if rsa_error:
            self.input_view.error_label.setText(rsa_error)
            return

        signature_filename = f"audit_log_signature_{datetime.fromisoformat(now).strftime('%Y-%m-%d_%H-%M-%S')}.sig"
        digital_signature_error = self.digital_signature(log_text, signature_filename)

        if digital_signature_error:
            self.input_view.error_label.setText(digital_signature_error)
            return
        
        self.input_view.success_label.setText("Audit log zapisi su uspješno izvezeni! Javni ključ za provjeru digitalnog potpisa možete kopirati klikom na gumb.")
        self.input_view.copy_btn.show()

    def encrypt_and_save(self, log_text: str, key: str, filename: str) -> str | None:
        encrypted_bytes, encryption_error = AesHelper.encrypt(log_text, key)

        if encryption_error:
            return encryption_error

        if not file_manager.open_file_download_dialog(self, "Spremi datoteku", filename, encrypted_bytes):
            self.input_view.error_label.setText("Nije moguće spremiti datoteku s izvozom.")

        return None
    
    def save_key(self, key: str, public_key: str, filename: str) -> str | None:
        encrypted_bytes, encryption_error = RsaHelper.encrypt(key, public_key)

        if encryption_error:
            return encryption_error
        
        if not file_manager.open_file_download_dialog(self, "Spremi kriptirani ključ", filename, encrypted_bytes):
            self.input_view.error_label.setText("Nije moguće spremiti kriptirani ključ.")

        return None
    
    def digital_signature(self, log_text: str, filename: str) -> str | None:
        private_key = key_manager.get_private_key()

        signature = RsaHelper.sign(log_text, private_key)

        if not file_manager.open_file_download_dialog(self, "Spremi digitalni potpis", filename, signature):
            self.input_view.error_label.setText("Nije moguće spremiti digitalni potpis.")

        return None
    
    def copy_public_key(self):
        public_key = key_manager.get_public_key()
        QApplication.clipboard().setText(public_key)

    
        
        

