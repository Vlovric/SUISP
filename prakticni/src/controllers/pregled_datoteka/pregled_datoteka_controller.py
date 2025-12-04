from PySide6.QtWidgets import QWidget, QStackedWidget
from src.utils.rsa_helper import RsaHelper
from src.utils.aes_helper import AesHelper
from src.models.datoteka.datoteka_model import DatotekaModel
from src.controllers.base_controller import BaseController
from src.views.pregled_datoteka.pregled_datoteka_view import PregledDatotekaView
from functools import partial
from src.utils.file_manager import file_manager
from src.utils.key_manager import key_manager
from src.utils.security_policy_manager import security_policy_manager
from datetime import datetime
from src.utils.log_manager import log
from pathlib import Path
from src.utils.process_helper import process_helper
import hashlib
import uuid
import os

class PregledDatotekaController(BaseController):
    def __init__(self):
        super().__init__()

        self._stack = QStackedWidget()
        self.view = PregledDatotekaView()
        self._stack.addWidget(self.view)

        self.load_files()

        self.view.import_btn.clicked.connect(self.handle_new_file)

    @property
    def root_widget(self) -> QWidget:
        return self._stack
    
    def reset(self):
        self.load_files()
        self._stack.setCurrentIndex(0)

    # Učitava datoteke iz baze (pozivati npr. kod dodavanja nove ili brisanja kako bi se osvježio popis)
    def load_files(self):
        files = DatotekaModel.fetch_all_locked()
        self.view.set_files(files)
        self.connect_buttons()

    # Povezuje sve gumbove sa handlerima
    def connect_buttons(self):
        for export_btn in self.view.export_buttons:
            btn, file_id = export_btn
            btn.clicked.connect(partial(self.handle_export, file_id))

        for delete_btn in self.view.delete_buttons:
            btn, file_id = delete_btn
            btn.clicked.connect(partial(self.handle_delete, file_id))

        for share_btn in self.view.share_buttons:
            btn, file_id = share_btn
            btn.clicked.connect(partial(self.handle_share, file_id))
    
    def handle_new_file(self):
        file = file_manager.select_file_dialog(self)
        if file == None:
            return
        
        kek = key_manager.get_public_key()
        dek = AesHelper.generate_key()

        dek_encrypted, error = RsaHelper.encrypt(dek, kek)
        if error:
            self.view.error_label.setText(error)
            return

        encrypted_file_name = f"{str(uuid.uuid4())}.bin"

        encrypted_content, error = AesHelper.encrypt(file.content, dek)
        if error:
            self.view.error_label.setText(error)
            return

        vault_storage_path = security_policy_manager.get_policy_param("vault_storage_path")

        path = os.path.join(vault_storage_path, encrypted_file_name)
        successful = file_manager.save_file(path, encrypted_content)
        if not successful:
            log(f"Nije moguće spremiti kriptiranu datoteku nastalu kriptiranjem datoteke {file.filename}")
            self.view.error_label.setText("Nije moguće spremiti datoteku.")
            return
        
        # Hashiram NE-kriptiran sadržaj (provjeriti je li ispravno),
        # pa se može provjeriti nakon dekriptiranja kod izvoza datoteke iz trezora je li enkriptirana datoteka mijenjana
        if file.is_binary:
            hash = hashlib.sha512(file.content)
        else:
            hash = hashlib.sha512(file.content.encode())
        current_time = str(datetime.now().isoformat())

        DatotekaModel.insert_file_entry(file.filename, encrypted_file_name, path, file.is_binary, current_time, dek_encrypted.hex(), hash.hexdigest())
        log(f"U sustav je prenesena datoteka {file.filename}")

        # Overwritea datoteku s nulama i onda ju obriše
        file.content = b'\x00' * len(file.content)
        del file

        self.reset()

    def handle_export(self, id):

        file = DatotekaModel.fetch_by_id(id)
        if not file:
            self.view.error_label.setText("Datoteka nije pronađena u bazi.")
            return
        
        try:
            private_key_decrypted = key_manager.get_private_key()
        except Exception as e:
            self.view.error_label.setText("Pogreška pri pokušaju otključavanja datoteke: " + str(e))
            return
        
        dek_encrypted_bytes = bytes.fromhex(file["dek_encrypted"])
        dek_bytes, error = RsaHelper.decrypt(dek_encrypted_bytes, private_key_decrypted)
        if error:
            self.view.error_label.setText("Pogreška pri pokušaju otključavanja datoteke: " + error)
            return
        
        bits = private_key_decrypted.key_size
        bytes_len = (bits + 7) // 8
        private_key_decrypted = b'\x00' * bytes_len

        encrypted_content = file_manager.read_file(file["path"])
        if encrypted_content is None:
            self.view.error_label.setText("Pogreška pri pokušaju čitanja datoteke iz trezora.")
            return
        
        decrypted_content, error = AesHelper.decrypt(encrypted_content, dek_bytes, file["binary"])
        if error:
            self.view.error_label.setText("Pogreška pri pokušaju otključavanja datoteke: " + error)
            return
        
        dek_bytes = b'\x00' * len(dek_bytes)

        old_hash = file["hash"]
        if file["binary"]:
            new_hash = hashlib.sha512(decrypted_content)
        else:
            new_hash = hashlib.sha512(decrypted_content.encode())
        
        if old_hash != new_hash.hexdigest():
            self.view.error_label.setText("Datoteka je oštećena ili je mijenjana dok je bila zaključana.")

        # Ovo sa pathovima je privremeno za development TODO
        temp_path = Path(__file__).parent.parent.parent.parent / "data" / "vault_storage" / "temp_otkljucane"
        if not temp_path.exists():
            os.makedirs(temp_path)
        full_path = temp_path / file["name"]
        #

        successful = file_manager.save_file(full_path, decrypted_content)
        decrypted_content = b'\x00' * len(decrypted_content)
        if not successful:
            self.view.error_label.setText("Pogreška pri pokušaju spremanja otključane datoteke.")
            return
        
        process_helper.open_file_in_default_app(str(full_path))

        DatotekaModel.set_file_lock(id, 0, str(full_path))
        log(f"Datoteka {file['name']} je otključana iz trezora.")
        
        self.reset()

    def handle_delete(self, id):
        # TODO implementirati
        print(f"Brisanje zapisa s {id} se handlea!")
        self.reset()

    def handle_share(self, id):
        # TODO implementirati
        print(f"Dijeljenje zapisa s {id} se handlea!")
        self.reset()