from enum import IntEnum

import PyQt6
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QStackedWidget
from pages.start_new.start_new_training import StartNewTraining
from pages.training_questions import TrainingQuestions
from pages.training_results import TrainingResults


class Training(QWidget):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                                          PyQt6.QtWidgets.QSizePolicy.Policy.Expanding)
        self.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                                          PyQt6.QtWidgets.QSizePolicy.Policy.Expanding)

        self.start_new = StartNewTraining()
        self.stacked_widget.addWidget(self.start_new)

        self.training_questions = TrainingQuestions()
        self.stacked_widget.addWidget(self.training_questions)

        self.training_results = TrainingResults()
        self.stacked_widget.addWidget(self.training_results)

        self.start_new.begin_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.training_questions))
