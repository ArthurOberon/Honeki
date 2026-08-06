from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFrame, QDialog
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QShortcut, QKeySequence
from functools import partial

class ReviewWindow(QWidget):
	
    def __init__(self, go_to_menu_callback, engine):
        super().__init__()

        self.engine = engine

        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)

        self.go_to_menu_callback = go_to_menu_callback

        self.init_top_layout()
        layout.addLayout(self.top_layout)

        layout.addSpacing(25)

        self.init_center_layout()
        layout.addLayout(self.center_layout)

        layout.addStretch(1)

        self.init_bottom_layout()
        layout.addLayout(self.bottom_layout)

        self.setLayout(layout)


        self.snackbar = QLabel("SNACKBAR")
        self.snackbar.setObjectName("snackbar")
        self.snackbar.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.snackbar.move(0, 650)

        self.set_answer_revealed(False)


    def init_top_layout(self):
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)

        self.btn_back = QPushButton("<-")
        self.btn_back.setObjectName("btn_back")
        self.btn_back.setProperty("top_btn", True)
        self.btn_back.setShortcut("Escape")
        self.btn_back.clicked.connect(self.on_quit_clicked)
        self.btn_back.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.btn_undo = QPushButton("UNDO")
        self.btn_undo.setProperty("top_btn", True)
        self.btn_undo.setShortcut("Ctrl+Z")
        self.btn_undo.clicked.connect(self.on_undo_clicked)
        self.btn_undo.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.btn_redo = QPushButton("REDO")
        self.btn_redo.setProperty("top_btn", True)
        self.btn_redo.setShortcut("Ctrl+Y")
        self.btn_redo.clicked.connect(self.on_redo_clicked)
        self.btn_redo.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        top_layout.addWidget(self.btn_back)
        top_layout.addWidget(self.btn_undo, stretch=1)
        top_layout.addWidget(self.btn_redo, stretch=1)

        self.top_layout = top_layout


    def init_center_layout(self):
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

        self.center_layout = center_layout


    def init_bottom_layout(self):
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)

        self.btn_show_answer = QPushButton("Show Back")
        self.btn_show_answer.setObjectName("btn_show_answer")
        self.btn_show_answer.setShortcut("Space")
        self.btn_show_answer.clicked.connect(self._on_show_answer_clicked)
        self.btn_show_answer.setFocus()

        self.btn_no = QPushButton("NO : <1m")
        self.btn_no.setObjectName("btn_no")
        self.btn_no.setToolTip("Keyboard: 1")
        self.btn_no.setShortcut(Qt.Key.Key_1)
        self.btn_no.clicked.connect(partial(self.on_answer_clicked, False))
        self.btn_no.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.btn_yes = QPushButton("YES")
        self.btn_yes.setObjectName("btn_yes")
        self.btn_yes.setToolTip("Keyboard: 2")
        self.btn_yes.clicked.connect(partial(self.on_answer_clicked, True))
        self.btn_yes.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.shortcut_btn_yes = QShortcut(QKeySequence(Qt.Key.Key_2), self.btn_yes)
        self.shortcut_btn_yes.activated.connect(self.btn_yes.animateClick)

        bottom_layout.addWidget(self.btn_show_answer)
        bottom_layout.addWidget(self.btn_no, stretch=1)
        bottom_layout.addWidget(self.btn_yes, stretch=1)

        self.bottom_layout = bottom_layout


	# ====================================================================================

    def show_snackbar(self, text):
        self.snackbar.setText(text)
        self.snackbar.show()
        QTimer.singleShot(2000, self.snackbar.hide)


    def set_answer_revealed(self, revealed: bool):
        self.label_front.setVisible(True)

        self.separator.setVisible(revealed)
        self.label_back.setVisible(revealed)
        self.btn_no.setVisible(revealed)
        self.btn_yes.setVisible(revealed)

        self.btn_show_answer.setVisible(not revealed)


    def _on_show_answer_clicked(self):
        self.set_answer_revealed(True)
 
    def on_quit_clicked(self):
        self.go_to_menu_callback()

    def on_undo_clicked(self):
        if not self.engine.undo():
            self.show_snackbar("Nothing to undo.")
        else:
            self.show_snackbar("Undo card.")
            self.load_one_card_to_review_on_window()

    def on_redo_clicked(self):
        if not self.engine.redo():
            self.show_snackbar("Nothing to redo.")
        else :
            self.show_snackbar("Redo card.")
            self.load_one_card_to_review_on_window()

    def on_answer_clicked(self, answer):
        print("in: on_answer_clicked -> call : self.engine.answer_card_review")
        self.engine.answer_card_review(self.card.id, answer)

        print(f"Answer : {answer}")
        print("in: on_answer_clicked -> call : load_one_card_to_review_on_window")
        self.load_one_card_to_review_on_window()


    def load_one_card_to_review_on_window(self):
        self.card = self.engine.get_next_card()
        
        self.label_front.setText(f"{self.card.name}")
        self.label_back.setText(f"{self.card.picture}\n{self.card.placed_in}\n{self.card.connect_to}")

        self.set_answer_revealed(False)

        timer = self.engine.get_string_formated_next_good_interval(self.card)
        self.btn_yes.setText(f"YES : {timer}")
