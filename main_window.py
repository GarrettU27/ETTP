import PyQt6
import qtawesome
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMainWindow, QStackedWidget, QHBoxLayout, \
    QPushButton, QScrollArea

from components.burger_item import BurgerItem
from components.burger_menu import BurgerMenu
from pages.about_us import AboutUs
from pages.lead_placement import LeadPlacement
from pages.read_ecg import ReadECG
from pages.start_new.start_new_testing import StartNewTesting
from pages.start_new.start_new_training import StartNewTraining
from pages.testing import Testing
from pages.training import Training
from pages.home import Home



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

        self.setStyleSheet("* { background: #ffffff; }")

        self.resize(screenSize.width(), screenSize.height())
        self.setWindowTitle("ETTP")
        self.setWindowIcon(QIcon("icon.jpg"))

        self.scroll = None
        self.stackedWidget = None
        self.create_stacked_widget()

        self.page_list = None
        self.create_page_list()

        burger_icon = qtawesome.icon("fa5s.bars")
        self.burger_button = QPushButton(burger_icon, "")
        self.burger_button.setIconSize(QSize(30, 30))
        self.burger_button.setStyleSheet("""
            QPushButton { 
                border: none; 
            }      
        """)
        self.burger_button.clicked.connect(self.page_list.toggle)

        default_window = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.page_list)
        layout.addWidget(self.burger_button)
        layout.setAlignment(self.burger_button, PyQt6.QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.scroll)
        default_window.setLayout(layout)

        self.setCentralWidget(default_window)

    def create_stacked_widget(self):
        # https://stackoverflow.com/questions/12781407/how-do-i-resize-the-contents-of-a-qscrollarea-as-more-widgets-are-placed-inside
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.stackedWidget = QStackedWidget(self.scroll)

        self.scroll.setWidget(self.stackedWidget)

        self.scroll.setStyleSheet("* { border: none; }")

        welcome = Home()
        welcome.training_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        welcome.testing_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))
        welcome.about_us_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        self.stackedWidget.addWidget(welcome)

        about_us = AboutUs()
        self.stackedWidget.addWidget(about_us)

        training = Training()
        self.stackedWidget.addWidget(training)

        testing = Testing()
        self.stackedWidget.addWidget(testing)

        start_new_training = StartNewTraining()
        self.stackedWidget.addWidget(start_new_training)

        read_ecg = ReadECG()
        self.stackedWidget.addWidget(read_ecg)

        lead_placement = LeadPlacement()
        self.stackedWidget.addWidget(lead_placement)

        start_new_testing = StartNewTesting()
        self.stackedWidget.addWidget(start_new_testing)

    def create_page_list(self):
        self.page_list = BurgerMenu()
        home = BurgerItem(["Home"], 0)
        home.setIcon(0, qtawesome.icon("fa5s.home"))

        about_us = BurgerItem(["About Us"], 1)
        about_us.setIcon(0, qtawesome.icon("fa5s.address-card"))

        train = BurgerItem(["Train"], 4)
        train.setIcon(0, qtawesome.icon("fa5s.globe"))

        ecg_reading = BurgerItem(["ECG Reading"], 10)
        ecg_reading.setIcon(0, qtawesome.icon("fa5s.book"))

        ecg_reading.addChild(BurgerItem(["Reading an ECG Strip"], 5))
        ecg_reading.addChild(BurgerItem(["Lead Placements"], 6))

        test = BurgerItem(["Test"], 7)
        test.setIcon(0, qtawesome.icon("fa5s.pen-nib"))

        self.page_list.addTopLevelItem(home)
        self.page_list.addTopLevelItem(train)
        self.page_list.addTopLevelItem(test)
        self.page_list.addTopLevelItem(ecg_reading)
        self.page_list.addTopLevelItem(about_us)
        self.page_list.itemClicked.connect(self.switch_page)

    def switch_page(self, item):
        self.stackedWidget.setCurrentIndex(item.index)




