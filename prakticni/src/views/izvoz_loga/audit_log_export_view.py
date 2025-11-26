from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton

class AuditLogExportView(QWidget):
    
    def __init__(self):
        super().__init__()

        label = QLabel("Izvoz audit loga")
        self.input_field = QLineEdit()
        self.submit_btn = QPushButton("Izvezi")

        layout = QVBoxLayout()

        layout.addWidget(label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)