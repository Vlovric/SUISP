from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

class FileItemWidget(QWidget):
    def __init__(self, file_record):
        super().__init__()

        self.file_record = file_record

        self.name_label = QLabel(file_record["name"])

        date_text = f"Prenesena: {file_record['date_uploaded']}"
        date_modified = file_record["date_modified"]
        if date_modified:
            date_text += f" Ažurirana: {date_modified}"

        self.date_label = QLabel(date_text)

        left = QVBoxLayout()
        left.addWidget(self.name_label)
        left.addWidget(self.date_label)

        self.btn_export = QPushButton("Izvezi")
        self.btn_delete = QPushButton("Obriši")
        self.btn_share = QPushButton("Dijeli")

        self.btn_export.clicked.connect(self.handle_export)
        self.btn_delete.clicked.connect(self.handle_delete)
        self.btn_share.clicked.connect(self.handle_share)

        right = QHBoxLayout()
        right.addWidget(self.btn_export)
        right.addWidget(self.btn_delete)
        right.addWidget(self.btn_share)

        layout = QHBoxLayout()
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