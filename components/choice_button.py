from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


class ChoiceButtonLeft(QPushButton):
    def __init__(self, text):
        super().__init__(text)



        self.setStyleSheet("""
            QPushButton {
                font-family:   "Encode Sans";
                font-weight:   400;
                font-size:     40px;
                line-height:   150%;
                text-align:    center;
                color:         #FFFFFF;
                background:    #074EE8;
                padding:       0.765em;
                border-radius: 25%;
                margin-top:    30px;
                margin-right:  15px;
            }
            
            QPushButton:hover {
                background: #063eb7;
            }
        """)
class ChoiceButtonRight(QPushButton):
    def __init__(self, text):
        super().__init__(text)



        self.setStyleSheet("""
            QPushButton {
                font-family:   "Encode Sans";
                font-weight:   400;
                font-size:     40px;
                line-height:   150%;
                text-align:    center;
                color:         #FFFFFF;
                background:    #074EE8;
                padding:       0.765em;
                border-radius: 25%;
                margin-top:    30px;
                margin-right   30px;
                margin-left:   15px;
            }
            
            QPushButton:hover {
                background: #063eb7;
            }
        """)

class ChoiceButtonNext(QPushButton):
    def __init__(self, text):
        super().__init__(text)



        self.setStyleSheet("""
            QPushButton {
                font-family:   "Encode Sans";
                font-weight:   400;
                font-size:     40px;
                line-height:   150%;
                text-align:    center;
                color:         #FFFFFF;
                background:    #074EE8;
                padding:       0.765em;
                border-radius: 25%;
                margin-top:    30px;
                margin-right   30px;
                margin-left:   15px;
            }
            
            QPushButton:hover {
                background: #063eb7;
            }
        """)