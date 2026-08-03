from PySide6.QtWidgets import QMainWindow, QStackedWidget

from .menu_window import MenuWindow
from .review_window import ReviewWindow
from .no_review_window import NoReviewWindow
from .setting_window import SettingWindow

import anki_engine

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

        self.engine = anki_engine.Engine()

        # Create stacked widget (to stack window/page)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create Instance of each window/page
        self.menu_window = MenuWindow(go_to_review_callback=self.show_review, go_to_setting_callback=self.show_setting, engine=self.engine)
        self.review_window = ReviewWindow(go_to_menu_callback=self.show_menu, engine=self.engine)
        self.no_review_window = NoReviewWindow(go_to_menu_callback=self.show_menu)
        self.setting_window = SettingWindow(go_to_menu_callback=self.show_menu)

        # Add page into the stacked_widget
        self.stacked_widget.addWidget(self.menu_window)
        self.stacked_widget.addWidget(self.review_window)
        self.stacked_widget.addWidget(self.no_review_window)
        self.stacked_widget.addWidget(self.setting_window)

        self.c = 0

        self.show_menu()

    def show_menu(self):
        self.stacked_widget.setCurrentWidget(self.menu_window)

    def show_review(self):

        if self.c <= 5: # self.engine.is_session_empty() # for loop on session until no card
            # self.review_window.load_review_one_card_window()
            self.review_window.load_one_card_to_review_on_window(self.c)
            self.stacked_widget.setCurrentWidget(self.review_window)
            self.c += 1
        else:
            self.stacked_widget.setCurrentWidget(self.no_review_window)

    def show_setting(self):
        self.stacked_widget.setCurrentWidget(self.setting_window)
