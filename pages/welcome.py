from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout

from components.heading_label import HeadingLabel
from components.main_button import MainButton
from generate_ecg_plot import get_ecg_svg


class Welcome(QWidget):
    def __init__(self):
        super().__init__()

        self.heading = HeadingLabel("Welcome")
        # self.heading.setMaximumHeight(self.heading.sizeHint().height())
        self.about_us_button = MainButton("About Us")
        self.training_button = MainButton("Train")
        self.testing_button = MainButton("Test")

        qsw = QSvgWidget()
        qsw.load(get_ecg_svg())
        qsw.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.heading, 0, 0)
        self.layout.addWidget(self.about_us_button, 1, 0)
        self.layout.addWidget(self.training_button, 2, 0)
        self.layout.addWidget(self.testing_button, 3, 0)
        self.layout.addWidget(qsw, 4, 0, 3, 1)
