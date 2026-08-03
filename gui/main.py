from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from windows.main_window import MainWindow

import sys
import os

def load_stylesheet(app, qss_path):
    with open(qss_path, "r") as file:
        app.setStyleSheet(file.read())

def main():

    app = QApplication(sys.argv)

    file_css = os.path.abspath("gui/style.qss")

    load_stylesheet(app, file_css)

    last_mtime = [os.path.getmtime(file_css)]

    def check_css_update():
        try:
            current_mtime = os.path.getmtime(file_css)
            if current_mtime != last_mtime[0]:
                last_mtime[0] = current_mtime
                load_stylesheet(app, file_css)
        except OSError:
            pass

    app.css_timer = QTimer()
    app.css_timer.timeout.connect(check_css_update)
    app.css_timer.start(500)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
