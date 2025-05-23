from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtNetwork import QHostAddress

from .request_client import RequestClient
from .update_client import UpdateClient


class WorkerThread(QThread):
    _req_client: RequestClient
    _upd_client: UpdateClient

    _req_addr = QHostAddress(r"127.0.0.1")
    _upd_addr = QHostAddress(r"127.0.0.1")
    _req_port = 37679
    _upd_port = 37680

    errsig = Signal(str)
    msgsig = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    def run(self) -> None:
        self._req_client = RequestClient(address=self._req_addr, port=self._req_port)
        self._req_client.errsig.connect(self.display_err)
        self._req_client.msgsig.connect(self.display_msg)

        self._upd_client = UpdateClient(address=self._upd_addr, port=self._upd_port)
        self._upd_client.errsig.connect(self.display_err)
        self._upd_client.msgsig.connect(self.display_msg)

        for num in range(2):
            self._req_client.morning(num)

        return super().run()

    def display_msg(self, msg: str) -> None:
        self.msgsig.emit(
            msg + ", from " + ", from " + self._get_sender_name(self.sender())
        )

    def display_err(self, msg: str) -> None:
        self.errsig.emit(
            "ERR: " + msg + ", from " + self._get_sender_name(self.sender())
        )

    def _get_sender_name(self, sender: QObject) -> str:
        if sender == self._req_client:
            return f"Request Socket, address {self._req_addr.toString()}, port {self._req_port}"
        elif sender == self._req_client:
            return f"Update Socket, address {self._upd_addr.toString()}, port {self._upd_port}"
        else:
            return "Unknown"
