from PySide6.QtCore import QObject

class BaseController(QObject):
    def __init__(self):
        super().__init__()

    @property
    def root_widget(self):
        """Vraća QWidget tj content ekrana koji se loada u glavni ekran, treba overrideat"""
        raise NotImplementedError
    
    def reset(self):
        """ Resetira kontroler na početno stanje, mora se overrideat """
        raise NotImplementedError