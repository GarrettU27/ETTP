from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


class MainButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.set_main_button_style()

    def set_main_button_style(self):
        self.setStyleSheet("""
                    QPushButton {
                        font-family: "Encode Sans";
                        font-weight: 400;
                        font-size: 40px;
                        line-height: 150%;
                        text-align: center;
                        color: #FFFFFF;
                        background: #074EE8;
                        padding: 0.4em;
                        border-radius: 25%;
                        margin-bottom: 30px;
                    }

                    QPushButton:hover {
                        background: #063eb7;
                    }
                """)