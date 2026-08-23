from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import Qt
from .base_review import BaseReviewWindow

class PictureFrontReviewWindow(BaseReviewWindow):

    def init_back_card_layout(self):

        self.back_layout.setSpacing(0)
        self.back_layout.setContentsMargins(20, 10, 20, 10)

        self.back_layout.addWidget(self.block_name_frame)
        self.back_layout.addSpacing(10)
        self.back_layout.addWidget(self.block_placed_in_frame)
        self.back_layout.addSpacing(10)
        self.back_layout.addWidget(self.block_connect_to_frame)

    def init_center_layout(self):
        center_layout = QVBoxLayout()
        center_layout.setSpacing(20)

        center_layout.addWidget(self.val_picture_label, alignment=Qt.AlignmentFlag.AlignCenter)
        center_layout.addWidget(self.separator, alignment=Qt.AlignmentFlag.AlignCenter)

        self.init_back_card_layout()

        center_layout.addWidget(self.back_container, stretch=1)

        self.center_layout = center_layout

    def set_picture_visibility(self, is_visible: bool):
       self.val_picture_label.setVisible(is_visible)
