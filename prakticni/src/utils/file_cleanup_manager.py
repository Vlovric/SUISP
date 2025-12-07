from src.utils.path_manager import path_manager
from src.models.datoteka.datoteka_model import DatotekaModel
from src.utils.file_manager import file_manager
from src.utils.key_manager import key_manager
from src.utils.rsa_helper import RsaHelper
from src.utils.aes_helper import AesHelper
import os
import hashlib
from datetime import datetime

class FileCleanupManager:

    @staticmethod
    def cleanup_on_logout():
        unlocked_files = DatotekaModel.fetch_all_unlocked()

        for file in unlocked_files:

            file_content = file_manager.read_file(file["path"])
            if file_content is None:
                continue

            try:
                file_hash = hashlib.sha512(file_content).hexdigest()
            except Exception:
                continue

            try:
                private_key_decrypted = key_manager.get_private_key()
            except Exception:
                continue

            dek_encrypted_bytes = bytes.fromhex(file["dek_encrypted"])
            dek_bytes, error = RsaHelper.decrypt(dek_encrypted_bytes, private_key_decrypted)
            if error:
                continue

            bits = private_key_decrypted.key_size
            bytes_len = (bits + 7) // 8
            private_key_decrypted = b'\x00' * bytes_len
            del private_key_decrypted

            plaintext_content = file_content
            encrypted_content, error = AesHelper.encrypt(plaintext_content, dek_bytes)
            if error:
                continue

            plaintext_content = b'\x00' * len(plaintext_content)
            del plaintext_content

            vault_storage_path = path_manager.FILES_DIR
            encrypted_file_name = file["encrypted_name"]

            path = os.path.join(vault_storage_path, encrypted_file_name)
            successful = file_manager.save_file(path, encrypted_content)
            if not successful:
                continue

            dek_bytes = b'\x00' * len(dek_bytes)
            del dek_bytes

            if not file_manager.secure_delete(file["path"]):
                continue

            current_time = str(datetime.now().isoformat())
            DatotekaModel.update_file_lock(file['id'], path, file_hash, current_time)

        FileCleanupManager._cleanup_temp_directory()




    
    @staticmethod
    def cleanup_on_login():
        unlocked_files = DatotekaModel.fetch_all_unlocked()

        if not os.path.exists(path_manager.TEMP_DIR):
            return
        
        for file in unlocked_files:
            if not file['path'].startswith(str(path_manager.TEMP_DIR)):
                continue

            try:
                file_manager.secure_delete(file['path'])

                path = os.path.join(path_manager.FILES_DIR, file['encrypted_name'])
                DatotekaModel.set_file_lock(file['id'], 1, path)
            except OSError:
                pass

        FileCleanupManager._cleanup_temp_directory()
        

    @staticmethod
    def _cleanup_temp_directory():
        try:
            for filename in os.listdir(path_manager.TEMP_DIR):
                file_path = os.path.join(path_manager.TEMP_DIR, filename)
                if os.path.isfile(file_path):
                    file_manager.secure_delete(file_path)
        except OSError:
            pass

    