from backend.get_ecg_from_db import get_training_flashcards
from pages.start_new.start_new import StartNew
from pages.training_flashcards import TrainingFlashcards


class StartNewTraining(StartNew):
    def __init__(self, set_state, training_questions: TrainingFlashcards):
        super().__init__(set_state)
        self.training_questions = training_questions

    def begin(self):
        flashcards = get_training_flashcards(self.get_arrhythmias(), int(self.question_number.currentText()))
        self.training_questions.start_new_training(flashcards)
        self.set_state()

    def heading_text(self) -> str:
        return "Train"

    def paragraph_text(self) -> str:
        return "Select which arrhythmias you want to learn how to identify"

    def begin_button_text(self) -> str:
        return "Begin Training"

    def number_text(self) -> str:
        return "Choose number of cards"