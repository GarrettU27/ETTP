import PyQt6
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem

from backend.generate_ecg_plot import get_ecg_svg
from components.heading_label import HeadingLabel
from components.image_widget import ImageWidget
from components.main_button import MainButton


class Home(QWidget):
    def __init__(self, start_new_training_function, start_new_testing_function, about_us_function):
        super().__init__()

        self.heading = HeadingLabel("Home")
        self.training_button = MainButton("Train")
        self.testing_button = MainButton("Test")
        self.about_us_button = MainButton("About Us")

        self.training_button.clicked.connect(start_new_training_function)
        self.testing_button.clicked.connect(start_new_testing_function)
        self.about_us_button.clicked.connect(about_us_function)

        image = ImageWidget()
        pix = QPixmap()
        pix.loadFromData(get_ecg_svg())
        image.setPixmap(pix)
        image.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                          PyQt6.QtWidgets.QSizePolicy.Policy.Expanding)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.training_button)
        self.layout.addWidget(self.testing_button)
        self.layout.addWidget(self.about_us_button)
        self.layout.addWidget(image)

        self.layout.setStretch(self.layout.indexOf(image), 2)

        self.layout.addStretch(1)

        # self.layout.addSpacerItem(QSpacerItem(1, 1, PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
        #                                       PyQt6.QtWidgets.QSizePolicy.Policy.Expanding))
