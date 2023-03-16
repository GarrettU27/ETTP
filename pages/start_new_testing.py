import PyQt6
import PyQt6.QtCore
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QSpacerItem, QHBoxLayout, QComboBox
from arrhythmia import supported_arrhythmias
from components.heading_label import HeadingLabel
from components.main_button import MainButton
from components.main_checkbox import MainCheckbox


class StartNewTesting(QWidget):
    def __init__(self):
        super().__init__()

        self.heading = HeadingLabel("What Do You Want to be Tested On?")

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.heading, 0, 0)

        for index, arrhythmia in enumerate(supported_arrhythmias):
            self.layout.addWidget(MainCheckbox(arrhythmia.name), index + 1, 0)

        submission_row = QWidget()
        submission_row.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.MinimumExpanding, PyQt6.QtWidgets.QSizePolicy.Policy.MinimumExpanding)

        submission_layout = QHBoxLayout(submission_row)
        question_number = QComboBox()
        question_number.addItems(str(num) for num in range(10))
        submission_layout.addWidget(question_number)

        submission_layout.addWidget(MainButton("Begin Test"))

        submission_layout.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignVCenter)

        submission_row.setLayout(QHBoxLayout(submission_row))

        self.layout.addWidget(submission_row, len(supported_arrhythmias) + 1, 0)
