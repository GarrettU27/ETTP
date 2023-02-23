import PyQt6
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QStackedWidget, QHBoxLayout, \
    QListWidget, QPushButton

from pages.home import Home
from pages.testing import Testing
from pages.training import Training
from pages.welcome import Welcome


class MainWindow(QMainWindow):
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

        home = Home()
        self.stackedWidget.addWidget(home)

        welcome = Welcome()
        self.stackedWidget.addWidget(welcome)

        training = Training()
        self.stackedWidget.addWidget(training)

        testing = Testing()
        self.stackedWidget.addWidget(testing)

        self.burger_button = QPushButton("BURGER")
        self.burger_button.clicked.connect(self.hide_burger_menu)

        page_list = QListWidget()
        page_list.addItem("Home")
        page_list.addItem("Welcome")
        page_list.addItem("Training")
        page_list.addItem("Testing")
        page_list.itemClicked.connect(self.switch_page)

        default_window = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(page_list)
        layout.addWidget(self.burger_button)
        layout.addWidget(self.stackedWidget)
        default_window.setLayout(layout)

        self.setCentralWidget(default_window)

    def switch_page(self, item):
        match item.text():
            case "Home":
                self.stackedWidget.setCurrentIndex(0)
            case "Welcome":
                self.stackedWidget.setCurrentIndex(1)
            case "Training":
                self.stackedWidget.setCurrentIndex(2)
            case "Testing":
                self.stackedWidget.setCurrentIndex(3)
            case _:
                self.stackedWidget.setCurrentIndex(0)

    def show_burger_menu(self):
        page_list = QListWidget()
        page_list.addItem("Home")
        page_list.addItem("Welcome")
        page_list.addItem("Training")
        page_list.addItem("Testing")
        page_list.itemClicked.connect(self.switch_page)

        default_window = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(page_list)
        layout.addWidget(self.burger_button)
        layout.addWidget(self.stackedWidget)
        default_window.setLayout(layout)

        self.burger_button.clicked.connect(self.hide_burger_menu)

        self.setCentralWidget(default_window)

    def hide_burger_menu(self):
        default_window = QWidget()
        self.burger_button.clicked.connect(self.show_burger_menu)
        layout = QHBoxLayout()
        layout.addWidget(self.burger_button)
        layout.addWidget(self.stackedWidget)
        default_window.setLayout(layout)
        self.setCentralWidget(default_window)
