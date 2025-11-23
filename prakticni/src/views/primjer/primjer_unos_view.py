from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class PrimjerUnosView(QWidget):

    def __init__(self):
        super().__init__()

        self.label = QLabel("Primjer unosa")
        self.input_field = QLineEdit()
        self.submit_btn = QPushButton("Unesi")

        layout = QVBoxLayout()

        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)
