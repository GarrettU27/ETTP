import PyQt6
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QMainWindow, QStackedWidget
from PyQt6.uic.properties import QtWidgets

from generate_ecg_plot import get_ecg_svg
from pages.home import Home
from pages.testing import Testing
from pages.training import Training
from pages.welcome import Welcome


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # handle high dpi
        if hasattr(PyQt6.QtCore.Qt, 'AA_EnableHighDpiScaling'):
            PyQt6.QtWidgets.QApplication.setAttribute(PyQt6.QtCore.Qt.AA_EnableHighDpiScaling, True)

        if hasattr(PyQt6.QtCore.Qt, 'AA_UseHighDpiPixmaps'):
            PyQt6.QtWidgets.QApplication.setAttribute(PyQt6.QtCore.Qt.AA_UseHighDpiPixmaps, True)

        # set screen size based off current screen size
        screenSize = self.screen().availableGeometry().size() * (3 / 4)

        self.resize(screenSize.width(), screenSize.height())
        self.setWindowTitle("ETTP")
        self.setWindowIcon(QIcon("icon.jpg"))

        self.stackedWidget = QStackedWidget()

        self.home = Home()
        self.home.button.clicked.connect(self.go_to_welcome)
        self.stackedWidget.addWidget(self.home)

        self.welcome = Welcome()
        self.welcome.button.clicked.connect(self.go_to_training)
        self.stackedWidget.addWidget(self.welcome)

        self.training = Training()
        self.training.button.clicked.connect(self.go_to_testing)
        self.stackedWidget.addWidget(self.training)

        self.testing = Testing()
        self.testing.button.clicked.connect(self.go_to_home)
        self.stackedWidget.addWidget(self.testing)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stackedWidget)
        self.setLayout(self.layout)

        self.setCentralWidget(self.stackedWidget)

    def go_to_home(self):
        self.stackedWidget.setCurrentIndex(0)

    def go_to_welcome(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_to_training(self):
        self.stackedWidget.setCurrentIndex(2)

    def go_to_testing(self):
        self.stackedWidget.setCurrentIndex(3)
