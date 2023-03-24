from typing import List

import PyQt6
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem

from backend.get_ecg_from_db import Question
from components.heading_label import HeadingLabel
from components.paragraph_label import ParagraphLabel


class TestingResults(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.heading = HeadingLabel("Test")
        self.layout.addWidget(self.heading)
        self.layout.setSpacing(30)

    def update_page(self, answers, questions: List[Question]):
        for answer, question in zip(answers, questions):
            if answer == question.correct_answer:
                answer_result = ParagraphLabel(f"Correct! Arrhythmia shown: {str(answer)}")
                self.layout.addWidget(answer_result)
            else:
                answer_result = ParagraphLabel(
                    f"Incorrect! Arrhythmia answered: {str(answer)}. Correct arrhythmia: {str(question.correct_answer)}")
                self.layout.addWidget(answer_result)

        self.layout.addSpacerItem(QSpacerItem(1, 1, PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                                              PyQt6.QtWidgets.QSizePolicy.Policy.Expanding))

    def clear_page(self):

        # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt

        # Too lazy am I? Too Bad!
        for i in reversed(range(self.layout.count())):
            widgetToRemove = self.layout.itemAt(i).widget()
            # remove it from the layout list
            self.layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
