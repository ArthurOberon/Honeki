from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt

class NoReviewWindow(QWidget):
    def __init__(self, go_to_menu_callback):
        super().__init__()

        layout = QVBoxLayout()

        layout.setSpacing(10)

        self.btn_back = QPushButton("<-")
        self.btn_back.setObjectName("btn_back_no_review")
        self.btn_back.setProperty("top_btn", True)
        self.btn_back.setShortcut("Escape")
        self.btn_back.clicked.connect(go_to_menu_callback)

        layout.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignLeft)

        title = QLabel("No Card Left To Review Today")
        title.setObjectName("title_no_review")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(100)

        layout.addWidget(title)

        layout.addStretch()

        self.setLayout(layout)
