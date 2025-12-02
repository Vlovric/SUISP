from PySide6.QtCore import QObject, Signal, QEvent
from datetime import datetime
from src.utils.log_manager import log
from src.utils.key_manager import key_manager
from datetime import datetime

class ActivityMonitor(QObject):
    activity_detected = Signal()
    WARNING_TIME: int = 240  # seconds
    INACTIVITY_TIMEOUT: int = 15 * 60  # seconds
    last_activity: datetime
    
    def eventFilter(self, obj, event):
        # Prati sve tipke, klikove, scroll, pomak miša
        if event.type() in [
            QEvent.Type.MouseMove,
            QEvent.Type.MouseButtonPress,
            QEvent.Type.KeyPress,
            QEvent.Type.Wheel
        ]:
            self.activity_detected.emit()
        return False