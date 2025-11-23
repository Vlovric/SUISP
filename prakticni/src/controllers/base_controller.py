from PySide6.QtCore import QObject

class BaseController(QObject):
    def __init__(self):
        super().__init__()

    @property
    def root_widget(self):
        """Return the QWidget that represents this controller's UI."""
        raise NotImplementedError