from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout

class UploadSharedFileView(QWidget):
    def __init__(self):
        super().__init__()

        self.description_label = QLabel(
            "Kako biste dobili dijeljenu datoteku, pošaljite osobi od koje tražite datoteku svoj javni ključ.\n"
            "Zatim kliknite na gumb 'Učitaj datoteku' kako biste ju unijeli u sustav."
        )
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignTop)

        self.copy_public_key_btn = QPushButton("Kopiraj javni ključ")
        self.copy_public_key_btn.setToolTip("Kopiraj javni ključ za učitavanje dijeljene datoteke")
        self.copy_public_key_btn.setProperty("class", "info")

        copy_layout = QHBoxLayout()
        copy_layout.addStretch()
        copy_layout.addWidget(self.copy_public_key_btn)
        copy_layout.addStretch()

        self.load_file_btn = QPushButton("Učitaj datoteku")

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.success_label = QLabel("")
        self.success_label.setStyleSheet("color: lime;")
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        next_layout = QHBoxLayout()
        next_layout.addStretch()
        next_layout.addWidget(self.load_file_btn)
        next_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.addWidget(self.description_label)
        main_layout.addLayout(copy_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(self.success_label)
        main_layout.addLayout(next_layout)

        self.setLayout(main_layout)