from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from src.utils.path_manager import path_manager

class UnlockedFileItemWidget(QWidget):
    def __init__(self, file_record):
        super().__init__()

        self.file_record = file_record

        self.name_label = QLabel(file_record["name"])

        left = QVBoxLayout()
        left.addWidget(self.name_label)

        button_style = "QPushButton { padding: 0px; margin: 0px; }"

        self.btn_lock = QPushButton()
        icon_path = str(path_manager.get_resource_path("src/pic/lock.svg"))
        self.btn_lock.setIcon(QIcon(icon_path))
        self.btn_lock.setIconSize(QSize(36, 36))

        self.btn_lock.setToolTip("Zaključaj datoteku")
        self.btn_lock.setFixedSize(40, 40)
        self.btn_lock.setStyleSheet(button_style)
        self.btn_lock.setProperty("class", "success")

        right = QHBoxLayout()
        right.addWidget(self.btn_lock)

        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addLayout(left)
        layout.addStretch()
        layout.addLayout(right)

        self.setLayout(layout)

