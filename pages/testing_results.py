from typing import List

import PyQt6
import qtawesome
from PyQt6 import QtGui
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QGridLayout

from backend.get_ecg_from_db import Question
from components.heading_label import HeadingLabel
from components.main_button import MainButton
from components.paragraph_label import ParagraphLabel


class TestingResults(QWidget):
    answer_labels: List[ParagraphLabel] = []
    note_labels: List[ParagraphLabel] = []
    icons: List[qtawesome.IconWidget] = []

    def __init__(self, set_state):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)

        self.heading = HeadingLabel("Test")
        self.subheading = ParagraphLabel("See what you need to study next")
        self.score = ParagraphLabel("Your total score: ", 30)

        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.subheading)
        self.layout.addWidget(self.score)

        self.grid = QGridLayout()
        self.grid.setSpacing(30)
        self.grid.setHorizontalSpacing(60)
        self.layout.addLayout(self.grid)

        new_test_button = MainButton("Start new test")
        new_test_button.clicked.connect(set_state)
        self.layout.addWidget(new_test_button)

        self.layout.addSpacerItem(QSpacerItem(1, 1, PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                                              PyQt6.QtWidgets.QSizePolicy.Policy.Expanding))

    def update_page(self, answers, questions: List[Question]):
        self.clear_page()

        # This can move items closer together if needed
        # self.grid.addItem(QSpacerItem(1, 1, PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
        #                               PyQt6.QtWidgets.QSizePolicy.Policy.Fixed), 0, 3)

        number_correct = 0

        for i, (answer, question) in enumerate(zip(answers, questions)):
            answer_label = ParagraphLabel(f"{i + 1}. {answer}", 40)
            answer_label.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                       PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)
            self.answer_labels.append(answer_label)

            if answer == question.correct_answer:
                number_correct += 1
                self.grid.addWidget(answer_label, i, 0)

                check_widget = qtawesome.IconWidget()
                check_icon = qtawesome.icon("fa5s.check", color='green')
                check_widget.setIcon(check_icon)
                check_widget.setIconSize(QSize(40, 40))
                check_widget.update()
                self.grid.addWidget(check_widget, i, 1)

                self.icons.append(check_widget)
            else:
                self.grid.addWidget(answer_label, i, 0)

                x_widget = qtawesome.IconWidget()
                x_icon = qtawesome.icon("fa5s.times", color='red')
                x_widget.setIcon(x_icon)
                x_widget.setIconSize(QSize(40, 40))
                x_widget.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Fixed,
                                       PyQt6.QtWidgets.QSizePolicy.Policy.Fixed)
                x_widget.update()
                self.grid.addWidget(x_widget, i, 1)

                self.icons.append(x_widget)

                note_label = ParagraphLabel(f"Correct answer: {question.correct_answer}", 40)
                note_label.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                         PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)
                self.note_labels.append(note_label)
                self.grid.addWidget(note_label, i, 2)

        self.score.setText(f"Your total score: {number_correct}/{len(questions)}")
        self.update_buttons_font_size()

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        self.update_buttons_font_size()

    def update_buttons_font_size(self):
        button_font_size = 40

        # I upped it to 900 here
        if self.width() <= 900:
            button_font_size = 20
            self.grid.setSpacing(15)
            self.grid.setHorizontalSpacing(30)
        else:
            self.grid.setSpacing(30)
            self.grid.setHorizontalSpacing(60)

        for answer_label in self.answer_labels:
            answer_label.set_font_size(button_font_size)

        for note_label in self.note_labels:
            note_label.set_font_size(button_font_size)

        for icon in self.icons:
            icon.setIconSize(QSize(button_font_size, button_font_size))
            icon.update()

    def clear_page(self):

        # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt

        # Too lazy am I? Too Bad!
        for i in reversed(range(self.grid.count())):
            widget_to_remove = self.grid.itemAt(i).widget()
            # remove it from the layout list
            self.grid.removeWidget(widget_to_remove)
            # remove it from the gui
            widget_to_remove.setParent(None)
