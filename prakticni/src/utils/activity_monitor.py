from PySide6.QtCore import QObject, Signal, QEvent
from datetime import datetime
from src.utils.log_manager import log
from src.utils.key_manager import key_manager
from datetime import datetime
from src.utils.security_policy_manager import security_policy_manager

class ActivityMonitor(QObject):
    activity_detected = Signal()
    WARNING_TIME: int = security_policy_manager.get_policy_param("session_timeout_minutes")
    INACTIVITY_TIMEOUT: int = security_policy_manager.get_policy_param("inactivity_timeout_minutes") * 60
    last_activity: datetime
    
    def eventFilter(self, obj, event):
        if event.type() in [
            QEvent.Type.MouseMove,
            QEvent.Type.MouseButtonPress,
            QEvent.Type.KeyPress,
            QEvent.Type.Wheel
        ]:
            self.activity_detected.emit()
        return False