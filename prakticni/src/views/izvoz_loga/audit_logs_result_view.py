from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton, QHBoxLayout

class AuditLogsResultView(QWidget):
    def __init__(self):
        super().__init__()

        self.text = QLabel("Audit log zapisi...")
        self.text.setObjectName("title")
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.addWidget(self.text)
        scroll_layout.addStretch()
        scroll_content.setLayout(scroll_layout)

        scroll.setWidget(scroll_content)

        self.back_btn = QPushButton("Natrag")

        back_layout = QHBoxLayout()
        back_layout.addStretch()
        back_layout.addWidget(self.back_btn)
        back_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        main_layout.addLayout(back_layout)

        self.setLayout(main_layout)