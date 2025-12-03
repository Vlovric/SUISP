from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton

class AuditLogExportView(QWidget):
    
    def __init__(self):
        super().__init__()

        label = QLabel("Izvoz audit loga")
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Unesite javni ključ auditora")
        self.input_field.setFixedHeight(200)
        
        self.submit_btn = QPushButton("Izvezi")

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.success_label = QLabel("")
        self.success_label.setStyleSheet("color: lime;")
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.copy_btn = QPushButton("Kopiraj")
        self.copy_btn.setToolTip("Kopiraj javni ključ za provjeru digitalnog potpisa")
        self.copy_btn.setProperty("class", "info")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)
        layout.addWidget(self.input_field)
        layout.addSpacing(12)
        layout.addWidget(self.submit_btn, alignment=Qt.AlignHCenter)
        layout.addWidget(self.error_label)
        layout.addWidget(self.success_label)
        layout.addWidget(self.copy_btn, alignment=Qt.AlignHCenter)

        self.setLayout(layout)