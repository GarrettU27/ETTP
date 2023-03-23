from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout

from Logic.testing import Testing_object
from backend.generate_ecg_plot import get_ecg_svg
from components.choice_button import ChoiceButtonLeft, ChoiceButtonRight
from components.heading_label import HeadingLabelTest
from pages.testing_results import TestingResults


class TestingQuestions(QWidget):
    test_object = Testing_object
    choices = ["something", "Is", "Really", "Wrong"]
    ECG_data = []
    test_results: TestingResults

    def __init__(self, test_results: TestingResults):
        super().__init__()
        self.qsw = QSvgWidget()
        self.test_object = Testing_object()
        self.test_results = test_results
        # self.choices = self.test_object.next_question()

        # get all of the necessary files required for creating the testing object here

        # load in the SVG data stream
        self.qsw.load(get_ecg_svg())
        self.qsw.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.title = HeadingLabelTest("Question")
        self.answer1 = ChoiceButtonLeft(self.choices[0])
        self.answer2 = ChoiceButtonRight(self.choices[1])
        self.answer3 = ChoiceButtonLeft(self.choices[2])
        self.answer4 = ChoiceButtonRight(self.choices[3])
        self.answer1.clicked.connect(lambda: self.update_nextQ(self.answer1))
        self.answer2.clicked.connect(lambda: self.update_nextQ(self.answer2))
        self.answer3.clicked.connect(lambda: self.update_nextQ(self.answer3))
        self.answer4.clicked.connect(lambda: self.update_nextQ(self.answer4))
        self.next = QPushButton(self)
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.title, 0, 1, 1, 2)
        self.layout.addWidget(self.answer1, 6, 0, 1, 2)
        self.layout.addWidget(self.answer2, 6, 2, 1, 2)
        self.layout.addWidget(self.answer3, 7, 0, 1, 2)
        self.layout.addWidget(self.answer4, 7, 2, 1, 2)
        self.layout.addWidget(self.qsw, 1, 0, 3, 4)

    def update_nextQ(self, item):
        self.test_object.add_answers(item.text())
        self.choices = self.test_object.next_question()
        if self.choices[0] == "X":
            print(self.test_object.answers)
            print(self.test_object.correct)
            self.test_object.check_answers()
            print(self.test_object.correctAns)
            self.test_results.update_page(self.test_object.questions, self.test_object.answers,
                                          self.test_object.correct, self.test_object.correctAns)
            return -1
        else:
            self.qsw.load(self.test_object.get_next_svg())
            self.title.setText("Question " + str(self.test_object.index_Q))
            self.answer1.setText(self.choices[0])
            self.answer2.setText(self.choices[1])
            self.answer3.setText(self.choices[2])
            self.answer4.setText(self.choices[3])

    def set_ecg_data(self, ecg_stuff):
        self.ECG_data = ecg_stuff.copy()
        self.test_object.set_arrhythmia(self.ECG_data)
        self.test_object.update_object()

    def start_test(self):
        self.choices = self.test_object.next_question()
        self.title.setText("Question " + str(self.test_object.index_Q))
        self.qsw.load(self.test_object.get_next_svg())
        self.answer1.setText(self.choices[0])
        self.answer2.setText(self.choices[1])
        self.answer3.setText(self.choices[2])
        self.answer4.setText(self.choices[3])
