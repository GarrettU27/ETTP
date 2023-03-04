from PyQt6.QtWidgets import QLabel


class HeadingLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)

        font = self.font()
        font.setPixelSize(64)
        self.setFont(font)

        self.setMaximumHeight(self.sizeHint().height())

        self.setStyleSheet("""
            QLabel {
                font-family: "Encode Sans SC";
                font-weight: 400;
                line-height: 150%;
                height: auto;
            }
        """)