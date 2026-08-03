from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt

class SettingWindow(QWidget):
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

		layout.addStretch()

		self.setLayout(layout)
