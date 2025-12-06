from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from PySide6.QtCore import Qt
from src.views.components.unlock_file_item_widget import UnlockedFileItemWidget

class UnlockedFilesView(QWidget):

    def __init__(self):
        super().__init__()

        self.lock_buttons = []

        self.title = QLabel("Moje otključane datoteke")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)

        self.list_container = QFrame()
        self.list_layout = QVBoxLayout()
        self.list_layout.setSpacing(24)
        self.list_layout.setContentsMargins(8, 8, 8, 8)
        self.list_container.setLayout(self.list_layout)

        self.scroll_area.setWidget(self.list_container)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.error_label)
        self.setLayout(main_layout)

    def set_files(self, file_records):
        self.lock_buttons = []

        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for rec in file_records:
            w = UnlockedFileItemWidget(rec)
            self.lock_buttons.append((w.btn_lock, rec["id"]))
            self.list_layout.addWidget(w)
        
        self.list_layout.addStretch()