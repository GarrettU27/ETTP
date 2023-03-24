from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QWidget, QVBoxLayout


class TestingResults(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

    def update_page(self, answers, correct):
        for answer, correct in zip(answers, correct):
            if answer == correct:
                answer_result = QLabel("Correct! Arrhythmia shown: " + str(answer))
                self.layout.addWidget(answer_result)
            else:
                answer_result = QLabel(
                    "Incorrect! Arrhythmia answered: " + str(answer) + " Correct arrhythmia: " + str(correct))
                self.layout.addWidget(answer_result)

    def clear_page(self):

        # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt

        # Too lazy am I? Too Bad!
        for i in reversed(range(self.layout.count())):
            widgetToRemove = self.layout.itemAt(i).widget()
            # remove it from the layout list
            self.layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
