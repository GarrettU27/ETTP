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
    home = None
    about_us = None
    testing = None
    training = None
    lead_placement = None
    read_ecg = None

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

        self.about_us = AboutUs()
        self.stackedWidget.addWidget(self.about_us)

        self.training = Training()
        self.stackedWidget.addWidget(self.training)

        self.testing = Testing()
        self.stackedWidget.addWidget(self.testing)

        self.home = Home()
        self.home.training_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.training))
        self.home.testing_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.testing))
        self.home.about_us_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.about_us))

        self.stackedWidget.addWidget(self.home)

        self.read_ecg = ReadECG()
        self.stackedWidget.addWidget(self.read_ecg)

        self.lead_placement = LeadPlacement()
        self.stackedWidget.addWidget(self.lead_placement)

        self.stackedWidget.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                                          PyQt6.QtWidgets.QSizePolicy.Policy.Expanding)

        self.stackedWidget.setCurrentWidget(self.home)

    def create_page_list(self):
        self.page_list = BurgerMenu()
        home = BurgerItem(["Home"], self.home)
        home.setIcon(0, qtawesome.icon("fa5s.home"))

        about_us = BurgerItem(["About Us"], self.about_us)
        about_us.setIcon(0, qtawesome.icon("fa5s.address-card"))

        train = BurgerItem(["Train"], self.training)
        train.setIcon(0, qtawesome.icon("fa5s.globe"))

        ecg_reading = BurgerItem(["ECG Reading"], self.read_ecg)
        ecg_reading.setIcon(0, qtawesome.icon("fa5s.book"))

        ecg_reading.addChild(BurgerItem(["Reading an ECG Strip"], self.read_ecg))
        ecg_reading.addChild(BurgerItem(["Lead Placements"], self.lead_placement))

        test = BurgerItem(["Test"], self.testing)
        test.setIcon(0, qtawesome.icon("fa5s.pen-nib"))

        self.page_list.addTopLevelItem(home)
        self.page_list.addTopLevelItem(train)
        self.page_list.addTopLevelItem(test)
        self.page_list.addTopLevelItem(ecg_reading)
        self.page_list.addTopLevelItem(about_us)
        self.page_list.itemClicked.connect(self.switch_page)

    def switch_page(self, item):
        self.stackedWidget.setCurrentWidget(item.widget)




