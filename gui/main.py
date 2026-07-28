from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QHBoxLayout, QFrame
from PySide6.QtCore import Qt

import sys
import anki_engine

def hello():
    print("Hello !")

class MenuWindow(QWidget):
    def __init__(self, go_to_review_callback):
        super().__init__()

        layout = QVBoxLayout()

        # Title
        title = QLabel("Menu - Main Page")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        title.setContentsMargins(30, 100, 30, 20)

        # Stat Info
        stat_layout = QHBoxLayout()
        stat_layout.setSpacing(30)

        self.label_new = QLabel("New: 20")
        self.label_new.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9;")

        self.label_error = QLabel("Error: 7")
        self.label_error.setStyleSheet("font-size: 18px; font-weight: bold; color: #e74c3c;")

        self.label_review = QLabel("Review: 63")
        self.label_review.setStyleSheet("font-size: 18px; font-weight: bold; color: #27ae60;")

        stat_layout.addWidget(self.label_new)
        stat_layout.addWidget(self.label_error)
        stat_layout.addWidget(self.label_review)

        stat_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stat_layout.setContentsMargins(0, 0, 0, 90)


        # Bouton
        btn = QPushButton("Start Today Session")
        btn.setFixedHeight(45)
        btn.setFixedWidth(450)
        btn.setStyleSheet("font-size: 16px; background-color: #3498db; color: white;")

        btn.clicked.connect(go_to_review_callback)


        # Layout Widgets
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
        top_layout.setSpacing(10)

        self.btn_back = QPushButton("<-")
        self.btn_back.setFixedWidth(60)

        self.btn_undo = QPushButton("UNDO")
        self.btn_redo = QPushButton("REDO")

        # top_btn_style = """
        #     QPushButton {
        #     border: 2px solid #7c5cbf;
        #     border-radius: 8px;
        #     padding: 10px;
        #     font-weight: bold;
        #     color: #7c5cbf;
        #     font-size: 14px;
        #     }
        # """

        top_btn_style = """
            QPushButton {
				background-color: #7c5cbf;
                color: white;
				height: 25;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: normal;
                font-size: 13px;
            }
        """

        self.btn_back.setStyleSheet(top_btn_style)
        self.btn_undo.setStyleSheet(top_btn_style)
        self.btn_redo.setStyleSheet(top_btn_style)

        self.btn_back.clicked.connect(go_to_menu_callback)


        top_layout.addWidget(self.btn_back)
        top_layout.addWidget(self.btn_undo, stretch=1)
        top_layout.addWidget(self.btn_redo, stretch=1)

        layout.addLayout(top_layout)

        layout.addSpacing(25)

        center_layout = QVBoxLayout()
        center_layout.setSpacing(15)

        self.label_front = QLabel("FRONT")
        self.label_front.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_front.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #777; max-height: 2px;")
        separator.setFixedWidth(400)

        self.label_back = QLabel("BACK")
        self.label_back.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_back.setStyleSheet("font-size: 24px; color: #444;")

        center_layout.addWidget(self.label_front)
        center_layout.addWidget(separator, alignment=Qt.AlignmentFlag.AlignCenter)
        center_layout.addWidget(self.label_back, stretch=1)

        layout.addLayout(center_layout)

        layout.addStretch(1)


        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)

        self.btn_no = QPushButton("NO")
        self.btn_no.setFixedHeight(50)
        # self.btn_no.setStyleSheet("""
        #     QPushButton {
        #         border: 2px solid #e74c3c;
        #         border-radius: 8px;
        #         color: #e74c3c;
        #         font-weight: bold;
        #         font-size: 16px;
        #     }
        # """)
        self.btn_no.setStyleSheet("""
            QPushButton {
				background-color: #e74c3c;
				color: white;
                border: none;
                border-bottom-right-radius: 12	px;
                font-size: 13px;
                font-weight: normal;
            }
        """)

        self.btn_yes = QPushButton("YES")
        self.btn_yes.setFixedHeight(50)
        # self.btn_yes.setStyleSheet("""
        #     QPushButton {
        #         border: 2px solid #3498db;
        #         border-radius: 8px;
        #         color: #3498db;
        #         font-weight: bold;
        #         font-size: 16px;
        #     }
        # """)

        self.btn_yes.setStyleSheet("""
            QPushButton {
				background-color: #3498db;
				color: white;
				border: none;
				border-bottom-right-radius: 12	px;
				font-size: 13px;
				font-weight: normal;
            }
        """)


        bottom_layout.addWidget(self.btn_no, stretch=1)
        bottom_layout.addWidget(self.btn_yes, stretch=1)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)


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

def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()