from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow, QTextEdit


class Window(QMainWindow):
    _msg_display: QTextEdit

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("PySide6 Sockets")

        self.setFixedWidth(640)
        self.setFixedHeight(480)

        self._msg_display = QTextEdit(self)
        self._msg_display.setPlainText("Starting main window...")
        self._msg_display.setReadOnly(True)
        self.setCentralWidget(self._msg_display)

    def display_msg(self, msg: str) -> None:
        self._msg_display.setPlainText(self._msg_display.toPlainText() + '\n' + msg)

