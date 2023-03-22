import os.path

import PyQt6.QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QSpacerItem, QLabel, QVBoxLayout, QHBoxLayout

from components.about_us_picture import AboutUsPicture
from components.heading_label import HeadingLabel
from components.paragraph_label import ParagraphLabel


class AboutUs(QWidget):
    def __init__(self):
        super().__init__()

        self.heading = HeadingLabel("About Us")

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(16)
        self.layout.addWidget(self.heading)

        people = [
            ("images:marie.jpg", "Marie Hessefort"),
            ("images:henry.jpg", "Henry Hein"),
            ("images:michael.jpg", "Michael Johnson"),
            ("images:jacob.jpg", "Jacob Medchill"),
            ("images:garrett.png", "Garrett Udstrand")
        ]

        for image, name in people:
            horizontal_layout = QHBoxLayout()
            horizontal_layout.setSpacing(30)
            horizontal_layout.addWidget(AboutUsPicture(image))
            horizontal_layout.addWidget(ParagraphLabel(name))
            self.layout.addLayout(horizontal_layout)

        self.layout.addSpacerItem(QSpacerItem(1, 1, PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                          PyQt6.QtWidgets.QSizePolicy.Policy.Expanding))

        # self.layout.addWidget(AboutUsPicture("../images/marie.jpg"), 1, 0)
        # self.layout.addWidget(ParagraphLabel("Marie Hessefort"), 1, 1)
        #
        # self.layout.addWidget(QLabel("Filler"), 2, 0)
        # self.layout.addWidget(ParagraphLabel("Henry Hein"), 2, 1)
        #
        # self.layout.addWidget(AboutUsPicture("../images/michael.jpg"), 3, 0)
        # self.layout.addWidget(ParagraphLabel("Michael Johnson"), 3, 1)
        #
        # self.layout.addWidget(AboutUsPicture("../images/jacob.jpg"), 4, 0)
        # self.layout.addWidget(ParagraphLabel("Jacob Medchill"), 4, 1)
        #
        # self.layout.addWidget(AboutUsPicture("../images/garrett.png"), 5, 0)
        # self.layout.addWidget(ParagraphLabel("Garrett Udstrand"), 5, 1)
