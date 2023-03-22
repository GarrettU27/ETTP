from backend.get_ecg_from_db import get_training_questions
from pages.start_new.start_new import StartNew
from pages.training_questions import TrainingQuestions


class StartNewTraining(StartNew):
    def __init__(self, set_state, training_questions: TrainingQuestions):
        super().__init__(set_state)
        self.training_questions = training_questions

    def begin(self):
        questions = get_training_questions(self.get_arrhythmias(), int(self.question_number.currentText()))
        self.training_questions.set_ecg_data(questions)
        self.set_state()

    def heading_text(self) -> str:
        return "Train"

    def paragraph_text(self) -> str:
        return "Select which arrhythmias you want to learn how to identify"

    def begin_button_text(self) -> str:
        return "Begin Training"
