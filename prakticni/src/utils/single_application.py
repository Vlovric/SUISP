from PySide6.QtWidgets import QApplication
from PySide6.QtNetwork import QLocalServer, QLocalSocket


class SingleApplication(QApplication):
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
        
        else:
            self.is_running = False
            self.socket.close()
            self._server = QLocalServer(self)

            self._server.removeServer(self.app_id)
            if not self._server.listen(self.app_id):
                raise RuntimeError(f"Unable to start the server: {self._server.errorString()}")

            self._server.newConnection.connect(self._handle_new_connection)

    def _handle_new_connection(self):
        new_socket = self._server.nextPendingConnection()
        try:
            window = self.activeWindow()
            if window:
                    window.show()
                    window.raise_()
                    window.activateWindow()
        finally:
            new_socket.close()