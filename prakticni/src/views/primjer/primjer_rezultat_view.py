from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class PrimjerRezultatView(QWidget):

    def __init__(self):
        super().__init__()

        self.result_title = QLabel("Prijašnji unos dohvaćen iz baze:")
        self.result_label = QLabel("")

        self.back_btn = QPushButton("Natrag")

        layout = QVBoxLayout()

        layout.addWidget(self.result_title)
        layout.addWidget(self.result_label)
        layout.addWidget(self.back_btn)

        self.setLayout(layout)

    def set_result(self, text):
        """ Metoda za postavljanje rezultata u labelu """
        self.result_label.setText(text)