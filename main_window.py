import PyQt6
import qtawesome
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QStackedWidget, QHBoxLayout, \
    QListWidget, QPushButton, QTreeWidget, QTreeWidgetItem

from burger_menu import BurgerMenu
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

        self.page_list = BurgerMenu(250)
        home = QTreeWidgetItem(["Home"])
        home.setIcon(0, qtawesome.icon("fa5s.home"))

        about_us = QTreeWidgetItem(["About Us"])
        about_us.setIcon(0, qtawesome.icon("fa5s.address-card"))

        train = QTreeWidgetItem(["Train"])
        train.setIcon(0, qtawesome.icon("fa5s.globe"))

        train.addChild(QTreeWidgetItem(["Start New"]))
        train.addChild(QTreeWidgetItem(["Reading an ECG Strip"]))
        train.addChild(QTreeWidgetItem(["Lead Placements"]))

        test = QTreeWidgetItem(["Test"])
        test.setIcon(0, qtawesome.icon("fa5s.pen-nib"))

        test.addChild(QTreeWidgetItem(["Start New"]))
        test.addChild(QTreeWidgetItem(["Last Score"]))
        test.addChild(QTreeWidgetItem(["Resume"]))

        tools = QTreeWidgetItem(["Tools"])
        tools.setIcon(0, qtawesome.icon("fa5s.wrench"))

        manage = QTreeWidgetItem(["Manage"])
        manage.setIcon(0, qtawesome.icon("fa5s.cog"))

        self.page_list.addTopLevelItem(home)
        self.page_list.addTopLevelItem(about_us)
        self.page_list.addTopLevelItem(train)
        self.page_list.addTopLevelItem(test)
        self.page_list.addTopLevelItem(tools)
        self.page_list.addTopLevelItem(manage)
        self.page_list.itemClicked.connect(self.switch_page)

        self.burger_button = QPushButton("BURGER")
        self.burger_button.clicked.connect(self.page_list.toggle)

        default_window = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.page_list)
        layout.addWidget(self.burger_button)
        layout.addWidget(self.stackedWidget)
        default_window.setLayout(layout)

        self.setCentralWidget(default_window)

    def switch_page(self, item):
        match item.text(0):
            case "Home":
                self.stackedWidget.setCurrentIndex(0)
            case "About Us":
                self.stackedWidget.setCurrentIndex(1)
            case "Training":
                self.stackedWidget.setCurrentIndex(2)
            case "Testing":
                self.stackedWidget.setCurrentIndex(3)
            case _:
                self.stackedWidget.setCurrentIndex(0)



