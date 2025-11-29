from PySide6.QtWidgets import QWidget, QLabel, QScrollArea, QFrame, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from src.views.components.file_item_widget import FileItemWidget

class PregledDatotekaView(QWidget):

    def __init__(self):
        super().__init__()

        self.title = QLabel("Moje datoteke")

        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

        self.list_container = QFrame()
        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(24)
        self.list_layout.setContentsMargins(8, 8, 8, 8)
        self.list_container.setLayout(self.list_layout)

        self.scroll_area.setWidget(self.list_container)

        self.import_btn = QPushButton("Prenesi")
        self.import_btn.setIcon(QIcon("src/pic/upload.svg"))
        self.import_btn.setToolTip("Prenesi datoteku")

        bottom_layout = QVBoxLayout()
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_layout.addWidget(self.import_btn, alignment=Qt.AlignHCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def set_files(self, file_records):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for rec in file_records:
            w = FileItemWidget(rec)
            self.list_layout.addWidget(w)

        self.list_layout.addStretch()