from PySide6.QtWidgets import QMainWindow, QStackedWidget
from src.views.primjer import PrimjerUnosView, PrimjerRezultatView # Uzimamo ekrane s kojima zelimo raditi
from src.models.primjer_model import PrimjerModel # Uzimamo model za rad s podacima koji ima staticke metode

class PrimjerController(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Primjer aplikacije")
        self.resize(400, 300)

        """ Inicijalizacija modela i ekrana """
        self.model = PrimjerModel()
        self.input_view = PrimjerUnosView()
        self.result_view = PrimjerRezultatView()

        """ Stacked widget za prebacivanje izmedu ekrana """
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.input_view) # index 0
        self.stacked_widget.addWidget(self.result_view) # index 1
        
        """ Postavljanje centralnog widgeta """
        self.setCentralWidget(self.stacked_widget)

        """ Povezivanje elemenata s metodama """
        self.input_view.submit_btn.clicked.connect(self.handle_submit)
        self.result_view.back_btn.clicked.connect(self.go_back)

    def handle_submit(self):
        text = self.input_view.input_field.text() # Dohvacamo uneseni tekst

        if not text:
            return
        
        self.result = PrimjerModel.insert_text(text) # Insertamo tekst u bazu preko modela
        if not self.result:
            # bio bi neki popup za poruku itd...
            return

        self.text = PrimjerModel.fetch_text_by_id(self.result) #nije nuzno potrebno jer imamo njegov text ali za primjer
        if not self.text:
            return
        
        self.result_view.set_result(self.text['text']) # Posto dobivamo dictionary iz modela passamo direkt u ovom slucaju atribut koji zelimo
        self.stacked_widget.setCurrentIndex(1) # Prebacujemo aktivni ekran na onaj s rezultatom

    def go_back(self):
        self.input_view.input_field.clear() # Cistimo input polje pri povratku
        self.stacked_widget.setCurrentIndex(0) # Vracamo se na ekran za unos





