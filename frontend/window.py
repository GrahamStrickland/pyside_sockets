from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QMainWindow, QMenu, QTextEdit


class Window(QMainWindow):
    _msg_display: QTextEdit

    startsig = Signal()
    quitsig = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("PySide6 Sockets")

        self.setFixedWidth(640)
        self.setFixedHeight(480)

        self._msg_display = QTextEdit(self)
        self._msg_display.setPlainText("Starting main window...")
        self._msg_display.setReadOnly(True)
        self.setCentralWidget(self._msg_display)

        threads_menu = QMenu("Threads", self)
        threads_action_group = QActionGroup(threads_menu)

        start_action = QAction("Start threads", threads_menu)
        start_action.triggered.connect(self.start)
        threads_menu.addAction(start_action)
        threads_action_group.addAction(start_action)

        quit_action = QAction("Quit threads", threads_menu) 
        quit_action.triggered.connect(self.quit)
        threads_menu.addAction(quit_action)
        threads_action_group.addAction(quit_action)

        threads_action_group.setExclusive(True)
        self.menuBar().addMenu(threads_menu)

    def display_msg(self, msg: str) -> None:
        self._msg_display.setPlainText(self._msg_display.toPlainText() + '\n' + msg)

    def start(self) -> None:
        self.display_msg("Starting threads...")
        self.startsig.emit()

    def quit(self) -> None:
        self.display_msg("Shutting down threads...")
        self.quitsig.emit()
