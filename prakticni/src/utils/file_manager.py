from PySide6.QtWidgets import QFileDialog
from src.utils.file_selection_response import FileSelectionResponse
import os

class FileManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileManager, cls).__new__(cls)
        return cls._instance
    
    def open_file_download_dialog(self, component, 
                                  save_text: str, filename: str, data: str, 
                                  save_options: str = "Text Files (*.txt);;All Files (*)", encoding: str = "utf-8") -> bool:
        path, _ = QFileDialog.getSaveFileName(
            component.root_widget, 
            save_text,
            filename,
            save_options
        )

        return self.save_file(path, data, encoding)

    def save_file(self, path, data, encoding = None) -> bool:
        is_binary_file = isinstance(data, (bytes, bytearray))
        
        if path:
            try:
                if is_binary_file:
                    with open(path, "wb") as f:
                        f.write(data)
                else:
                    with open(path, "w", encoding=encoding) as f:
                        f.write(data)
            except OSError:
                return False
            
        return True
    
    def select_file_dialog(self, component, 
                    open_text: str = "Otvori datoteku",
                    file_filter: str = "All Files (*)", ) -> FileSelectionResponse | None:
        path, _ = QFileDialog.getOpenFileName(
            component.root_widget,
            open_text,
            "",
            file_filter
        )

        if not path:
            return None
        
        return FileSelectionResponse(path)
    
    def read_file(self, path: str) -> bytes | None:
        if not path:
            return None
        try:
            with open(path, "rb") as f:
                return f.read()
        except OSError:
            return None
        
    def secure_delete(self, path: str) -> bool:
        if not path:
            return False
        try:
            size = os.path.getsize(path)
            with open(path, "r+b") as f:
                chunk = b"\x00" * (1024 * 1024)  # 1 MB
                remaining = size
                while remaining > 0:
                    to_write = chunk if remaining >= len(chunk) else b"\x00" * remaining
                    f.write(to_write)
                    remaining -= len(to_write)
                f.flush()
                os.fsync(f.fileno())
            
            try:
                dirpath = os.path.dirname(path)
                tmpname = os.path.join(dirpath, f".del_{os.urandom(8).hex()}")
                os.replace(path, tmpname)
                path = tmpname
            except Exception:
                pass
            os.remove(path)
            return True
        except Exception:
            return False
    
file_manager = FileManager()