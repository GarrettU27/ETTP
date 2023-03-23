from backend.get_ecg_from_db import get_training_questions, get_testing_questions
from pages.start_new.start_new import StartNew
from Logic.testing import Testing_object

global testing_questions
class StartNewTesting(StartNew):
    def __init__(self, set_state, testing_questions: Testing_object):
        super().__init__(set_state)
        testing_questions = Testing_object
    def begin(self):
        questions = get_testing_questions(self.get_arrhythmias(), int(self.question_number.currentText()))
        testing_questions.set_arrhythmia(self.testing_questions,questions)
        testing_questions.update_object(self.testing_questions)
        testing_questions.next_question(self.testing_questions)
        self.set_state()

    def heading_text(self) -> str:
        return "Test"

    def paragraph_text(self) -> str:
        return "Select which arrhythmias you want to be tested on"

    def begin_button_text(self) -> str:
        return "Begin Test"
