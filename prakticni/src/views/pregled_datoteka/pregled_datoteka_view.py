from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PregledDatotekaView(QWidget):

    def __init__(self):
        super().__init__()

        self.label = QLabel("Moje datoteke")

        layout = QVBoxLayout()

        layout.addWidget(self.label)

        self.setLayout(layout)