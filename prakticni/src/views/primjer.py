from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class PrimjerUnosView(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Primjer unosa")
        self.input_field = QLineEdit()
        self.submit_btn = QPushButton("Unesi")

        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

class PrimjerRezultatView(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.result_title = QLabel("Prijašnji unos dohvaćen iz baze:")
        self.result_label = QLabel("")

        self.back_btn = QPushButton("Natrag")

        layout.addWidget(self.result_title)
        layout.addWidget(self.result_label)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)

    def set_result(self, text):
        """ Metoda za postavljanje rezultata u labelu """
        self.result_label.setText(text)
