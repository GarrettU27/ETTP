import math
from typing import List, Callable

import PyQt6
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout

from backend.generate_ecg_plot import create_test_ecg
from backend.get_ecg_from_db import Question
from components.choice_button import ChoiceButton
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

        self.qsw = QSvgWidget()
        self.qsw.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                               PyQt6.QtWidgets.QSizePolicy.Policy.Expanding)

        self.title = HeadingLabel("Test")

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.qsw)

        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

    def start_new_test(self, questions: List[Question], choices: List[str]):
        self.questions = questions
        self.choices = choices
        self.reset_test()

    def reset_test(self):
        self.current_question = 0
        self.total_questions = len(self.questions)

        for answer_button in self.answer_buttons:
            self.grid.removeWidget(answer_button)

        self.answer_buttons = []

        for choice in self.choices:
            answer_button = ChoiceButton(choice)
            answer_button.clicked.connect(lambda: self.show_next_question(choice))
            self.answer_buttons.append(answer_button)

        for (i, answer_button) in enumerate(self.answer_buttons):
            self.grid.addWidget(answer_button, math.floor(i / 2), i % 2)

        self.show_question()

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
        self.qsw.load(create_test_ecg(self.questions[self.current_question].ecg))
        self.qsw.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
