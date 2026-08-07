from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFrame, QDialog
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QShortcut, QKeySequence, QPixmap, QMovie
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
        center_layout.setSpacing(20)

        self.label_front = QLabel("FRONT")
        self.label_front.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_front.setObjectName("label_front")

        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setObjectName("separator")

        center_layout.addWidget(self.label_front)
        center_layout.addWidget(self.separator, alignment=Qt.AlignmentFlag.AlignCenter)

        self.init_back_card_layout()

        center_layout.addLayout(self.back_layout, stretch=1)

        self.center_layout = center_layout

    def create_back_card_block(self, title_text):
        card_frame = QFrame()
        card_frame.setProperty("class", "back_card_block")


        layout = QVBoxLayout(card_frame)
        layout.setSpacing(6)
        # layout.setContentsMargins(32, 24, 32, 24)
        layout.setContentsMargins(16, 16, 16, 16)
        # layout.setContentsMargins(16, 12, 16, 12)

        title_label = QLabel(title_text)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setProperty("class", "back_card_block_title")

        value_label = QLabel()
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setProperty("class", "back_card_block_value")

        if title_text :
            layout.addWidget(title_label)
        layout.addWidget(value_label, alignment=Qt.AlignmentFlag.AlignCenter)

        return card_frame, value_label

    def init_back_card_layout(self):
        self.back_layout = QVBoxLayout()

        self.back_layout.setSpacing(0)
        self.back_layout.setContentsMargins(20, 10, 20, 10)

        self.block_placed_in_frame, self.val_placed_in_label = self.create_back_card_block("PLACED IN")
        self.block_connect_to_frame, self.val_connect_to_label = self.create_back_card_block("PLACED IN")
        self.block_picture_frame, self.val_picture_label = self.create_back_card_block("")

        self.val_picture_label.setMaximumHeight(300)
        self.val_picture_label.setMaximumWidth(600)
        # self.val_picture_label.setScaledContents(False)

        self.back_layout.addWidget(self.block_placed_in_frame)
        self.back_layout.addSpacing(10)
        self.back_layout.addWidget(self.block_connect_to_frame)
        self.back_layout.addSpacing(10)
        self.back_layout.addWidget(self.block_picture_frame)


    def set_back_layout_visibile(self, revealed):
        self.block_placed_in_frame.setVisible(revealed)
        self.block_connect_to_frame.setVisible(revealed)
        self.block_picture_frame.setVisible(revealed)


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
        self.set_back_layout_visibile(revealed)
        self.btn_no.setVisible(revealed)
        self.btn_yes.setVisible(revealed)

        self.btn_show_answer.setVisible(not revealed)


    def _on_show_answer_clicked(self):
        self.set_answer_revealed(True)
 
    def on_quit_clicked(self):
        if hasattr(self, 'movie') and self.movie:
            self.movie.stop()
            self.movie = None
        self.val_picture_label.clear()

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
        if hasattr(self, 'movie') and self.movie:
            self.movie.stop()
            self.movie = None
        self.val_picture_label.clear()

        self.engine.answer_card_review(self.card.id, answer)
        self.load_one_card_to_review_on_window()


    def load_one_card_to_review_on_window(self):
        self.card = self.engine.get_next_card()
        
        self.label_front.setText(f"{self.card.name}")


        self.val_placed_in_label.setText(self.card.placed_in)
        
        if isinstance(self.card.connect_to, list):
            self.val_connect_to_label.setText(" • ".join(self.card.connect_to))
        else:
            self.val_connect_to_label.setText(str(self.card.connect_to))


        if self.card.picture and self.card.picture != "null":
            pixmap = QPixmap(self.card.picture)

            if not pixmap.isNull():

                if self.card.picture.lower().endswith(".gif"):
                    self.movie = QMovie(self.card.picture)

                    self.movie.setScaledSize(QSize(300, 300))
                    
                    self.val_picture_label.setText("")
                    self.val_picture_label.setMovie(self.movie)
                    self.movie.start()
                else:
                    scaled_pixmap = pixmap.scaled(
                        600, 300,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
    
                    self.val_picture_label.setText("")
                    self.val_picture_label.setPixmap(scaled_pixmap)
            else:
                self.val_picture_label.setText("No Picture")

            self.block_picture_frame.show()
        else:

            self.block_picture_frame.hide()



        self.set_answer_revealed(False)

        timer = self.engine.get_string_formated_next_good_interval(self.card)
        self.btn_yes.setText(f"YES : {timer}")
