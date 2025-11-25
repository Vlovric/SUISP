from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QStackedWidget
from src.controllers.base_controller import BaseController

from src.views.primjer.primjer_unos_view import PrimjerUnosView # Uzimamo ekrane s kojima zelimo raditi
from src.views.primjer.primjer_rezultat_view import PrimjerRezultatView
from src.models.primjer.primjer_model import PrimjerModel # Uzimamo model za rad s podacima koji ima staticke metode

class PrimjerController(BaseController):
    navigate_forward = Signal()
    navigate_back = Signal()

    def __init__(self):
        super().__init__()

        """ Inicijalizacija modela, ekrana i stacka svih ekrana """
        self._stack = QStackedWidget()
        self.input_view = PrimjerUnosView()
        self.result_view = PrimjerRezultatView()

        """ Stacked widget za prebacivanje izmedu ekrana """
        self._stack.addWidget(self.input_view) # index 0
        self._stack.addWidget(self.result_view) # index 1

        """ Povezivanje elemenata s metodama """
        self.input_view.submit_btn.clicked.connect(self.handle_submit)
        self.result_view.back_btn.clicked.connect(self.go_back)

    @property
    def root_widget(self) -> QWidget:
        return self._stack # Svaki controller exposea svoj stack ekrana da bi glavni kontroler mogao loadat

    def reset(self): # Resetira view na prvi ekran i cleara sve, kad se stisne na navigaciji da sve bude clear
        self.input_view.input_field.clear()
        self._stack.setCurrentIndex(0)

    def handle_submit(self):
        text = self.input_view.input_field.text() # Dohvacamo uneseni tekst
        if not text:
            return
        
        result = PrimjerModel.insert_text(text) # Insertamo tekst u bazu preko modela
        if not result:
            # bio bi neki popup za poruku itd...
            return

        row = PrimjerModel.fetch_text_by_id(result) #nije nuzno potrebno jer imamo njegov text ali za primjer
        if not row:
            return
        
        self.result_view.set_result(row['text']) # Posto dobivamo dictionary iz modela passamo direkt u ovom slucaju atribut koji zelimo
        self._stack.setCurrentIndex(1) # Prebacujemo aktivni ekran na onaj s rezultatom
        self.navigate_forward.emit() # Emitamo signal da smo otisli naprijed

    def go_back(self):
        self.input_view.input_field.clear() # Cistimo input polje pri povratku
        self._stack.setCurrentIndex(0) # Vracamo se na ekran za unos
        self.navigate_back.emit() # Emitamo signal da smo se vratili nazad




