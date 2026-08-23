from PySide6.QtWidgets import QMainWindow, QStackedWidget

from .menu_window import MenuWindow
from .name_front_review_window import TextFrontReviewWindow
from .picture_front_review_window import PictureFrontReviewWindow
from .no_review_window import NoReviewWindow
from .setting_window import SettingWindow

import anki_engine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Anki-Like GUI")
        self.resize(1200, 800)
        # self.resize(800, 600)

        self.engine = anki_engine.Engine()

        # Create stacked widget (to stack window/page)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create Instance of each window/page
        self.menu_window = MenuWindow(go_to_review_callback=self.show_review, go_to_setting_callback=self.show_setting, engine=self.engine)
        self.name_front_review_window = TextFrontReviewWindow(go_to_menu_callback=self.show_menu, engine=self.engine)
        self.picture_front_review_window = PictureFrontReviewWindow(go_to_menu_callback=self.show_menu, engine=self.engine)
        self.no_review_window = NoReviewWindow(go_to_menu_callback=self.show_menu)
        self.setting_window = SettingWindow(go_to_menu_callback=self.show_menu, engine=self.engine)

        # Add page into the stacked_widget
        self.stacked_widget.addWidget(self.menu_window)
        self.stacked_widget.addWidget(self.name_front_review_window)
        self.stacked_widget.addWidget(self.picture_front_review_window)
        self.stacked_widget.addWidget(self.no_review_window)
        self.stacked_widget.addWidget(self.setting_window)

        self.show_menu()

    def show_menu(self):
        self.menu_window.update_state_layout()
        self.stacked_widget.setCurrentWidget(self.menu_window)

    def get_current_review_window(self):
        # if mode is None:
        mode = self.engine.get_config_review_mode()

        if mode == "picture":
            return self.picture_front_review_window

        return self.name_front_review_window


    def show_review(self):
        if self.engine.is_session_empty(): # for loop on session until no card
            current_review = self.get_current_review_window()
            current_review.load_one_card_to_review_on_window()
            self.stacked_widget.setCurrentWidget(current_review)
        else:
            self.engine.clear_history()
            self.stacked_widget.setCurrentWidget(self.no_review_window)

    def show_setting(self):
        self.stacked_widget.setCurrentWidget(self.setting_window)
