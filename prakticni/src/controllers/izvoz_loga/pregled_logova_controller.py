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
        self.view.public_key_field.clear()
        self._stack.setCurrentIndex(0)

    def copy_public_key(self):
        QApplication.clipboard().setText(self.public_key)

    def load_files(self):
        self.view.error_label.setText("")
        self.view.success_label.setText("")

        # Provjeri je li unesen privatni ključ
        user_private_key = self.view.public_key_field.toPlainText()

        if (len(user_private_key) == 0):
            self.view.error_label.setText("Javni ključ osobe nije unesen!")
            return

        # Učitaj datoteku ključa
        key_file = file_manager.select_file_dialog(self, "Otvori datoteku ključa.")

        if key_file is None:
            self.view.error_label.setText("Nije moguće otvoriti datoteku.")
            return
        
        if not key_file.successful:
            self.view.error_label.setText("Nije moguće otvoriti datoteku!")
            return
        
        if not key_file.filename.endswith(".bin") or not key_file.is_binary:
            self.view.error_label.setText("Odabrana je datoteka s krivom ekstenzijom.")
            return

        # Provjeri može li se dekriptirati i je li ispravna, ako ne, napiši grešku
        aes_key, rsa_error = RsaHelper.decrypt(key_file.content, self.private_key)

        if rsa_error:
            self.view.error_label.setText("Nije moguće dekriptirati datoteku ključa: " + rsa_error)
            return

        # Učitaj datoteku
        file = file_manager.select_file_dialog(self, "Otvori datoteku potpisanih audit zapisa.")

        if file is None:
            self.view.error_label.setText("Nije moguće otvoriti datoteku.")
            return
        
        if not file.successful:
            self.view.error_label.setText("Nije moguće otvoriti datoteku!")
            return
        
        if not file.filename.endswith(".bin") or not file.is_binary:
            self.view.error_label.setText("Odabrana je datoteka s krivom ekstenzijom.")
            return

        # Provjeri može li se dekriptirati dekriptiranim ključem i je li ispravna, ako ne napiši grešku
        log_text, aes_error = AesHelper.decrypt(file.content, aes_key, False)

        if aes_error:
            self.view.error_label.setText("Nije moguće dekriptirati datoteku log zapisa: " + aes_error)
            return

        # Učitaj datoteku digitalnog potpisa
        signature_file = file_manager.select_file_dialog(self, "Otvori digitalni potpis.")

        if signature_file is None:
            self.view.error_label.setText("Nije moguće otvoriti datoteku.")
            return
        
        if not signature_file.successful:
            self.view.error_label.setText("Nije moguće otvoriti datoteku!")
            return
        
        if not signature_file.filename.endswith(".sig") or not signature_file.is_binary:
            self.view.error_label.setText("Odabrana je datoteka s krivom ekstenzijom.")
            return

        # Provjeri je li digitalni potpis ispravan i ako nije, ispiši grešku
        valid = RsaHelper.verify(log_text, signature_file.content, user_private_key)

        if not valid:
            self.view.error_label.setText("Digitalni potpis nije validan!")
            return

        # Otvori novi prozor s log zapisima koji se mogu skrolati
        self.result_view.text.setText(log_text)
        self._stack.setCurrentIndex(1)

    def go_back(self):
        self.reset()