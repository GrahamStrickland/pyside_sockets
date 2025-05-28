from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QHostAddress

from .update_client import UpdateClient


class UpdateManager(QObject):
    _upd_client: UpdateClient
    _upd_addr = QHostAddress(r"127.0.0.1")
    _upd_port = 37680
    _started: bool

    errsig = Signal(str)
    msgsig = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._started = False

    def do_work(self) -> None:
        self._upd_client = UpdateClient(address=self._upd_addr, port=self._upd_port)
        self._upd_client.errsig.connect(self.display_err)
        self._upd_client.msgsig.connect(self.display_msg)
        self.display_msg("Update thread started...")
        self._started = True

        while True: 
            msgs = self._upd_client.recv()
            if len(msg := "".join(msgs)) > 0:
                self.display_msg(msg)
                self._upd_client.send("Thanks!")

    def display_msg(self, msg: str) -> None:
        self.msgsig.emit(f"{msg} from Update Manager")

    def display_err(self, msg: str) -> None:
        self.errsig.emit(f"ERR: {msg} from Update Manager")

    def quit(self) -> None:
        if self._started:
            self._upd_client.quit()
