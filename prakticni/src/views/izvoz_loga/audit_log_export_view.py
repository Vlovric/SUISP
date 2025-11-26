from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton

class AuditLogExportView(QWidget):
    
    def __init__(self):
        super().__init__()

        label = QLabel("Izvoz audit loga")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Unesite javni ključ auditora")
        
        self.submit_btn = QPushButton("Izvezi")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)
        layout.addWidget(self.input_field)
        layout.addSpacing(12)
        layout.addWidget(self.submit_btn, alignment=Qt.AlignHCenter)

        self.setLayout(layout)