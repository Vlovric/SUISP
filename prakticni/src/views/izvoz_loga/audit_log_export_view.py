from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton

class AuditLogExportView(QWidget):
    
    def __init__(self):
        super().__init__()

        label = QLabel("Izvoz audit loga")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Unesite javni ključ auditora")
        
        self.submit_btn = QPushButton("Izvezi")

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)
        layout.addWidget(self.input_field)
        layout.addSpacing(12)
        layout.addWidget(self.submit_btn, alignment=Qt.AlignHCenter)
        layout.addWidget(self.error_label)

        self.setLayout(layout)