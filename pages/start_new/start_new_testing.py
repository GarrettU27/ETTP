from backend.arrhythmia_annotation import get_supported_arrhythmias
from backend.get_ecg_from_db import get_testing_questions
from pages.start_new.start_new import StartNew
from pages.testing_questions import TestingQuestions


class StartNewTesting(StartNew):
    test_window = TestingQuestions

    def __init__(self, set_state, testing_questions: TestingQuestions):
        super().__init__(set_state)
        self.test_window = testing_questions

    def begin(self):
        questions = get_testing_questions(self.get_arrhythmias(), int(self.question_number.currentText()))
        self.test_window.start_new_test(questions)
        self.set_state()

    def get_supported_arrhythmias(self):
        all_supported_arrhythmias = get_supported_arrhythmias()

        # remove normal sinus rhythm
        return filter(lambda arrhythmia: arrhythmia.id != 54, all_supported_arrhythmias)

    def heading_text(self) -> str:
        return "Test"

    def paragraph_text(self) -> str:
        return "Select which arrhythmias you want to be tested on"

    def begin_button_text(self) -> str:
        return "Begin Test"

    def number_text(self) -> str:
        return "Choose number of questions"
