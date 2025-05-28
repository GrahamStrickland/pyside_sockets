import sys

import pydevd
from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QApplication

from frontend.window import Window
from frontend.request_manager import RequestManager
from frontend.update_manager import UpdateManager


pydevd.connected = True
pydevd.settrace(suspend=False)


class PySideSockets(QObject):
    request_manager: RequestManager
    request_thread: QThread

    update_manager: UpdateManager
    update_thread: QThread

    quitsig = Signal()

    def __init__(self, window: Window, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.moveToThread(QThread.currentThread())

        self.request_thread = QThread()
        self.request_manager = RequestManager()
        self.request_manager.moveToThread(self.request_thread)
        self.request_thread.finished.connect(self.request_manager.deleteLater)
        self.request_manager.msgsig.connect(window.display_msg)
        self.request_manager.errsig.connect(window.display_msg)
        self.quitsig.connect(self.request_manager.quit)

        self.update_thread = QThread()
        self.update_manager = UpdateManager()
        self.update_manager.moveToThread(self.update_thread)
        self.update_thread.finished.connect(self.update_manager.deleteLater)
        self.update_manager.msgsig.connect(window.display_msg)
        self.update_manager.errsig.connect(window.display_msg)
        self.quitsig.connect(self.update_manager.quit)

        window.startsig.connect(self.request_manager.do_work)
        window.startsig.connect(self.update_manager.do_work)
        window.quitsig.connect(self.quit)
        self.request_thread.start()
        self.update_thread.start()

    def quit(self) -> None:
        self.quitsig.emit()

        self.request_thread.quit()
        self.request_thread.wait()

        self.update_thread.quit()
        self.update_thread.wait()


def main() -> None:
    app = QApplication(sys.argv)

    window = Window()
    sockets = PySideSockets(window)
    app.aboutToQuit.connect(sockets.quit)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
