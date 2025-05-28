from random import random
from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QHostAddress

from .request_client import RequestClient


def pi_approx(n: int) -> float:
    pi = 1.0
    for i in range(1, n):
        sign = -1 if i % 2 != 0 else 1
        pi += sign * (1 / (2 * i + 1))
    return 4.0 * pi


class RequestManager(QObject):
    _req_client: RequestClient
    _req_addr = QHostAddress(r"127.0.0.1")
    _req_port = 37679
    _started: bool

    errsig = Signal(str)
    msgsig = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._started = False

    def do_work(self) -> None:
        self._req_client = RequestClient(address=self._req_addr, port=self._req_port)
        self._req_client.errsig.connect(self.display_err)
        self._req_client.msgsig.connect(self.display_msg)
        self.display_msg("Request thread started...")
        self._started = True

        for num in range(1, 5):
            pi_approx(int(random() * 10**(5 - num)))
            msgs = self._req_client.make_req(f"Hello! #{num}")
            self.msgsig.emit("".join(msgs))

    def display_msg(self, msg: str) -> None:
        self.msgsig.emit(f"{msg} from Request Manager")

    def display_err(self, msg: str) -> None:
        self.errsig.emit(f"ERR: {msg} from Request Manager")

    def quit(self) -> None:
        if self._started:
            self._req_client.quit()
