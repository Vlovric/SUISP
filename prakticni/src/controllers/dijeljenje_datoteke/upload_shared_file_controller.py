from datetime import datetime
import hashlib
import io
import json
import os
import uuid
import zipfile
from src.models.datoteka.datoteka_model import DatotekaModel
from src.utils.security_policy_manager import security_policy_manager
from src.utils.aes_helper import AesHelper
from src.utils.rsa_helper import RsaHelper
from src.views.dijeljenje_datoteke.upload_shared_file_view import UploadSharedFileView
from src.controllers.base_controller import BaseController
from PySide6.QtWidgets import QWidget, QStackedWidget, QApplication
from src.utils.key_manager import key_manager
from src.utils.file_manager import file_manager
from src.utils.log_manager import log

class UploadSharedFileController(BaseController):
    def __init__(self):
        super().__init__()

        self._stack = QStackedWidget()
        self.view = UploadSharedFileView()

        self._stack.addWidget(self.view)

        self.view.copy_public_key_btn.clicked.connect(self.copy_public_key)
        self.view.load_file_btn.clicked.connect(self.upload_file)

    @property
    def root_widget(self) -> QWidget:
        return self._stack
    
    def reset(self):
        self.view.error_label.setText("")
        self.view.success_label.setText("")
    
    def go_back(self):
        self.reset()

    def upload_file(self):
        self.view.error_label.setText("")
        self.view.success_label.setText("")

        # Učitavanje datoteke
        package_file = file_manager.select_file_dialog(self, "Otvori dijeljenu datoteku.", "Shared File Package (*.shfipkg)")

        if package_file is None:
            self.view.error_label.setText("Nije moguće otvoriti datoteku.")
            return
        
        if not package_file.successful:
            self.view.error_label.setText("Nije moguće otvoriti datoteku.")
            return
        
        if not package_file.filename.endswith(".shfipkg") or not package_file.is_binary:
            self.view.error_label.setText("Odabrana je datoteka s krivom ekstenzijom.")
            return
        
        packaged_files, package_error = self.parse_import_package(package_file.content)

        if package_error:
            self.view.error_label.setText(package_error)
            return
        
        encrypted_dek_bytes, file_bytes, filename, is_binary = packaged_files

        # Pokušaj dekripcije DEK-a
        private_key = key_manager.get_private_key()
        decrypted_dek, decryption_error = RsaHelper.decrypt(encrypted_dek_bytes, private_key)

        if decryption_error:
            self.view.error_label.setText(decryption_error + " - DEK je neispravan")
            return
        
        # Pokušaj dekripcije same datoteke (nigdje se ne sprema, samo u memoriji)
        decrypted_file, decryption_error = AesHelper.decrypt(file_bytes, decrypted_dek)

        if decryption_error:
            self.view.error_label.setText(decryption_error + " - datoteka je neispravna")
            return
        
        # Brišemo dekriptirani DEK - bilo potrebno samo da se testira je li kriptiran ispravnim javnim ključem
        decrypted_dek = b'\x00' * len(decrypted_dek)
        del decrypted_dek

        # Spremamo file na disk
        vault_storage_path = security_policy_manager.get_policy_param("vault_storage_path")
        encrypted_file_name = f"{str(uuid.uuid4())}.bin"

        path = os.path.join(vault_storage_path, encrypted_file_name)
        successful = file_manager.save_file(path, file_bytes)
        if not successful:
            log(f"Nije moguće spremiti podijeljenu kriptiranu datoteku")
            self.view.error_label.setText("Nije moguće spremiti datoteku.")
            return

        # Ubacivanje u bazu
        if is_binary:
            hash = hashlib.sha512(decrypted_file)
        else:
            hash = hashlib.sha512(decrypted_file.encode())
        current_time = str(datetime.now().isoformat())

        DatotekaModel.insert_file_entry(filename, encrypted_file_name, path, is_binary, current_time, encrypted_dek_bytes.hex(), hash.hexdigest())
        log(f"U sustav je prenesena dijeljena datoteka {filename}")

        # Brišemo dekriptiranu datoteku u memoriji
        decrypted_file = b'\x00' * len(decrypted_file)
        del decrypted_file

        self.view.success_label.setText("Dijeljena datoteka ubačena je u trezor.")

    def parse_import_package(self, zip_bytes: bytes) -> tuple[tuple[bytes, bytes, str, bool] | None, str | None]:
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zip_file:
            files = zip_file.namelist()

            if "dek.bin" not in files \
            or "file.bin" not in files \
            or "metadata.json" not in files:
                return None, "Paket nije valjan ili nedostaju datoteke."
            
            dek_bytes = zip_file.read("dek.bin")
            file_bytes = zip_file.read("file.bin")
            metadata_bytes = zip_file.read("metadata.json")

            try:
                metadata = json.loads(metadata_bytes.decode("utf-8"))
            except:
                return None, "Metapodaci su neispravni."
            filename = metadata.get("filename")
            
            if not filename:
                return None, "Metapodaci su neispravni: nedostaje naziv."
            
            is_binary = metadata.get("is_binary")
            if is_binary is None or not isinstance(is_binary, bool):
                return None, "Metapodaci su neispravni: nedostaje informacija je li datoteka binarna."
            
            return (dek_bytes, file_bytes, filename, is_binary), None

    def copy_public_key(self):
        public_key = key_manager.get_public_key()
        QApplication.clipboard().setText(public_key)