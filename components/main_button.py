from PyQt6 import QtCore
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QPushButton


class MainButton(QPushButton):
    font_size: int
    status = 0

    def __init__(self, text, font_size=40):
        super().__init__(text)
        self.set_font_size(font_size)
        self.set_main_button_style()
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.status = 0

    def set_font_size(self, font_size):
        self.font_size = font_size
        f = self.font()
        f.setPixelSize(self.font_size)
        self.setFont(f)

        # reset the style so that font
        # size changes carry through
        if self.status == 0:
            self.set_main_button_style()
        if self.status == 1:
            self.set_right_button_style()
        if self.status == 2:
            self.set_wrong_button_style()

    def set_wrong_button_style(self):
        self.setStyleSheet(f"""
                    QPushButton {{
                        font-family: "Encode Sans";
                        font-weight: 400;
                        line-height: 150%;
                        text-align: center;
                        color: #FFFFFF;
                        background: red;
                        padding: {0.4 * self.font_size}px;
                        border-radius: 25%;
                    }}

                    QPushButton:hover {{
                        background: red;
                    }}
                    
                    QPushButton:disabled {{
                        background: #E6E6E6;
                        color: #626262;
                    }}
                    
                    QPushButton:disabled:hover {{
                        background: #E6E6E6;
                    }}
                    
                    QPushButton:checked {{
                        background: #44AF69;
                    }}
                    
                    QPushButton:checked:hover {{
                        background: #368c54;
                    }}
                    
                    QPushButton#test_choice {{
                        padding: {0.765 * self.font_size}px;
                    }}
                """)
    def set_right_button_style(self):
        self.setStyleSheet(f"""
                    QPushButton {{
                        font-family: "Encode Sans";
                        font-weight: 400;
                        line-height: 150%;
                        text-align: center;
                        color: #FFFFFF;
                        background: green;
                        padding: {0.4 * self.font_size}px;
                        border-radius: 25%;
                    }}

                    QPushButton:hover {{
                        background: green;
                    }}
                    
                    QPushButton:disabled {{
                        background: #E6E6E6;
                        color: #626262;
                    }}
                    
                    QPushButton:disabled:hover {{
                        background: #E6E6E6;
                    }}
                    
                    QPushButton:checked {{
                        background: #44AF69;
                    }}
                    
                    QPushButton:checked:hover {{
                        background: #368c54;
                    }}
                    
                    QPushButton#test_choice {{
                        padding: {0.765 * self.font_size}px;
                    }}
                """)
    
    def set_main_button_style(self):
        self.setStyleSheet(f"""
                    QPushButton {{
                        font-family: "Encode Sans";
                        font-weight: 400;
                        line-height: 150%;
                        text-align: center;
                        color: #FFFFFF;
                        background: #074EE8;
                        padding: {0.4 * self.font_size}px;
                        border-radius: 25%;
                    }}

                    QPushButton:hover {{
                        background: #063eb7;
                    }}
                    
                    QPushButton:disabled {{
                        background: #E6E6E6;
                        color: #626262;
                    }}
                    
                    QPushButton:disabled:hover {{
                        background: #E6E6E6;
                    }}
                    
                    QPushButton:checked {{
                        background: #44AF69;
                    }}
                    
                    QPushButton:checked:hover {{
                        background: #368c54;
                    }}
                    
                    QPushButton#test_choice {{
                        padding: {0.765 * self.font_size}px;
                    }}
                """)
