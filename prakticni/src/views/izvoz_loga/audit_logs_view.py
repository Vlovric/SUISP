from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout

class AuditLogsView(QWidget):
    def __init__(self):
        super().__init__()

        self.description_label = QLabel(
            "Kako biste provjeriti audit log zapise nekog korisnika, potrebno je dati mu Vaš javni ključ. "
            "Kako bi se mogao provjeriti digitalni potpis korisnika, potrebno je u donje tekstualno polje zalijepiti njegov javni ključ. "
            "Zatim je potrebno učitati tri datoteke koje korisnik pošalje. Na vrhu piše koja se datoteka treba učitati. "
            "Nakon što je to gotovo, kliknite na gumb 'Dalje'. "
            "NAPOMENA: Svaki put kad se odjavite i prijavite, Vaši ključevi se promijene!"
        )
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignTop)

        self.copy_public_key_btn = QPushButton("Kopiraj javni ključ")
        self.copy_public_key_btn.setToolTip("Kopiraj javni ključ za kriptiranje audit logova")
        self.copy_public_key_btn.setProperty("class", "info")

        self.public_key_field = QTextEdit()
        self.public_key_field.setPlaceholderText("Unesite javni ključ korisnika ovdje...")

        copy_layout = QHBoxLayout()
        copy_layout.addStretch()
        copy_layout.addWidget(self.copy_public_key_btn)
        copy_layout.addStretch()

        self.load_files_btn = QPushButton("Dalje")

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.success_label = QLabel("")
        self.success_label.setStyleSheet("color: lime;")
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        next_layout = QHBoxLayout()
        next_layout.addStretch()
        next_layout.addWidget(self.load_files_btn)
        next_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.addWidget(self.description_label)
        main_layout.addLayout(copy_layout)
        main_layout.addWidget(self.public_key_field)
        main_layout.addStretch()
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(self.success_label)
        main_layout.addLayout(next_layout)

        self.setLayout(main_layout)