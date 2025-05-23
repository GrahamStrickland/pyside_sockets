from PySide6.QtCore import QObject
from PySide6.QtNetwork import QHostAddress
from PySide6.QtWidgets import QMainWindow, QTextEdit

from .request_client import RequestClient
from .update_client import UpdateClient


class Window(QMainWindow):
    _msg_display: QTextEdit
    _req_client: RequestClient
    _upd_client: UpdateClient

    _req_addr = QHostAddress(r"127.0.0.1")
    _upd_addr = QHostAddress(r"127.0.0.1")
    _req_port = 37679
    _upd_port = 37680

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.setFixedWidth(640)
        self.setFixedHeight(480)

        self._msg_display = QTextEdit(self)
        self._msg_display.setPlainText("")
        self._msg_display.setReadOnly(True)
        self.setCentralWidget(self._msg_display)

        self._req_client = RequestClient(
            address=self._req_addr, port=self._req_port, parent=self
        )
        self._req_client.errsig.connect(self.display_err)
        self._req_client.msgsig.connect(self.display_msg)

        self._upd_client = UpdateClient(
            address=self._upd_addr, port=self._upd_port, parent=self
        )
        self._upd_client.errsig.connect(self.display_err)
        self._upd_client.msgsig.connect(self.display_msg)

    def display_msg(self, msg: str) -> None:
        self._msg_display.setPlainText(msg)

    def display_err(self, msg: str) -> None:
        self._msg_display.setPlainText("ERR: " + msg)
