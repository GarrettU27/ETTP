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
            ("", "We created this application to allow users of all levels to improve their knowledge of ECGs and their ability to read an ECG strip and Identify different arrhythmias."),
            ("images:marie.jpg", "Marie Hessefort: I am an Electrical Engineering major at the University of Minnesota with a focus in Biomedical Engineering, Circuit Design, and Digital Signal Processing. "),
            ("images:henry.jpg", "Henry Hein: I am a Computer Engineering major at the University of Minnesota with a focus in Firmware and Digital Logic Design"),
            ("images:michael.jpg", "Michael Johnson: I am a Computer Engineering major at the University of Minnesota."),
            ("images:jacob.jpg", "Jacob Medchill: I am a Computer Engineering major at the University of Minnesota with a focus on embedded systems."),
            ("images:garrett.png", "Garrett Udstrand: I am a Computer Engineering major at the University of Minnesota with a focus in Application Development and AI."),
            ("images:Sobelman.jpg", "Gerald Sobelman: Project Sponsor and Professor, Department of Electrical and Computer Engineering.  Learn more about my research at: https://cse.umn.edu/ece/gerald-sobelman") 
        ]

        for image, name, in people:
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
