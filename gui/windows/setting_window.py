from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QFormLayout, QSpinBox, QComboBox
from PySide6.QtCore import Qt, QTimer

import json

class SettingWindow(QWidget):
	def __init__(self, go_to_menu_callback, engine):
		super().__init__()

		self.engine = engine

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
		btn.setObjectName("btn_save_setting")
		btn.clicked.connect(self.on_save_setting)
		btn.setFocus()

		layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

		layout.addStretch()

		self.setLayout(layout)

		self.snackbar = QLabel("SNACKBAR")
		self.snackbar.setObjectName("snackbar")
		self.snackbar.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
		self.snackbar.move(0, 650)

		self.set_form_to_config()


	def show_snackbar(self, text):
		self.snackbar.setText(text)
		self.snackbar.show()
		QTimer.singleShot(2000, self.snackbar.hide)


	def set_form_to_config(self):
		json_str = self.engine.get_config_json()

		config = json.loads(json_str)

		self.new_by_day_spin.setValue(config.get("numberNewByDay", 20))
		self.lat_spin.setValue(config.get("LAT", 10))
	
		is_review_random = config.get("newRandomReview", False) 
		self.new_review_random_combo.setCurrentText(str(is_review_random))

		is_select_random = config.get("newRandomSelect", False)
		self.new_select_random_combo.setCurrentText(str(is_select_random))


	def get_json_setting_values(self):
		values = {
			"numberNewByDay": self.new_by_day_spin.value(),
			"LAT": self.lat_spin.value(),
			"newRandomReview": self.new_review_random_combo.currentText() == "True",
			"newRandomSelect": self.new_select_random_combo.currentText() == "True",
		}

		json_str = json.dumps(values)

		return json_str



	def on_save_setting(self):
		json_str = self.get_json_setting_values()

		self.engine.save_config(json_str)

		self.show_snackbar("Setting saved.")
