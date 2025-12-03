from PySide6.QtWidgets import QFileDialog, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit
from src.utils.file_selection_response import FileSelectionResponse

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
    
    def delete_file_dialog(self, parent, file_name: str) -> bool:
        dlg = QDialog(parent)
        dlg.setWindowTitle("UPOZORENJE!")
        
        layout = QVBoxLayout()
        
        label = QLabel(f"Ako ste sigurni da želite obrisati ovu datoteku,\nupišite {file_name} u prozor kako bi ju obrisali:")
        layout.addWidget(label)
        
        input_field = QLineEdit()
        layout.addWidget(input_field)
        
        error_label = QLabel("")
        error_label.setStyleSheet("color: red;")
        error_label.hide()
        layout.addWidget(error_label)
        
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)
        layout.addWidget(buttonBox)
        
        dlg.setLayout(layout)
        
        def on_accept():
            if input_field.text() == file_name:
                dlg.accept()
            else:
                error_label.setText(f"GREŠKA: Krivo upisano ime! Upišite točno: {file_name}")
                error_label.show()
        
        buttonBox.accepted.connect(on_accept)
        buttonBox.rejected.connect(dlg.reject)
        
        result = dlg.exec()
        return result == QDialog.Accepted
    
file_manager = FileManager()