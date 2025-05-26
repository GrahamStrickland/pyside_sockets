import sys

import pydevd
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication

from frontend.window import Window
from frontend.request_manager import RequestManager
from frontend.update_manager import UpdateManager


pydevd.connected = True
pydevd.settrace(suspend=False)


def main() -> None:
    app = QApplication(sys.argv)

    window = Window()

    request_thread = QThread()
    request_manager = RequestManager()
    request_manager.moveToThread(request_thread)
    request_thread.finished.connect(request_manager.deleteLater)
    request_manager.msgsig.connect(window.display_msg)
    request_manager.errsig.connect(window.display_msg)

    update_thread = QThread()
    update_manager = UpdateManager()
    update_manager.moveToThread(update_thread)
    update_thread.finished.connect(update_manager.deleteLater)
    update_manager.msgsig.connect(window.display_msg)
    update_manager.errsig.connect(window.display_msg)

    app.aboutToQuit.connect(request_thread.quit)
    app.aboutToQuit.connect(update_thread.quit)

    window.show()
    window.startsig.connect(request_manager.do_work)
    window.startsig.connect(update_manager.do_work)
    request_thread.start()
    update_thread.start()

    app.exec()


if __name__ == "__main__":
    main()
