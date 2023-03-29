from PyQt6 import QtCore
from PyQt6.QtWidgets import QLabel


class ParagraphLabel(QLabel):
    def __init__(self, text, font_size=20):
        super().__init__(text)

        self.set_font_size(font_size)

        self.setWordWrap(True)

        self.setStyleSheet("""
            QLabel {
                font-family: "Encode Sans";
                font-weight: 400;
                line-height: 150%;
                height: auto;
            }
        """)

    def set_font_size(self, font_size):
        font = self.font()
        font.setPixelSize(font_size)
        self.setFont(font)

    # fix sizing on wordwrap https://forum.qt.io/topic/127467/how-to-get-required-height-for-a-qlabel-without-showing-the-label/7?lang=en-US
    def sizeHint(self) -> QtCore.QSize:
        self.show()
        return self.rect().size()
