import io
import zipfile
from PySide6.QtWidgets import QWidget, QStackedWidget, QApplication
from src.views.izvoz_loga.audit_logs_result_view import AuditLogsResultView
from src.utils.rsa_helper import RsaHelper
from src.utils.aes_helper import AesHelper
from src.views.izvoz_loga.audit_logs_view import AuditLogsView
from src.controllers.base_controller import BaseController
from src.utils.key_manager import key_manager
from src.utils.file_manager import file_manager

class AuditLogsController(BaseController):
    def __init__(self):
        super().__init__()

        self._stack = QStackedWidget()
        self.view = AuditLogsView()
        self.result_view = AuditLogsResultView()

        self._stack.addWidget(self.view)
        self._stack.addWidget(self.result_view)

        # Novi, auditorov par ključeva kojim se kriptiraju audit logovi
        public_key_bytes, private_key_bytes = key_manager.generate_rsa_keypair()
        self.public_key = public_key_bytes.decode("utf-8")
        self.private_key = private_key_bytes.decode("utf-8")

        self.view.copy_public_key_btn.clicked.connect(self.copy_public_key)
        self.view.load_files_btn.clicked.connect(self.load_files)
        self.result_view.back_btn.clicked.connect(self.go_back)

    @property
    def root_widget(self) -> QWidget:
        return self._stack
    
    def reset(self):
        self.view.error_label.setText("")
        self.view.success_label.setText("")
        self.view.public_key_field.clear()
        self._stack.setCurrentIndex(0)
    
    def go_back(self):
        self.reset()

    def load_files(self):
        self.view.error_label.setText("")
        self.view.success_label.setText("")

        # Provjeri je li unesen privatni ključ
        user_private_key = self.view.public_key_field.toPlainText()

        if (len(user_private_key) == 0):
            self.view.error_label.setText("Javni ključ osobe nije unesen!")
            return
        
        # Učitava zip file i čita iz njega ostale datoteke
        package_file = file_manager.select_file_dialog(self, "Otvori audit paket.", "Audit paket (*.alogpkg)")

        if package_file is None:
            self.view.error_label.setText("Nije moguće otvoriti datoteku.")
            return
        
        if not package_file.successful:
            self.view.error_label.setText("Nije moguće otvoriti datoteku.")
            return
        
        if not package_file.filename.endswith(".alogpkg") or not package_file.is_binary:
            self.view.error_label.setText("Odabrana je datoteka s krivom ekstenzijom.")
            return
        
        packaged_files, package_error = self.parse_import_package(package_file.content)

        if package_error:
            self.view.error_label.setText(package_error)
            return

        log_bytes, key_bytes, signature_bytes = packaged_files

        # Provjeri može li se dekriptirati i je li ispravna, ako ne, napiši grešku
        aes_key, rsa_error = RsaHelper.decrypt(key_bytes, self.private_key)

        if rsa_error:
            self.view.error_label.setText("Nije moguće dekriptirati datoteku ključa: " + rsa_error)
            return

        # Provjeri može li se dekriptirati dekriptiranim ključem i je li ispravna, ako ne napiši grešku
        log_text, aes_error = AesHelper.decrypt(log_bytes, aes_key, False)

        if aes_error:
            self.view.error_label.setText("Nije moguće dekriptirati datoteku log zapisa: " + aes_error)
            return

        # Provjeri je li digitalni potpis ispravan i ako nije, ispiši grešku
        valid = RsaHelper.verify(log_text, signature_bytes, user_private_key)

        if not valid:
            self.view.error_label.setText("Digitalni potpis nije validan!")
            return

        # Otvori novi prozor s log zapisima koji se mogu skrolati
        self.result_view.text.setText(log_text)
        self._stack.setCurrentIndex(1)

    def parse_import_package(self, zip_bytes: bytes) -> tuple[tuple[bytes, bytes, bytes] | None, str | None]:
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zip_file:
            files = zip_file.namelist()

            if "encrypted_log.bin" not in files \
            or "encrypted_key.bin" not in files \
            or "signature.sig" not in files:
                return None, "Paket nije valjan ili nedostaju datoteke."

            log_bytes = zip_file.read("encrypted_log.bin")
            key_bytes = zip_file.read("encrypted_key.bin")
            sig_bytes = zip_file.read("signature.sig")

            return (log_bytes, key_bytes, sig_bytes), None

    def copy_public_key(self):
        QApplication.clipboard().setText(self.public_key)