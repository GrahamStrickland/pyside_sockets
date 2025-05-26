from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QHostAddress

from .request_client import RequestClient


class RequestManager(QObject):
    _req_client: RequestClient
    _req_addr = QHostAddress(r"127.0.0.1")
    _req_port = 37679

    errsig = Signal(str)
    msgsig = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    def do_work(self) -> None:
        self._req_client = RequestClient(address=self._req_addr, port=self._req_port)
        self._req_client.errsig.connect(self.display_err)
        self._req_client.msgsig.connect(self.display_msg)
        self.display_msg("Request thread started...")

        for num in range(1, 11):
            msgs = self._req_client.morning(num)
            self.msgsig.emit("".join(msgs))

    def display_msg(self, msg: str) -> None:
        self.msgsig.emit(f"{msg} from Request Manager")

    def display_err(self, msg: str) -> None:
        self.errsig.emit(f"ERR: {msg} from Request Manager")
