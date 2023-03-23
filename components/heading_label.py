from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QLabel
import PyQt6


class HeadingLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)

        self.setWordWrap(True)
        self.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred, PyQt6.QtWidgets.QSizePolicy.Policy.Minimum)

        font = self.font()
        font.setPixelSize(64)
        self.setFont(font)

        self.setStyleSheet("""
            QLabel {
                font-family: "Encode Sans SC";
                font-weight: 400;
                line-height: 150%;
                height: auto;
            }
        """)

        self.adjustSize()