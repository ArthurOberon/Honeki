from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, QFileSystemWatcher
from windows.main_window import MainWindow

import sys
import os
import glob

# --------------------------------------------------------
# For in case watcher not working because working on Windows

def get_qss_files(qss_dir):
    return glob.glob(os.path.join(qss_dir, "*.qss"))

def load_combined_stylesheets(app, qss_dir):
    combined_css = ""

    for file_path in get_qss_files(qss_dir):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                combined_css += f.read() + '\n'
        except OSError:
            pass

    app.setStyleSheet(combined_css)

def getmtimes(qss_dir):
    return {f: os.path.getmtime(f) for f in get_qss_files(qss_dir) if os.path.exists(f)}

def setup_qss_watcher(app):

    qss_dir = os.path.abspath("gui/qss/")
    load_combined_stylesheets(app, qss_dir)
    last_mtime = [getmtimes(qss_dir)]

    def check_qss_update():
        try:
            current_mtime = getmtimes(qss_dir)
            if current_mtime != last_mtime[0]:
                last_mtime[0] = current_mtime
                load_combined_stylesheets(app, qss_dir)
        except OSError:
            pass

    app.css_timer = QTimer()
    app.css_timer.timeout.connect(check_qss_update)
    app.css_timer.start(500)

# --------------------------------------------------------------------------------------

class QSSManager:
    def __init__(self, app):
        self.app = app
        self.path = "gui/qss/"
        self.qss_files = glob.glob(f"{self.path}*.qss")

        self.watcher = QFileSystemWatcher(self.qss_files)

        self.watcher.fileChanged.connect(self.reload_styles)

        self.reload_styles()

    def reload_styles(self):
        combined_css = ""

        for file_path in self.qss_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    combined_css += f.read() + '\n'
            except OSError:
                pass
    
        self.app.setStyleSheet(combined_css)


def main():

    app = QApplication(sys.argv)

    setup_qss_watcher(app)

    # app.qss_manager = QSSManager(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
