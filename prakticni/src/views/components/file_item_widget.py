from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QIcon
from datetime import datetime

class FileItemWidget(QWidget):
    def __init__(self, file_record):
        super().__init__()

        self.file_record = file_record

        self.name_label = QLabel(file_record["name"])

        date_text = ""
        date_modified = file_record["date_modified"]
        if date_modified:
            date_text = f"Ažurirana: {self.format_date(date_modified)}"
        else:
            date_text = f"Prenesena: {self.format_date(file_record['date_uploaded'])}"

        self.date_label = QLabel(date_text)

        left = QVBoxLayout()
        left.addWidget(self.name_label)
        left.addWidget(self.date_label)

        button_style = "QPushButton { padding: 0px; margin: 0px; }"

        self.btn_export = QPushButton()
        self.btn_export.setIcon(QIcon("src/pic/download.svg"))
        self.btn_export.setToolTip("Izvezi datoteku")
        self.btn_export.setFixedSize(40, 40)
        self.btn_export.setStyleSheet(button_style)
        self.btn_export.setProperty("class", "success")
        self.btn_export.clicked.connect(self.handle_export)
        
        self.btn_delete = QPushButton()
        self.btn_delete.setIcon(QIcon("src/pic/delete.svg"))
        self.btn_delete.setToolTip("Sigurnosno obriši datoteku")
        self.btn_delete.setFixedSize(40, 40)
        self.btn_delete.setStyleSheet(button_style)
        self.btn_delete.setProperty("class", "danger")
        self.btn_delete.clicked.connect(self.handle_delete)

        self.btn_share = QPushButton()
        self.btn_share.setIcon(QIcon("src/pic/share.svg"))
        self.btn_share.setToolTip("Dijeli datoteku")
        self.btn_share.setFixedSize(40, 40)
        self.btn_share.setStyleSheet(button_style)
        self.btn_share.setProperty("class", "info")
        self.btn_share.clicked.connect(self.handle_share)

        right = QHBoxLayout()
        right.addWidget(self.btn_export)
        right.addWidget(self.btn_delete)
        right.addWidget(self.btn_share)

        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addLayout(left)
        layout.addStretch()
        layout.addLayout(right)

        self.setLayout(layout)

    def format_date(self, date_text):
        return datetime.fromisoformat(date_text).strftime('%d.%m.%Y. %H:%M:%S')

    def handle_export(self):
        # TODO implementirati
        print("Export se handlea!")

    def handle_delete(self):
        # TODO implementirati
        print("Brisanje se handlea!")

    def handle_share(self):
        # TODO implementirati
        print("Dijeljenje se handlea!")