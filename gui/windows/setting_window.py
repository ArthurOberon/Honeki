from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QFormLayout, QSpinBox, QComboBox
from PySide6.QtCore import Qt 

class SettingWindow(QWidget):
	def __init__(self, go_to_menu_callback):
		super().__init__()

		layout = QVBoxLayout()

		layout.setSpacing(10)

		# Button Back
		self.btn_back = QPushButton("<-")
		self.btn_back.setObjectName("btn_back_setting")
		self.btn_back.setProperty("top_btn", True)
		self.btn_back.setShortcut("Escape")
		self.btn_back.setFocusPolicy(Qt.FocusPolicy.NoFocus)
		self.btn_back.clicked.connect(go_to_menu_callback)

		layout.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		layout.addSpacing(10)

	
        # Title
		title = QLabel("Setting")
		title.setObjectName("title-setting")
		title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

		layout.addWidget(title)
		layout.addSpacing(50)


		# Form Layout
		form_container = QWidget()
		form_container.setObjectName("layout_form")

		layout_form = QFormLayout(form_container)
		layout_form.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
		layout_form.setLabelAlignment(Qt.AlignmentFlag.AlignCenter)

		self.new_by_day_spin = QSpinBox()
		self.new_by_day_spin.setRange(0, 300)
		self.new_by_day_spin.setValue(20)
		self.new_by_day_spin.setSingleStep(1)
		self.new_by_day_spin.setObjectName("spin_new_by_day")
		self.new_by_day_spin.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
		# self.new_by_day_spin.setKeyboardTracking(False)
		self.new_by_day_spin.setAccelerated(True)

		layout_form.addRow("Number of new cards by day", self.new_by_day_spin)

		self.lat_spin = QSpinBox()
		self.lat_spin.setRange(0, 300)
		self.lat_spin.setValue(20)
		self.lat_spin.setSingleStep(1)
		self.lat_spin.setSuffix("m")
		self.lat_spin.setObjectName("spin_lat")
		self.lat_spin.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
		self.new_by_day_spin.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
		# self.new_by_day_spin.setKeyboardTracking(False)
		self.new_by_day_spin.setAccelerated(True)

		layout_form.addRow("Number of new cards by day", self.lat_spin)

		self.new_review_random_combo = QComboBox()
		self.new_review_random_combo.setObjectName("combo_new_review_random")
		self.new_review_random_combo.addItems(["True", "False"])
		self.new_review_random_combo.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

		layout_form.addRow("Select new card to review randomly", self.new_review_random_combo)
		
		self.new_select_random_combo = QComboBox()
		self.new_select_random_combo.setObjectName("combo_new_select_random")
		self.new_select_random_combo.addItems(["True", "False"])
		self.new_select_random_combo.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

		layout_form.addRow("Select new card to review randomly", self.new_select_random_combo)

		layout_form.setVerticalSpacing(40)
		layout_form.setHorizontalSpacing(40)

		layout.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignCenter)
		layout.addSpacing(20)

		btn = QPushButton("Save")
		btn.setObjectName("btn_start")
		btn.setFocus()

		layout.addWidget(btn)

		layout.addStretch()

		self.setLayout(layout)
