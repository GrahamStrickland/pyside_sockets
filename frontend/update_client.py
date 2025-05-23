from PySide6.QtCore import QObject
from PySide6.QtNetwork import QHostAddress

from .client_base import ClientBase


class UpdateClient(ClientBase):
    def __init__(
        self, address: QHostAddress, port: int, parent: QObject | None = None
    ) -> None:
        super().__init__(address=address, port=port, parent=parent)
