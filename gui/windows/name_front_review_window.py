from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import Qt
from .base_review import BaseReviewWindow

class NameFrontReviewWindow(BaseReviewWindow):

    def init_back_card_layout(self):

        self.block_picture_frame = self.create_back_card_block("", self.val_picture_label)

        self.back_layout.setSpacing(0)
        self.back_layout.setContentsMargins(20, 10, 20, 10)

        self.back_layout.addWidget(self.block_placed_in_frame)
        self.back_layout.addSpacing(10)
        self.back_layout.addWidget(self.block_connect_to_frame)
        self.back_layout.addSpacing(10)
        self.back_layout.addWidget(self.block_picture_frame)

    def init_center_layout(self):
        center_layout = QVBoxLayout()
        center_layout.setSpacing(20)

        center_layout.addWidget(self.label_name)
        center_layout.addWidget(self.separator, alignment=Qt.AlignmentFlag.AlignCenter)

        self.init_back_card_layout()

        center_layout.addWidget(self.back_container, stretch=1)

        self.center_layout = center_layout

    def set_picture_visibility(self, is_visible: bool):
       self.block_picture_frame.setVisible(is_visible)
