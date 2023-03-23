from PyQt6.QtWidgets import QLabel


class ParagraphLabel(QLabel):
    def __init__(self, text, font_size = 20):
        super().__init__(text)

        font = self.font()
        font.setPixelSize(font_size)
        self.setFont(font)

        self.setMaximumHeight(self.sizeHint().height())

        self.setStyleSheet("""
            QLabel {
                font-family: "Encode Sans";
                font-weight: 400;
                line-height: 150%;
                height: auto;
            }
        """)