from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout

class FileSharingView(QWidget):
    def __init__(self):
        super().__init__()

        self.description_label = QLabel(
            "Dijeljenje datoteke "
        )
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignTop)

        self.public_key_field = QTextEdit()
        self.public_key_field.setPlaceholderText("Unesite javni ključ osobe kojoj dijelite datoteku ovdje...")

        self.share_file_btn = QPushButton("Podijeli")
        self.share_file_btn.setProperty("class", "info")

        self.back_btn = QPushButton("Natrag")

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.success_label = QLabel("")
        self.success_label.setStyleSheet("color: lime;")
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        next_layout = QHBoxLayout()
        next_layout.addStretch()
        next_layout.addWidget(self.share_file_btn)
        next_layout.addWidget(self.back_btn)
        next_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.addWidget(self.description_label)
        main_layout.addWidget(self.public_key_field)
        main_layout.addStretch()
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(self.success_label)
        main_layout.addLayout(next_layout)

        self.setLayout(main_layout)