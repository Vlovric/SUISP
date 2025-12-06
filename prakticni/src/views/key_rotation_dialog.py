from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt

class KeyRotationDialog(QDialog):
    def __init__(self, total_files: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rotacija ključeva u tijeku")
        self.setModal(True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.label = QLabel("Rotacija ključeva u tijeku. Molimo pričekajte...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, total_files)
        self.progress_bar.setValue(0)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def update_progress(self, current: int, total: int):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.label.setText(f"Rotacija ključeva: {current} / {total}")