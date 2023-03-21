import os.path

import PyQt6
from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QComboBox, QVBoxLayout, QSpacerItem
from arrhythmia import supported_arrhythmias
from components.heading_label import HeadingLabel
from components.main_button import MainButton
from components.main_checkbox import MainCheckbox


class StartNew(QWidget):
    def __init__(self):
        super().__init__()

        self.heading = HeadingLabel(self.heading_text())
        self.heading.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                     PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.heading)
        self.layout.setSpacing(30)

        for index, arrhythmia in enumerate(supported_arrhythmias):
            self.layout.addWidget(MainCheckbox(arrhythmia.name))

        submission_row = QWidget()
        submission_row.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                     PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)

        submission_layout = QHBoxLayout(submission_row)
        question_number = QComboBox()
        question_number.addItems(str(num * 5) for num in range(1, 6))
        question_number.setCurrentIndex(2)
        submission_layout.addWidget(question_number)
        question_number.setStyleSheet("""
            QComboBox {
                font-family: "Encode Sans";
                border: 1px solid #ddd;
                padding: 0.4em;
                font-size: 40px;
                border-radius: 25%;
            }

            QComboBox::drop-down {
                border: none;
            }
            
            QComboBox::down-arrow {
                image: url(images:dropdown.png);
                padding-right: 40px;
            }
        """)

        submission_layout.addWidget(MainButton(self.begin_button_text()))
        submission_layout.setSpacing(30)

        self.layout.addWidget(submission_row)
        self.layout.addSpacerItem(QSpacerItem(1, 1, PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                                     PyQt6.QtWidgets.QSizePolicy.Policy.Expanding))

    def heading_text(self) -> str:
        return "Heading"

    def begin_button_text(self) -> str:
        return "Begin"
