import os

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class arrhythmia_picture(QLabel):
    def __init__(self, filename):
        super().__init__()

        pixmap = QPixmap(filename)
        self.setPixmap(pixmap)

        self.setScaledContents(True)

        self.setMaximumWidth(145)
        self.setMaximumHeight(145)