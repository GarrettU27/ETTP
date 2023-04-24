import io
import math
from functools import partial
from typing import List, Callable

import PyQt6
from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSlot, QThreadPool, QRunnable, QMetaObject, Q_ARG
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout

from backend.generate_ecg_plot import create_test_ecg
from backend.get_ecg_from_db import Question
from components.choice_button import ChoiceButton
from components.heading_label import HeadingLabel
from components.image_widget import ImageWidget
from components.waiting_spinner_widget import QtWaitingSpinner
from pages.testing_results import TestingResults


class TestingQuestions(QWidget):
    test_results: TestingResults
    current_question = 0
    total_questions: int
    end_test: bool
    back_to_results = 0
    restart_test = 0

    questions: List[Question]
    answer_buttons: List[ChoiceButton] = []
    answers: List[str] = []
    choices: List[str] = []

    def __init__(self, set_state: Callable, test_results: TestingResults, back_to_results: Callable, restart_test : Callable):
        super().__init__()
        self.test_results = test_results
        self.set_state = set_state
        self.end_test = False
        self.back_to_results = back_to_results
        self.restart_test = restart_test

        self.ecg_plot = ImageWidget()
        self.ecg_plot.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                                    PyQt6.QtWidgets.QSizePolicy.Policy.Expanding)

        self.title = HeadingLabel("Test")

        self.spinner = QtWaitingSpinner(self, True, True)

        self.spinner.setRoundness(70.0)
        self.spinner.setMinimumTrailOpacity(15.0)
        self.spinner.setTrailFadePercentage(70.0)
        self.spinner.setNumberOfLines(12)
        self.spinner.setLineLength(10)
        self.spinner.setLineWidth(5)
        self.spinner.setInnerRadius(10)
        self.spinner.setRevolutionsPerSecond(2.5)
        self.spinner.setColor(QColor(0, 0, 0))

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.ecg_plot)

        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)
        self.spinner.raise_()

    def start_new_test(self, questions: List[Question], choices: List[str]):
        self.questions = questions
        self.choices = choices
        self.end_test = False
        self.reset_test()

    def reset_test(self):
        self.current_question = 0
        self.total_questions = len(self.questions)
        self.answers = []

        for answer_button in self.answer_buttons:
            self.grid.removeWidget(answer_button)

        self.answer_buttons = []

        for choice in self.choices:
            answer_button = ChoiceButton(choice)
            answer_button.clicked.connect(partial(self.show_next_question, choice))
            self.answer_buttons.append(answer_button)

        self.update_buttons_font_size()

        for (i, answer_button) in enumerate(self.answer_buttons):
            self.grid.addWidget(answer_button, math.floor(i / 2), i % 2)

        exitButton = ChoiceButton("Exit test completely")
        exitButton.clicked.connect(partial(self.restart_test))
        #Not sure what color should go here, but 
        exitButton.setStyleSheet("QPushButton{{background: #ff6803;}}")
        exitButton.update()
        self.grid.addWidget(exitButton,math.floor(len(self.choices)/2 + 1),0,1,2)
        self.answer_buttons.append(exitButton)
        self.load_question()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update_buttons_font_size()

    def update_buttons_font_size(self):
        button_font_size = 40

        # this 'magic' numbers came from using a pixel ruler on my
        # computer to determine when the button becomes too wide
        # I just end up using this as the break point for all
        # size updates
        if self.width() <= 1380:
            button_font_size = 30
        if self.width() <= 1200:
            button_font_size = 20

        for answer_button in self.answer_buttons:
            answer_button.set_font_size(button_font_size)
        

    def show_next_question(self, previous_questions_answer: str):
        self.answers.append(previous_questions_answer)
        self.current_question += 1
        if self.current_question >= self.total_questions:
            self.end_test = True
            #self.test_results.update_page(self.answers, self.questions)
            self.test_results.updatePage(self.answers,self.questions)
            self.set_state()
        else:
            #Implement some code here to save the previous question's choices
            self.load_question()

    def load_question(self):
        self.spinner.start()
        load_test_ecg = LoadTestECG(self)
        QThreadPool.globalInstance().start(load_test_ecg)

    def show_previous_question(self, question_num):
        if self.end_test:
            self.current_question = question_num
            

            for answer_button in self.answer_buttons:
                self.grid.removeWidget(answer_button)
            self.answer_buttons = []

            for choice in self.choices:
                answer_button = ChoiceButton(choice)
                answer_button.setDisabled(True)
                if choice == self.answers[self.current_question]:
                    answer_button.setDisabled(False)
                    answer_button.status = 2
                    answer_button.set_wrong_button_style()
                if choice == self.questions[self.current_question].correct_answer:
                    answer_button.setDisabled(False)
                    answer_button.status = 1
                    answer_button.set_right_button_style()
                self.answer_buttons.append(answer_button)

            for (i, answer_button) in enumerate(self.answer_buttons):
                self.grid.addWidget(answer_button, math.floor(i / 2), i % 2)

            exitButton = ChoiceButton("Exit back to results page")
            exitButton.clicked.connect(partial(self.set_state))
            self.answer_buttons.append(exitButton)
            self.grid.addWidget(exitButton,math.floor(len(self.choices)/2 + 1),0,1,2)
            self.load_question()
            self.back_to_results()



    @pyqtSlot(io.BytesIO)
    def show_question(self, data):
        self.spinner.stop()
        self.adjustSize()

        self.title.setText(f"Test - Question {str(self.current_question + 1)}/{str(self.total_questions)}")

        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.ecg_plot.setPixmap(pixmap)

# https://gist.github.com/eyllanesc/1a09157d17ba13d223c312b28a81c320
class LoadTestECG(QRunnable):
    def __init__(self, testing_questions: TestingQuestions):
        QRunnable.__init__(self)
        self.testing_questions = testing_questions

    def run(self):
        ecg = create_test_ecg(self.testing_questions.questions[self.testing_questions.current_question].ecg)
        QMetaObject.invokeMethod(self.testing_questions, "show_question", Qt.ConnectionType.QueuedConnection,
                                 Q_ARG(bytes, ecg))
