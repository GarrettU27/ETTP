from PyQt6.QtWidgets import QWidget, QStackedWidget
from pages.start_new.start_new_testing import StartNewTesting
from pages.testing_questions import TestingQuestions
from pages.testing_results import TestingResults


class Testing(QWidget):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget(self)

        self.start_new = StartNewTesting()
        self.stacked_widget.addWidget(self.start_new)

        self.testing_questions = TestingQuestions()
        self.stacked_widget.addWidget(self.testing_questions)

        self.testing_results = TestingResults()
        self.stacked_widget.addWidget(self.testing_results)

        self.start_new.begin_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.testing_questions))
