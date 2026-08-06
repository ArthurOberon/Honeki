from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class MenuWindow(QWidget):
    def __init__(self, go_to_review_callback, go_to_setting_callback, engine):
        super().__init__()

        self.engine = engine

        layout = QVBoxLayout()

        # Setting button
        self.btn_setting = QPushButton()
        self.btn_setting.setObjectName("btn_setting")

        # Icon made by Rahul Kaklotar
        self.btn_setting.setIcon(QIcon("gui/assets/setting_icon.png"))
        self.btn_setting.setIconSize(QSize(40, 40))
        self.btn_setting.setToolTip("Setting")
        self.btn_setting.clicked.connect(go_to_setting_callback)
        self.btn_setting.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_setting.setShortcut("P")

        layout.addWidget(self.btn_setting, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addSpacing(10)

        # Title
        title = QLabel("Menu - Main Page")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Stat Info
        stat_layout = QHBoxLayout()
        stat_layout.setSpacing(30)

        self.label_new = QLabel("New: 0")
        self.label_new.setObjectName("label_new")

        self.label_error = QLabel("Error: 0")
        self.label_error.setObjectName("label_error")

        self.label_review = QLabel("Review: 0")
        self.label_review.setObjectName("label_review")

        stat_layout.addWidget(self.label_new)
        stat_layout.addWidget(self.label_error)
        stat_layout.addWidget(self.label_review)

        stat_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stat_layout.setContentsMargins(0, 0, 0, 90)


        btn = QPushButton("Start Today Session")
        btn.setObjectName("btn_start")
        btn.clicked.connect(go_to_review_callback)
        btn.setFocus()

        layout.addWidget(title)
        layout.addLayout(stat_layout)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)

    def update_state_layout(self):
        stats = self.engine.get_data() # for label new, error, review

        self.label_new.setText(f"New: {stats.new}")
        self.label_error.setText(f"Error: {stats.error}")
        self.label_review.setText(f"Review: {stats.review}")