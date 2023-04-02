import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from scipy.io import loadmat

from components.ecg_plot import ECGPlot
from components.heading_label import HeadingLabel
from components.main_button import MainButton


def convert_to_millivolts(microvolts: int):
    # the data is in microvolts, convert to millivolts
    return microvolts / 1000


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

        mat = loadmat("./JS00001.mat")
        data = mat["val"]
        ecg = []

        for ecg_lead in data:
            ecg.append([convert_to_millivolts(bits) for bits in ecg_lead][0:1300])

        ecg = np.array(ecg)
        ecg_plot = ECGPlot()
        ecg_plot.plot_ecg(ecg)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.training_button)
        self.layout.addWidget(self.testing_button)
        self.layout.addWidget(self.about_us_button)
        self.layout.addWidget(ecg_plot)

        self.layout.addStretch(1)
