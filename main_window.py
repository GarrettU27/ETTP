from enum import Enum

import PyQt6
import qtawesome
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtWidgets import QWidget, QMainWindow, QStackedWidget, QHBoxLayout, \
    QPushButton

from components.burger_item import BurgerItem
from components.burger_menu import BurgerMenu
from pages.about_us import AboutUs
from pages.home import Home
from pages.lead_placement import LeadPlacement
from pages.read_ecg import ReadECG
from pages.scrollable_page import ScrollablePage
from pages.start_new.start_new_testing import StartNewTesting
from pages.start_new.start_new_training import StartNewTraining
from pages.testing_questions import TestingQuestions
from pages.testing_results import TestingResults
from pages.training_flashcards import TrainingFlashcards


class MainWindow(QMainWindow):
    class State(Enum):
        NEW = 1
        IN_PROGRESS = 2
        DONE = 3

    home = None
    about_us = None
    testing = None
    training = None
    lead_placement = None
    read_ecg = None
    start_new_testing = None
    testing_questions = None
    testing_results = None
    start_new_training = None
    training_questions = None
    training_results = None

    testing_state: State = State.NEW
    training_state: State = State.NEW

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
        self.setWindowIcon(QIcon("images:icon.jpg"))

        self.scroll = None
        self.stacked_widget = None
        self.create_stacked_widget()

        self.page_list = None
        self.create_page_list()

        burger_icon = qtawesome.icon("fa5s.bars")
        self.burger_button = QPushButton(burger_icon, "")
        self.burger_button.setIconSize(QSize(30, 30))
        self.burger_button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
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
        layout.addWidget(self.stacked_widget)
        default_window.setLayout(layout)

        self.setCentralWidget(default_window)

    def create_stacked_widget(self):
        # https://stackoverflow.com/questions/12781407/how-do-i-resize-the-contents-of-a-qscrollarea-as-more-widgets-are-placed-inside
        # self.scroll = QScrollArea()
        # self.scroll.setWidgetResizable(True)

        # There's a bug that causes the app to crash if the vertical scrollbar appears due to an
        # AspectRatioImage resizing. To deal with that, we just always keep the scrollbar on.
        # There potentially is a better solution, but this will work for now
        # self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.stacked_widget = QStackedWidget(self)

        # self.scroll.setWidget(self.stacked_widget)
        #
        # self.scroll.setStyleSheet("* { border: none; }")

        self.about_us = ScrollablePage(AboutUs())
        self.stacked_widget.addWidget(self.about_us)

        self.home = Home()
        self.home.training_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.start_new_training))
        self.home.testing_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.start_new_testing))
        self.home.about_us_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.about_us))

        self.stacked_widget.addWidget(self.home)

        self.read_ecg = ScrollablePage(ReadECG())
        self.stacked_widget.addWidget(self.read_ecg)

        self.lead_placement = ScrollablePage(LeadPlacement())
        self.stacked_widget.addWidget(self.lead_placement)

        self.testing_results = TestingResults(
            lambda: (self.set_testing_state(self.State.NEW), self.choose_testing_page())
        )
        self.stacked_widget.addWidget(self.testing_results)

        self.testing_questions = TestingQuestions(
            lambda: (self.set_testing_state(self.State.DONE), self.choose_testing_page()),
            self.testing_results
        )
        self.stacked_widget.addWidget(self.testing_questions)

        self.start_new_testing = StartNewTesting(
            lambda: (self.set_testing_state(self.State.IN_PROGRESS), self.choose_testing_page()),
            self.testing_questions
        )
        self.stacked_widget.addWidget(self.start_new_testing)

        self.training_questions = TrainingFlashcards(
            lambda: (self.set_training_state(self.State.NEW), self.choose_training_page())
        )
        self.stacked_widget.addWidget(self.training_questions)

        self.start_new_training = StartNewTraining(
            lambda: (self.set_training_state(self.State.IN_PROGRESS), self.choose_training_page()),
            self.training_questions
        )
        self.stacked_widget.addWidget(self.start_new_training)

        self.stacked_widget.setCurrentWidget(self.home)

    def choose_training_page(self):
        match self.training_state:
            case self.State.NEW:
                self.stacked_widget.setCurrentWidget(self.start_new_training)
            case self.State.IN_PROGRESS:
                self.stacked_widget.setCurrentWidget(self.training_questions)

    def choose_testing_page(self):
        match self.testing_state:
            case self.State.NEW:
                self.stacked_widget.setCurrentWidget(self.start_new_testing)
            case self.State.IN_PROGRESS:
                self.stacked_widget.setCurrentWidget(self.testing_questions)
            case self.State.DONE:
                self.stacked_widget.setCurrentWidget(self.testing_results)

    def set_testing_state(self, testing_state: State):
        self.testing_state = testing_state

    def set_training_state(self, training_state: State):
        self.training_state = training_state

    def create_page_list(self):
        self.page_list = BurgerMenu()
        home = BurgerItem(["Home"], self.home)
        home.setIcon(0, qtawesome.icon("fa5s.home"))

        about_us = BurgerItem(["About Us"], self.about_us)
        about_us.setIcon(0, qtawesome.icon("fa5s.address-card"))

        train = BurgerItem(["Train"], self.start_new_training)
        train.setIcon(0, qtawesome.icon("fa5s.globe"))

        ecg_reading = BurgerItem(["ECG Reading"], self.read_ecg)
        ecg_reading.setIcon(0, qtawesome.icon("fa5s.book"))

        ecg_reading.addChild(BurgerItem(["Reading an ECG Strip"], self.read_ecg))
        ecg_reading.addChild(BurgerItem(["Lead Placements"], self.lead_placement))

        test = BurgerItem(["Test"], self.start_new_testing)
        test.setIcon(0, qtawesome.icon("fa5s.pen-nib"))

        self.page_list.addTopLevelItem(home)
        self.page_list.addTopLevelItem(train)
        self.page_list.addTopLevelItem(test)
        self.page_list.addTopLevelItem(ecg_reading)
        self.page_list.addTopLevelItem(about_us)
        self.page_list.itemClicked.connect(self.switch_page)

    def switch_page(self, item):
        if item.widget == self.start_new_training:
            self.choose_training_page()
        elif item.widget == self.start_new_testing:
            self.choose_testing_page()
        else:
            self.stacked_widget.setCurrentWidget(item.widget)
