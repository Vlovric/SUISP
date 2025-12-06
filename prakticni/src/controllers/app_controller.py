from PySide6.QtWidgets import QMainWindow, QStackedWidget, QToolBar, QMessageBox, QPushButton, QWidget, QSizePolicy
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
from src.controllers.key_rotation_controller import KeyRotationController
from src.utils.key_rotation_helper import KeyRotationHelper

class AppController(QMainWindow):
    logout_requested = Signal()  # Signal koji se emitira kad treba odjava
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure File Vault")
        self.resize(800, 600)
        self.INACTIVITY_TIMEOUT = security_policy_manager.get_policy_param("inactivity_timeout_minutes") * 60  # 15 minuta (za testiranje se može staviti kraći interval)
        self.WARNING_TIME = security_policy_manager.get_policy_param("wallet_session_timeout_minutes")  # (za testiranje se može staviti kraći interval)

        # Timer za praćenje neaktivnosti
        self.idle_timer = QTimer()
        self.idle_timer.timeout.connect(self._check_idle)
        self.idle_timer.start(1000)  # Provjera svake sekunde
        
        # Timer za countdown upozorenja
        self.warning_timer = QTimer()
        self.warning_timer.timeout.connect(self._update_warning)
        self.warning_remaining = 0
        
        # Zadnja aktivnost
        self.last_activity = datetime.now()
        
        # Activity monitor
        self.activity_monitor = ActivityMonitor()
        self.activity_monitor.activity_detected.connect(self._reset_idle)
        
        # Instaliraj event filter na cijelu aplikaciju
        QCoreApplication.instance().installEventFilter(self.activity_monitor)

        # Kreiramo toolbar za navigaciju
        nav_bar = QToolBar("Navigation")
        nav_bar.setMovable(False)
        self.addToolBar(nav_bar)

        # Kreiramo stack widget za content ekrana
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.controllers = {}

        # Pregled svih datoteka
        self._register_controller("pregled_datoteka", PregledDatotekaController())
        pregled_datoteka_action = QAction("Zaključane datoteke", self)
        pregled_datoteka_action.triggered.connect(partial(self._show_controller, "pregled_datoteka"))
        nav_bar.addAction(pregled_datoteka_action)

        # Zakljucavanje datoteka
        self._register_controller("otkljucane_datoteke", UnlockedFilesController())
        otkljucane_datoteke_action = QAction("Otključane datoteke", self)
        otkljucane_datoteke_action.triggered.connect(partial(self._show_controller, "otkljucane_datoteke"))
        nav_bar.addAction(otkljucane_datoteke_action)
        
        # Prijenos dijeljene datoteke
        self._register_controller("ucitavanje_dijeljene_datoteke", UploadSharedFileController())
        ucitavanje_dijeljene_datoteke_action = QAction("Učitavanje dijeljene datoteke", self)
        ucitavanje_dijeljene_datoteke_action.triggered.connect(partial(self._show_controller, "ucitavanje_dijeljene_datoteke"))
        nav_bar.addAction(ucitavanje_dijeljene_datoteke_action)

        # Izvoz audit logova
        self._register_controller("audit_log_export", AuditLogExportController())
        audit_log_export_action = QAction("Izvoz audit loga", self)
        audit_log_export_action.triggered.connect(partial(self._show_controller, "audit_log_export"))
        nav_bar.addAction(audit_log_export_action)

        # Pregled audit logova
        self._register_controller("audit_logs", AuditLogsController())
        audit_log_export_action = QAction("Pregled audit logova", self)
        audit_log_export_action.triggered.connect(partial(self._show_controller, "audit_logs"))
        nav_bar.addAction(audit_log_export_action)
        
        # Spacer koji gura gumb za odjavu na desnu stranu
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        nav_bar.addWidget(spacer)

        # Crveni gumb za odjavu
        logout_button = QPushButton("Odjava")
        logout_button.setProperty("class", "danger")
        logout_button.clicked.connect(self._handle_logout)
        nav_bar.addWidget(logout_button)

        self.key_rotation_controller = KeyRotationController(self)
        # Rucna rotacija kljuceva
        rotate_keys_action = QAction("Rotacija ključeva", self)
        rotate_keys_action.triggered.connect(self.key_rotation_controller.start_key_rotation)
        nav_bar.addAction(rotate_keys_action)

        # Palimo prvi controller tj. inicijalni ekran
        self._show_controller("pregled_datoteka")

        self._check_key_rotation()

    def _check_key_rotation(self):
        if KeyRotationHelper.needs_rotation():
            self.key_rotation_controller.start_key_rotation()

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
            # countdown upozorenje
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
            # automatska odjava nakon odbrojavanja
            self.warning_timer.stop()
            self._auto_logout()

    def _show_warning_dialog(self):
        # Modal dialog koji prikazuje countdown
        self.warning_dialog = QMessageBox(self)
        self.warning_dialog.setWindowTitle("Neaktivnost")
        self.warning_dialog.setText(
            f"Bit ćete odjavljeni za {self.WARNING_TIME} sekundi zbog neaktivnosti.\n Pomaknite se ili pritisnite tipku da ostanete prijavljeni."
        )
        # Ovdje nesta fali.....
        self.warning_dialog.show()

    def _reset_idle(self):
        self.last_activity = datetime.now()
        
        if self.warning_timer.isActive():
            self.warning_timer.stop()
            if hasattr(self, 'warning_dialog'):
                self.warning_dialog.close()
    
    def _auto_logout(self):
        log("Automatska odjava zbog neaktivnosti")
        key_manager.clear_kek()
        key_manager.clear_pdk()
        
        if hasattr(self, 'warning_dialog'):
            self.warning_dialog.close()
        self.logout_requested.emit()

    def _handle_logout(self):
        log("Korisnik se odjavio")
        key_manager.clear_kek()
        key_manager.clear_pdk()
        
        if self.idle_timer.isActive():
            self.idle_timer.stop()
        if self.warning_timer.isActive():
            self.warning_timer.stop()
        
        if hasattr(self, 'warning_dialog'):
            self.warning_dialog.close()
        self.logout_requested.emit()