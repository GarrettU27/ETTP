import PyQt6
from PyQt6 import QtCore
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QVBoxLayout, QSpacerItem

from backend.arrhythmia_annotation import get_supported_arrhythmias
from components.heading_label import HeadingLabel
from components.main_button import MainButton
from components.main_checkbox import MainCheckbox
from components.paragraph_label import ParagraphLabel


class StartNew(QWidget):
    def __init__(self, set_state):
        super().__init__()

        self.heading = HeadingLabel(self.heading_text())
        self.heading.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                   PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)
        self.paragraph = ParagraphLabel(self.paragraph_text())
        self.paragraph.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                     PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.heading)
        self.layout.addWidget(self.paragraph)
        self.layout.setSpacing(30)

        self.set_state = set_state

        self.checkboxes = []

        for index, arrhythmia in enumerate(self.get_supported_arrhythmias()):
            checkbox = MainCheckbox(arrhythmia.rhythm_name)
            checkbox.clicked.connect(self.update_self)
            self.checkboxes.append((checkbox, arrhythmia.id))
            self.layout.addWidget(checkbox)

        submission_row = QWidget()
        submission_row.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Preferred,
                                     PyQt6.QtWidgets.QSizePolicy.Policy.Preferred)

        submission_layout = QHBoxLayout(submission_row)

        question_number_layout = QVBoxLayout()

        question_number_label = ParagraphLabel(self.number_text())
        question_number_layout.addWidget(question_number_label)

        self.question_number = QComboBox()
        self.question_number.addItems(str(num * 5) for num in range(1, 6))
        self.question_number.setCurrentIndex(2)

        question_number_layout.addWidget(self.question_number)
        question_number_layout.setSpacing(7)
        self.question_number.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.question_number.setStyleSheet("""
            QComboBox {
                font-family: "Encode Sans";
                border: 1px solid #ddd;
                padding: 0.4em;
                font-size: 25px;
                border-radius: 25%;
                margin: 0;
            }

            QComboBox::drop-down {
                border: none;
            }
            
            QComboBox::down-arrow {
                image: url(images:dropdown.png);
                padding-right: 40px;
            }
        """)

        submission_layout.addLayout(question_number_layout)

        self.begin_button = MainButton(self.begin_button_text())
        submission_layout.addWidget(self.begin_button)
        self.begin_button.setEnabled(False)
        self.begin_button.clicked.connect(self.begin)
        submission_layout.setSpacing(30)

        submission_layout.setAlignment(self.begin_button, PyQt6.QtCore.Qt.AlignmentFlag.AlignBottom)

        self.layout.addWidget(submission_row)
        self.layout.addSpacerItem(QSpacerItem(1, 1, PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                                              PyQt6.QtWidgets.QSizePolicy.Policy.Expanding))

    def begin(self):
        self.set_state()

    def update_self(self):
        self.begin_button.setEnabled(self.can_begin())

        if len(self.get_arrhythmias()) > 3:
            if self.question_number.count() == 4:
                current_choice = self.question_number.currentIndex()
            else:
                current_choice = self.question_number.currentIndex() - 1
            self.question_number.clear()
            self.question_number.addItems(str(num * 5) for num in range(2, 6))
            self.question_number.setCurrentIndex(max(current_choice, 0))
        else:
            if self.question_number.count() == 5:
                current_choice = self.question_number.currentIndex()
            else:
                current_choice = self.question_number.currentIndex() + 1
            self.question_number.clear()
            self.question_number.addItems(str(num * 5) for num in range(1, 6))
            self.question_number.setCurrentIndex(current_choice)

    def can_begin(self):
        return len(self.get_arrhythmias()) > 0

    def get_arrhythmias(self):
        arrhythmias = []

        for checkbox, arrhythmia_id in self.checkboxes:
            if checkbox.isChecked():
                arrhythmias.append(arrhythmia_id)

        return arrhythmias

    def get_supported_arrhythmias(self):
        return get_supported_arrhythmias()

    def heading_text(self) -> str:
        return "Heading"

    def paragraph_text(self) -> str:
        return "Paragraph"

    def begin_button_text(self) -> str:
        return "Begin"

    def number_text(self) -> str:
        return "Number"
