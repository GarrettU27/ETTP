from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QCursor


class MainButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.set_main_button_style()
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

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
                    }

                    QPushButton:hover {
                        background: #063eb7;
                    }
                    
                    QPushButton:disabled {
                        background: #E6E6E6;
                        color: #626262;
                    }
                    
                    QPushButton:disabled:hover {
                        background: #E6E6E6;
                    }
                    
                    QPushButton:checked {
                        background: #44AF69;
                    }
                    
                    QPushButton:checked:hover {
                        background: #368c54;
                    }
                """)
