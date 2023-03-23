from PyQt6.QtWidgets import QWidget


class TestingQuestions(QWidget):
    def __init__(self):
        super().__init__()

    def set_ecg_data(self, questions):
        print(questions)
