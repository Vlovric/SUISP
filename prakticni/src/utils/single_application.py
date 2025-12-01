from PySide6.QtWidgets import QApplication
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtCore import Signal


class SingleApplication(QApplication):
    activateRequested = Signal()

    def __init__(self, argv, app_id):
        super().__init__(argv)
        self.app_id = app_id
        self.socket = QLocalSocket()
        self.socket.connectToServer(self.app_id)

        if self.socket.waitForConnected(500):

            try:
                if self.socket.state() == QLocalSocket.ConnectedState:
                    self.socket.write(b"ACTIVATE")
                    self.socket.flush()
            except Exception:
                pass
            finally:
                self.socket.close()

            self.is_running = True
            return
        
        self.is_running = False
        self.socket.close()
        self._server = QLocalServer(self)

        self._server.removeServer(self.app_id)
        if not self._server.listen(self.app_id):
            raise RuntimeError(f"Unable to start the server: {self._server.errorString()}")

        self._server.newConnection.connect(self._handle_new_connection)

    def _handle_new_connection(self):
        socket = self._server.nextPendingConnection()
        try:
            _ = socket.readAll()
            self.activateRequested.emit()

        finally:
            socket.close()