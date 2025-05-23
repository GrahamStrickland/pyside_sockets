import sys

from PySide6.QtWidgets import QApplication

from frontend.window import Window
from frontend.worker_thread import WorkerThread


def main() -> None:
    app = QApplication(sys.argv)
    worker_thread = WorkerThread()
    app.aboutToQuit.connect(worker_thread.quit)

    window = Window()
    worker_thread.msgsig.connect(window.display_msg)
    worker_thread.errsig.connect(window.display_msg)
    window.display_msg("Starting thread...")

    window.show()
    worker_thread.start()

    app.exec()


if __name__ == "__main__":
    main()
