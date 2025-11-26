from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QStackedWidget
from src.controllers.base_controller import BaseController

from src.views.izvoz_loga.audit_log_export_view import AuditLogExportView

class AuditLogExportController(BaseController):
    def __init__(self):
        super().__init__()

        self._stack = QStackedWidget()
        self.input_view = AuditLogExportView()

        self._stack.addWidget(self.input_view)

        self.input_view.submit_btn.clicked.connect(self.handle_submit)

    @property
    def root_widget(self) -> QWidget:
        return self._stack
    
    def reset(self):
        self.input_view.input_field.clear()
        self._stack.setCurrentIndex(0)

    def handle_submit(self):
        print("Gumb stisnut!")

