from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout

from arrhythmia import supported_arrhythmias
from components.heading_label import HeadingLabel
from components.main_button import MainButton


class StartNewTesting(QWidget):
    def __init__(self):
        super().__init__()

        self.heading = HeadingLabel("What Do You Want to be Tested On?")

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.heading, 0, 0)

        for index, arrhythmia in enumerate(supported_arrhythmias):
            self.layout.addWidget(MainButton(arrhythmia.name), index + 1, 0)
