import sys

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication

from frontend.window import Window
from frontend.worker_object import WorkerObject


def main() -> None:
    app = QApplication(sys.argv)

    window = Window()
    worker_thread = QThread()
    worker_object = WorkerObject()
    worker_object.moveToThread(worker_thread)
    worker_thread.finished.connect(worker_object.deleteLater)
    app.aboutToQuit.connect(worker_thread.quit)

    worker_object.msgsig.connect(window.display_msg)
    worker_object.errsig.connect(window.display_msg)

    window.show()
    window.startsig.connect(worker_object.do_work)
    worker_thread.start()

    app.exec()


if __name__ == "__main__":
    main()
