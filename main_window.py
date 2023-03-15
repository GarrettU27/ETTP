import PyQt6
import qtawesome
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QStackedWidget, QHBoxLayout, \
    QPushButton, QTreeWidgetItem, QScrollArea

from components.burger_menu import BurgerMenu
from pages.about_us import AboutUs
from pages.home import Home
from pages.lead_placement import LeadPlacement
from pages.read_ecg import ReadECG
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

        self.setStyleSheet("* { background: #ffffff; }")

        self.resize(screenSize.width(), screenSize.height())
        self.setWindowTitle("ETTP")
        self.setWindowIcon(QIcon("icon.jpg"))

        # https://stackoverflow.com/questions/12781407/how-do-i-resize-the-contents-of-a-qscrollarea-as-more-widgets-are-placed-inside
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.stackedWidget = QStackedWidget(self.scroll)

        self.scroll.setWidget(self.stackedWidget)

        self.scroll.setStyleSheet("* { border: none; }")

        welcome = Welcome()
        welcome.about_us_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.stackedWidget.addWidget(welcome)

        about_us = AboutUs()
        self.stackedWidget.addWidget(about_us)

        home = Home()
        self.stackedWidget.addWidget(home)

        training = Training()
        self.stackedWidget.addWidget(training)

        testing = Testing()
        self.stackedWidget.addWidget(testing)

        lead_placement = LeadPlacement()
        self.stackedWidget.addWidget(lead_placement)

        read_ecg = ReadECG()
        self.stackedWidget.addWidget(read_ecg)

        self.page_list = BurgerMenu()
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

        # tools = QTreeWidgetItem(["Tools"])
        # tools.setIcon(0, qtawesome.icon("fa5s.wrench"))
        #
        # manage = QTreeWidgetItem(["Manage"])
        # manage.setIcon(0, qtawesome.icon("fa5s.cog"))

        self.page_list.addTopLevelItem(home)
        self.page_list.addTopLevelItem(about_us)
        self.page_list.addTopLevelItem(train)
        self.page_list.addTopLevelItem(test)
        # self.page_list.addTopLevelItem(tools)
        # self.page_list.addTopLevelItem(manage)
        self.page_list.itemClicked.connect(self.switch_page)

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
            case "Lead Placements":
                self.stackedWidget.setCurrentIndex(5)
            case "Reading an ECG Strip":
                self.stackedWidget.setCurrentIndex(6)
            case _:
                self.stackedWidget.setCurrentIndex(0)




