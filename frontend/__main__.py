import sys

from PySide6.QtWidgets import QApplication

from frontend.window import Window


def main() -> None:
    app = QApplication(sys.argv)
    window = Window()
    window.display_msg("".join(sys.argv))
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
