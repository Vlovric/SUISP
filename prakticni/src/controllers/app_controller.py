from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QPushButton, QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtCore import QTimer, QCoreApplication, Signal
from src.utils.activity_monitor import ActivityMonitor
from datetime import datetime

from functools import partial
from src.controllers.izvoz_loga.pregled_logova_controller import AuditLogsController
from src.controllers.pregled_datoteka.pregled_datoteka_controller import PregledDatotekaController
from src.controllers.izvoz_loga.izvoz_loga_controller import AuditLogExportController
from src.controllers.zakljucavanje_datoteke.unlocked_files_controller import UnlockedFilesController
from src.controllers.dijeljenje_datoteke.upload_shared_file_controller import UploadSharedFileController
from src.utils.key_manager import key_manager
from src.utils.log_manager import log
from src.utils.security_policy_manager import security_policy_manager
from src.views.components.flow_layout import FlowLayout
from src.utils.file_cleanup_manager import FileCleanupManager

class AppController(QMainWindow):
    logout_requested = Signal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sigurnosni trezor datoteka")
        self.resize(1000, 800)
        self.center()
        self.INACTIVITY_TIMEOUT = security_policy_manager.get_policy_param("inactivity_timeout_minutes") * 60 
        self.WARNING_TIME = security_policy_manager.get_policy_param("session_timeout_minutes")

        self.idle_timer = QTimer()
        self.idle_timer.timeout.connect(self._check_idle)
        self.idle_timer.start(1000)
        self.warning_timer = QTimer()
        self.warning_timer.timeout.connect(self._update_warning)
        self.warning_remaining = 0
        
        self.last_activity = datetime.now()
        
        self.activity_monitor = ActivityMonitor()
        self.activity_monitor.activity_detected.connect(self._reset_idle)
        
        QCoreApplication.instance().installEventFilter(self.activity_monitor)

        nav_widget = QWidget()
        nav_layout = FlowLayout(nav_widget)
        nav_layout.setContentsMargins(10, 10, 10, 10)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.controllers = {}

        self. _register_controller("pregled_datoteka", PregledDatotekaController())
        btn1 = QPushButton("Zaključane datoteke")
        btn1.setObjectName("nav_btn")
        btn1.clicked.connect(partial(self._show_controller, "pregled_datoteka"))
        nav_layout.addWidget(btn1)

        self._register_controller("otkljucane_datoteke", UnlockedFilesController())
        btn2 = QPushButton("Otključane datoteke")
        btn2.setObjectName("nav_btn")
        btn2.clicked.connect(partial(self._show_controller, "otkljucane_datoteke"))
        nav_layout.addWidget(btn2)
        
        self._register_controller("prijenos_dijeljene_datoteke", UploadSharedFileController())
        btn3 = QPushButton("Prijenos dijeljene datoteke")
        btn3.setObjectName("nav_btn")
        btn3.clicked.connect(partial(self._show_controller, "prijenos_dijeljene_datoteke"))
        nav_layout.addWidget(btn3)

        self._register_controller("izvoz_audit_logova", AuditLogExportController())
        btn4 = QPushButton("Izvoz audit logova")
        btn4.setObjectName("nav_btn")
        btn4.clicked.connect(partial(self._show_controller, "izvoz_audit_logova"))
        nav_layout.addWidget(btn4)

        self._register_controller("pregled_audit_logova", AuditLogsController())
        btn5 = QPushButton("Pregled audit logova")
        btn5.setObjectName("nav_btn")
        btn5.clicked.connect(partial(self._show_controller, "pregled_audit_logova"))
        nav_layout.addWidget(btn5)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        nav_layout.addWidget(spacer)

        logout_button = QPushButton("Odjava")
        logout_button.setObjectName("logout_button")
        logout_button.clicked.connect(self._handle_logout)
        nav_layout.addWidget(logout_button)

        toolbar_container = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.addWidget(nav_widget)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(toolbar_container)
        main_layout.addWidget(self.stack)
        self.setCentralWidget(main_widget)

        self._show_controller("pregled_datoteka")

    def _register_controller(self, name: str, controller):
        self.controllers[name] = controller
        self.stack.addWidget(controller.root_widget)

    def _show_controller(self, name: str):
        ctrl = self.controllers.get(name)
        if not ctrl:
            return
        
        ctrl.reset()

        index = self.stack.indexOf(ctrl.root_widget)
        if index != -1:
            self.stack.setCurrentIndex(index)

    def _check_idle(self):
        elapsed = (datetime.now() - self.last_activity).total_seconds()
        
        if elapsed >= self.INACTIVITY_TIMEOUT:
            if not self.warning_timer.isActive():
                self.warning_remaining = self.WARNING_TIME
                self.warning_timer.start(1000)
                self._show_warning_dialog()

    def _update_warning(self):
        self.warning_remaining -= 1
        
        if self.warning_remaining > 0:
            self.warning_dialog.setText(
                f"Bit ćete odjavljeni za {self.warning_remaining} sekundi zbog neaktivnosti. \n Pomaknite se ili pritisnite tipku da ostanete prijavljeni."
            )
        else:
            self.warning_timer.stop()
            self._auto_logout()

    def _show_warning_dialog(self):
        self.warning_dialog = QMessageBox(self)
        self.warning_dialog.setWindowTitle("Neaktivnost")
        self.warning_dialog.setText(
            f"Bit ćete odjavljeni za {self.WARNING_TIME} sekundi zbog neaktivnosti.\n Pomaknite se ili pritisnite tipku da ostanete prijavljeni."
        )
        self.warning_dialog.show()

    def _reset_idle(self):
        self.last_activity = datetime.now()
        
        if self.warning_timer.isActive():
            self.warning_timer.stop()
            if hasattr(self, 'warning_dialog'):
                self.warning_dialog.close()
    
    def _auto_logout(self):
        log("Automatska odjava zbog neaktivnosti")
        FileCleanupManager.cleanup_on_logout()
        key_manager.clear_kek()
        key_manager.clear_pdk()
        
        if hasattr(self, 'warning_dialog'):
            self.warning_dialog.close()
        self.logout_requested.emit()

    def _handle_logout(self):
        log("Korisnik se odjavio")
        FileCleanupManager.cleanup_on_logout()
        key_manager.clear_kek()
        key_manager.clear_pdk()
        
        if self.idle_timer.isActive():
            self.idle_timer.stop()
        if self.warning_timer.isActive():
            self.warning_timer.stop()
        
        if hasattr(self, 'warning_dialog'):
            self.warning_dialog.close()
        self.logout_requested.emit()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frame_gm.moveCenter(screen)
        self.move(frame_gm.topLeft())

    def closeEvent(self, event):

        log("Korisnik je zatvorio aplikaciju.")
        FileCleanupManager.cleanup_on_logout()
        key_manager.clear_kek()
        key_manager.clear_pdk()
        event.accept()