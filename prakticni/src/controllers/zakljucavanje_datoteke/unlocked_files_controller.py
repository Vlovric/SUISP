from src.controllers.base_controller import BaseController
from src.views.zakljucavanje_datoteke.unlocked_files_view import UnlockedFilesView
from src.models.datoteka.datoteka_model import DatotekaModel
from src.utils.file_manager import file_manager
from src.utils.key_manager import key_manager
from src.utils.rsa_helper import RsaHelper
from src.utils.aes_helper import AesHelper
from src.utils.security_policy_manager import security_policy_manager
from src.utils.log_manager import log

from PySide6.QtWidgets import QStackedWidget, QWidget
from functools import partial
import hashlib
import os

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
        
        # - ponovno se hashira i pohranjuje u bazu
        try:
            file_hash = hashlib.sha512(file_content).hexdigest()
        except Exception as e:
            self.view.error_label.setText("Pogreška pri izračunu hash vrijednosti datoteke.")
            return
                
        
        
        # - uzimam privatni iz baze, dekriptiram
        try:
            private_key_decrypted = key_manager.get_private_key()
        except Exception as e:
            self.view.error_label.setText(str(e))
            return
        
        # - uzimam DEK od filea, dekriptiram
        dek_encrypted_bytes = bytes.fromhex(file["dek_encrypted"])
        dek_bytes, error = RsaHelper.decrypt(dek_encrypted_bytes, private_key_decrypted)
        if error:
            self.view.error_label.setText("Pogreška pri pokušaju zaključavanja datoteke: " + error)
        # - nukeam privatni iz memorije
        bits = private_key_decrypted.key_size
        bytes_len = (bits + 7) // 8
        private_key_decrypted = b'\x00' * bytes_len

        # - kriptiram datoteku s DEK-om
        plaintext_content = file_content
        encrypted_content, error = AesHelper.encrypt(plaintext_content, dek_bytes)
        if error:
            self.view.error_label.setText("Pogreška pri pokušaju zaključavanja datoteke: " + error)
            return

        # - premjestam u izvorni folder
        vault_storage_path = security_policy_manager.get_policy_param("vault_storage_path")
        encrypted_file_name = file["encrypted_name"]

        path = os.path.join(vault_storage_path, encrypted_file_name)
        successful = file_manager.save_file(path, encrypted_content)
        if not successful:
            self.view.error_label.setText("Pogreška pri pokušaju spremanja zaključane datoteke u trezor.")
            return

        # - safe deleteam (overwrite s nule i delete) plaintext datoteku TODO
        # - nukeam DEK iz memorije
        dek_bytes = b'\x00' * len(dek_bytes)
        # - mijenjam atribut u bazi da je zakljucana
        # - updateam putanju na kriptiranu
        DatotekaModel.update_file_lock(file_id, path, file_hash)
        # - loggam zakljucavanje
        log(f"Datoteka {file['name']} je zaključana i spremljena u trezor.")
        
        return
    