from PySide6.QtWidgets import QFileDialog

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
    
file_manager = FileManager()