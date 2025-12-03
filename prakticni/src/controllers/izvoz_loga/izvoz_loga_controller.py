from datetime import datetime
import io
import zipfile
from PySide6.QtWidgets import QWidget, QStackedWidget, QApplication
from src.controllers.base_controller import BaseController
from src.utils.log_manager import log, log_manager
from src.utils.file_manager import file_manager
from src.utils.rsa_helper import RsaHelper
from src.utils.aes_helper import AesHelper
from src.utils.key_manager import key_manager

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
        self.input_view.error_label.setText("")
        self.input_view.success_label.setText("")
        self.input_view.copy_btn.hide()
        self._stack.setCurrentIndex(0)

    def handle_submit(self):
        self.input_view.error_label.setText("")
        self.input_view.success_label.setText("")
        self.input_view.copy_btn.hide()

        public_key = self.input_view.input_field.toPlainText()

        if (len(public_key) == 0):
            self.input_view.error_label.setText("Ključ nije unesen!")
            return
        
        log("Korisnik je pokrenuo izvoz audit log zapisa.")
        
        log_text, error = log_manager.get_logs()
        if error:
            self.input_view.error_label.setText(error)
            return

        aes_key = AesHelper.generate_key()

        log_bytes, aes_error = AesHelper.encrypt(log_text, aes_key)

        if aes_error:
            self.input_view.error_label.setText(aes_error)
            return

        key_bytes, rsa_error = RsaHelper.encrypt(aes_key, public_key)

        if rsa_error:
            self.input_view.error_label.setText(rsa_error)
            return

        private_key = key_manager.get_private_key()
        signature_bytes = RsaHelper.sign(log_text, private_key)

        now = datetime.now().isoformat()
        filename = f"audit_log_{datetime.fromisoformat(now).strftime('%Y-%m-%d_%H-%M-%S')}.alogpkg"

        zip_bytes = self.build_export_package(log_bytes, key_bytes, signature_bytes)

        if not file_manager.open_file_download_dialog(self, "Spremi izvezen audit log.", filename, zip_bytes, "Audit Log Package (*.alogpkg)"):
            self.input_view.error_label.setText("Nije moguće spremiti audit log.")
        
        self.input_view.success_label.setText("Audit log zapisi su uspješno izvezeni! Javni ključ za provjeru digitalnog potpisa možete kopirati klikom na gumb.")
        self.input_view.copy_btn.show()

    def build_export_package(self, log_bytes: bytes, key_bytes: bytes, signature_bytes: bytes) -> bytes:
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("encrypted_log.bin", log_bytes)
            zip_file.writestr("encrypted_key.bin", key_bytes)
            zip_file.writestr("signature.sig", signature_bytes)
        
        return buffer.getvalue()
    
    def copy_public_key(self):
        public_key = key_manager.get_public_key()
        QApplication.clipboard().setText(public_key)
    
        
        

