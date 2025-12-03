import io
import zipfile
from PySide6.QtWidgets import QWidget, QStackedWidget
from src.utils.file_selection_response import FileSelectionResponse
from src.views.dijeljenje_datoteke.file_sharing_view import FileSharingView
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
import hashlib
import uuid
import os

class PregledDatotekaController(BaseController):
    def __init__(self):
        super().__init__()

        self._stack = QStackedWidget()
        self.view = PregledDatotekaView()
        self.share_view = FileSharingView()
        self._stack.addWidget(self.view)
        self._stack.addWidget(self.share_view)
        self._stack.setCurrentIndex(0)

        self.load_files()

        self.view.import_btn.clicked.connect(self.handle_new_file)
        self.share_view.back_btn.clicked.connect(self.reset)
        self.share_view.share_file_btn.clicked.connect(self.handle_share)

        self.file_to_share = None

    @property
    def root_widget(self) -> QWidget:
        return self._stack
    
    def reset(self):
        self.load_files()
        self.share_view.error_label.setText("")
        self.share_view.success_label.setText("")
        self.share_view.public_key_field.setText("")
        self._stack.setCurrentIndex(0)

    # Učitava datoteke iz baze (pozivati npr. kod dodavanja nove ili brisanja kako bi se osvježio popis)
    def load_files(self):
        files = DatotekaModel.fetch_all()
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
            btn.clicked.connect(partial(self.open_share_view, file_id))
    
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

        DatotekaModel.insert_file_entry(file.filename, path, file.is_binary, current_time, dek_encrypted.hex(), hash.hexdigest())
        log(f"U sustav je prenesena datoteka {file.filename}")

        # Overwritea datoteku s nulama i onda ju obriše
        file.content = b'\x00' * len(file.content)
        del file

        self.reset()

    def handle_export(self, id):
        # TODO implementirati
        print(f"Export zapisa s {id} se handlea!")
        self.reset()

    def handle_delete(self, id):
        # TODO implementirati
        print(f"Brisanje zapisa s {id} se handlea!")
        self.reset()

    def open_share_view(self, id):
        self.file_to_share = DatotekaModel.get_file(id)
        if self.file_to_share is None:
            self.view.error_label.setText("Ne postoji datoteka.")
            return
        
        self.share_view.description_label.setText(f"Dijeljenje datoteke '{self.file_to_share['name']}'\nZa dijeljenje datoteke s korisnikom, u donje polje zalijepite njegov javni ključ.")
        
        self._stack.setCurrentIndex(1)

    def handle_share(self):
        self.share_view.error_label.setText("")
        self.share_view.success_label.setText("")
        
        if self.file_to_share is None:
            return
        
        public_key = self.share_view.public_key_field.toPlainText()

        if (len(public_key) == 0):
            self.share_view.error_label.setText("Javni ključ nije unesen!")
            return
        
        # Dohvati datoteku
        file = FileSelectionResponse(self.file_to_share["path"])

        if file is None:
            self.share_view.error_label.setText("Nije moguće otvoriti datoteku.")
            return
        
        if not file.successful:
            self.share_view.error_label.setText("Nije moguće otvoriti datoteku.")
            return

        # Dekriptiraj DEK svojim privatnim ključem
        encrypted_dek = self.file_to_share["dek_encrypted"]
        private_key = key_manager.get_private_key()
        decrypted_dek, decryption_error = RsaHelper.decrypt(bytes.fromhex(encrypted_dek), private_key)

        if decryption_error:
            self.share_view.error_label.setText(decryption_error)
            return

        # Enkriptiraj DEK unesenim javnim ključem
        dek_bytes, encryption_error = RsaHelper.encrypt(decrypted_dek, public_key)

        if encryption_error:
            self.share_view.error_label.setText(encryption_error)
            return

        # Sve spremi u jedan paket i spremi datoteku
        now = datetime.now().isoformat()
        original_filename = self.file_to_share["name"].split(".")[0]
        filename = f"{original_filename}_shared_file_{datetime.fromisoformat(now).strftime('%Y-%m-%d_%H-%M-%S')}.shfipkg"
        zip_bytes = self.build_share_package(file.content, dek_bytes)

        if not file_manager.open_file_download_dialog(self, "Spremi datoteku za podijeliti.", filename, zip_bytes):
            self.share_view.error_label.setText("Nije moguće spremiti datoteku za dijeliti.")
            return

        self.share_view.success_label.setText("Datoteka za dijeliti je uspješno spremljena.")

    def build_share_package(self, file_bytes: bytes, dek_bytes: bytes) -> bytes:
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("file.bin", file_bytes)
            zip_file.writestr("dek.bin", dek_bytes)

        return buffer.getvalue()
        

        
