from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, QTimer

import sys
import os
import anki_engine

def hello():
    print("Hello !")

class MenuWindow(QWidget):
    def __init__(self, go_to_review_callback):
        super().__init__()

        layout = QVBoxLayout()

        # Title
        title = QLabel("Menu - Main Page")
        title.setObjectName("title")
        # title.setStyleSheet("font-size: 22px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        # title.setContentsMargins(30, 100, 30, 20)

        # Stat Info
        stat_layout = QHBoxLayout()
        stat_layout.setSpacing(30)

        self.label_new = QLabel("New: 20")
        self.label_new.setObjectName("label_new")

        self.label_error = QLabel("Error: 7")
        self.label_error.setObjectName("label_error")

        self.label_review = QLabel("Review: 63")
        self.label_review.setObjectName("label_review")

        stat_layout.addWidget(self.label_new)
        stat_layout.addWidget(self.label_error)
        stat_layout.addWidget(self.label_review)

        stat_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stat_layout.setContentsMargins(0, 0, 0, 90)


        btn = QPushButton("Start Today Session")
        btn.setObjectName("btn_start")


        btn.clicked.connect(go_to_review_callback)


        layout.addWidget(title)
        layout.addLayout(stat_layout)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)

class ReviewWindow(QWidget):
    def __init__(self, go_to_menu_callback):
        super().__init__()

        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)

        self.btn_back = QPushButton("<-")
        self.btn_back.setObjectName("btn_back")

        self.btn_undo = QPushButton("UNDO")
        self.btn_redo = QPushButton("REDO")

        self.btn_back.setProperty("top_btn", True)
        self.btn_undo.setProperty("top_btn", True)
        self.btn_redo.setProperty("top_btn", True)

        self.btn_back.setShortcut("Escape")
        self.btn_undo.setShortcut("Ctrl+Z")
        self.btn_redo.setShortcut("Ctrl+Y")

        self.btn_back.clicked.connect(go_to_menu_callback)
        # self.btn_undo.clicked.connect()
        # self.btn_redo.clicked.connect()


        top_layout.addWidget(self.btn_back)
        top_layout.addWidget(self.btn_undo, stretch=1)
        top_layout.addWidget(self.btn_redo, stretch=1)

        layout.addLayout(top_layout)

        layout.addSpacing(25)

        center_layout = QVBoxLayout()
        center_layout.setSpacing(15)

        self.label_front = QLabel("FRONT")
        self.label_front.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_front.setObjectName("label_front")

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setObjectName("separator")

        self.label_back = QLabel("BACK")
        self.label_back.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_back.setObjectName("label_back")

        center_layout.addWidget(self.label_front)
        center_layout.addWidget(self.separator, alignment=Qt.AlignmentFlag.AlignCenter)
        center_layout.addWidget(self.label_back, stretch=1)

        layout.addLayout(center_layout)

        layout.addStretch(1)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)

        self.btn_show_answer = QPushButton("Show Back")
        self.btn_show_answer.setObjectName("btn_show_answer")

        self.btn_no = QPushButton("NO")
        self.btn_no.setObjectName("btn_no")

        self.btn_yes = QPushButton("YES")
        self.btn_yes.setObjectName("btn_yes")

        self.btn_show_answer.setShortcut("Space")
        self.btn_no.setShortcut("1")
        # self.btn_no.setShortcut("1")
        self.btn_yes.setShortcut("2")
        # self.btn_yes.setShortcut("1")

        self.btn_show_answer.clicked.connect(self._on_show_answer_clicked)
        self.btn_no.clicked.connect(self.load_card)
        self.btn_yes.clicked.connect(self.load_card)

        bottom_layout.addWidget(self.btn_show_answer)
        bottom_layout.addWidget(self.btn_no, stretch=1)
        bottom_layout.addWidget(self.btn_yes, stretch=1)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

        self.set_answer_revealed(False)


    def set_answer_revealed(self, revealed: bool):
        self.label_front.setVisible(True)

        self.separator.setVisible(revealed)
        self.label_back.setVisible(revealed)
        self.btn_no.setVisible(revealed)
        self.btn_yes.setVisible(revealed)

        self.btn_show_answer.setVisible(not revealed)

    def _on_show_answer_clicked(self):
        # if self.rust_backend:
            # pass

        self.set_answer_revealed(True)

    def load_card(self):
        self.set_answer_revealed(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Anki-Like GUI")
        self.resize(1200, 800)
        # self.resize(800, 600)

        # engine_status = anki_engine.status()
        # engine = anki_engine.Engine()

        # layout = QVBoxLayout()
        # label = QLabel(f"Engine Message: {engine.test}")
        # # label = QLabel(f"Engine Status: {engine_status}")
        # layout.addWidget(label)

        # container = QWidget()
        # container.setLayout(layout)
        # self.setCentralWidget(container)

        # Create stacked widget (to stack window/page)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create Instance of each window/page
        self.menu_window = MenuWindow(go_to_review_callback=self.show_review)
        self.review_window = ReviewWindow(go_to_menu_callback=self.show_menu)

        # Add page into the stacked_widget
        self.stacked_widget.addWidget(self.menu_window)
        self.stacked_widget.addWidget(self.review_window)

        self.show_menu()

    def show_menu(self):
        self.stacked_widget.setCurrentWidget(self.menu_window)

    def show_review(self):
        self.stacked_widget.setCurrentWidget(self.review_window)


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
