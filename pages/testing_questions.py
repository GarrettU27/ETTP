import math
from functools import partial
from typing import List, Callable

from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout

from backend.get_ecg_from_db import Question
from components.choice_button import ChoiceButton
from components.ecg_plot import ECGPlot
from components.heading_label import HeadingLabel
from pages.testing_results import TestingResults


class TestingQuestions(QWidget):
    test_results: TestingResults
    current_question = 0
    total_questions: int

    questions: List[Question]
    answer_buttons: List[ChoiceButton] = []
    answers: List[str] = []
    choices: List[str] = []

    def __init__(self, set_state: Callable, test_results: TestingResults):
        super().__init__()
        self.test_results = test_results
        self.set_state = set_state

        self.title = HeadingLabel("Test")
        self.ecg_plot = ECGPlot()

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.ecg_plot)

        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)
        self.layout.addStretch(1)

    def start_new_test(self, questions: List[Question], choices: List[str]):
        self.questions = questions
        self.choices = choices
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

        self.show_question()

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        self.update_buttons_font_size()

    def update_buttons_font_size(self):
        button_font_size = 40

        # this 'magic' 795 number came from using a pixel ruler on my
        # computer to determine when the button becomes too wide
        # I just end up using this as the break point for all
        # size updates
        if self.width() <= 795:
            button_font_size = 20

        for answer_button in self.answer_buttons:
            answer_button.set_font_size(button_font_size)

    def show_next_question(self, previous_questions_answer: str):
        self.answers.append(previous_questions_answer)
        self.current_question += 1
        if self.current_question >= self.total_questions:
            self.test_results.update_page(self.answers, self.questions)
            self.set_state()
        else:
            self.show_question()

    def show_question(self):
        self.title.setText(f"Test - Question {str(self.current_question + 1)}/{str(self.total_questions)}")
        self.ecg_plot.plot_ecg(self.questions[self.current_question].ecg)
