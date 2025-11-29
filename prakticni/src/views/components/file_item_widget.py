from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QIcon

class FileItemWidget(QWidget):
    def __init__(self, file_record):
        super().__init__()

        self.file_record = file_record

        self.name_label = QLabel(file_record["name"])

        date_text = ""
        date_modified = file_record["date_modified"]
        if date_modified:
            date_text = f"Ažurirana: {date_modified}"
        else:
            date_text = f"Prenesena: {file_record['date_uploaded']}"

        self.date_label = QLabel(date_text)

        left = QVBoxLayout()
        left.addWidget(self.name_label)
        left.addWidget(self.date_label)

        self.btn_export = QPushButton()
        self.btn_export.setIcon(QIcon("src/pic/download.svg"))
        self.btn_export.setToolTip("Izvezi datoteku")
        self.btn_export.clicked.connect(self.handle_export)
        
        self.btn_delete = QPushButton()
        self.btn_delete.setIcon(QIcon("src/pic/delete.svg"))
        self.btn_delete.setToolTip("Sigurnosno obriši datoteku")
        self.btn_delete.clicked.connect(self.handle_delete)

        self.btn_share = QPushButton()
        self.btn_share.setIcon(QIcon("src/pic/share.svg"))
        self.btn_share.setToolTip("Dijeli datoteku")
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

    def handle_export(self):
        # TODO implementirati
        print("Export se handlea!")

    def handle_delete(self):
        # TODO implementirati
        print("Brisanje se handlea!")

    def handle_share(self):
        # TODO implementirati
        print("Dijeljenje se handlea!")