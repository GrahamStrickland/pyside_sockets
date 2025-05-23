from PySide6.QtCore import QObject
from PySide6.QtNetwork import QHostAddress

from .client_base import ClientBase


class RequestClient(ClientBase):
    def __init__(
        self, address: QHostAddress, port: int, parent: QObject | None = None
    ) -> None:
        super().__init__(address=address, port=port, parent=parent)

    def morning(self, num: int) -> str:
        return self._make_req(f"'Morning!' #{num}")

    def _make_req(self, message: str) -> str:
        self.send(message)
        return self.recv()
