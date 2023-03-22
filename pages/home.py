import PyQt6
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from components.heading_label import HeadingLabel
from components.main_button import MainButton
from backend.generate_ecg_plot import get_ecg_svg


class Home(QWidget):
    def __init__(self):
        super().__init__()

        self.heading = HeadingLabel("Home")
        self.training_button = MainButton("Train")
        self.testing_button = MainButton("Test")
        self.about_us_button = MainButton("About Us")

        qsw = QSvgWidget()
        qsw.load(get_ecg_svg())
        qsw.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        qsw.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                                              PyQt6.QtWidgets.QSizePolicy.Policy.Expanding)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.training_button)
        self.layout.addWidget(self.testing_button)
        self.layout.addWidget(self.about_us_button)
        self.layout.addWidget(qsw)
