from typing import List, Callable

from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout

from backend.get_ecg_from_db import Flashcard
from components.ecg_plot import ECGPlot
from components.heading_label import HeadingLabel
from components.main_button import MainButton
from components.paragraph_label import ParagraphLabel


class TrainingFlashcards(QWidget):
    current_flashcard = 0
    total_flashcards: int
    flashcards: List[Flashcard]

    def __init__(self, set_state: Callable):
        super().__init__()
        self.set_state = set_state

        self.ecg_plot = ECGPlot()
        self.title = HeadingLabel("Train")
        self.arrhythmia_name = ParagraphLabel("Normal Sinus Rhythm", 40)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.ecg_plot)
        self.layout.addWidget(self.arrhythmia_name)

        self.grid = QGridLayout()
        self.bpm_label = ParagraphLabel("Heart Rate (bpm):")
        self.rhythm_label = ParagraphLabel("Rhythm:")
        self.p_wave_label = ParagraphLabel("P Wave:")
        self.pr_label = ParagraphLabel("PR Interval (seconds):")
        self.qrs_label = ParagraphLabel("QRS Complex (seconds):")
        self.note_label = ParagraphLabel("Note:")

        self.grid.addWidget(self.bpm_label, 0, 0)
        self.grid.addWidget(self.rhythm_label, 1, 0)
        self.grid.addWidget(self.p_wave_label, 2, 0)
        self.grid.addWidget(self.pr_label, 0, 1)
        self.grid.addWidget(self.qrs_label, 1, 1)
        self.grid.addWidget(self.note_label, 2, 1)
        self.grid.setSpacing(15)

        self.layout.addLayout(self.grid)

        self.card_movement_row = QHBoxLayout()
        self.card_movement_row.setSpacing(30)

        self.previous_button = MainButton("Previous")
        self.card_movement_row.addWidget(self.previous_button)
        self.previous_button.clicked.connect(self.show_previous_flashcard)

        self.next_button = MainButton("Next")
        self.card_movement_row.addWidget(self.next_button)
        self.next_button.clicked.connect(self.show_next_flashcard)

        self.layout.addLayout(self.card_movement_row)

    # As far as I can tell, compresses things down by hinting it should be
    # at maximum the screen's height
    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        self.setMaximumHeight(self.screen().geometry().height())

    def start_new_training(self, flashcards: List[Flashcard]):
        self.flashcards = flashcards
        self.reset_training()

    def reset_training(self):
        self.total_flashcards = len(self.flashcards)
        self.current_flashcard = 0
        self.show_flashcard()

    def show_next_flashcard(self):
        self.current_flashcard += 1
        if self.current_flashcard >= self.total_flashcards:
            self.set_state()
        else:
            self.show_flashcard()

    def show_previous_flashcard(self):
        self.current_flashcard -= 1
        if self.current_flashcard < 0:
            self.current_flashcard = 0
        self.show_flashcard()

    def show_flashcard(self):
        self.adjustSize()

        current_card = self.flashcards[self.current_flashcard]

        self.title.setText(f"Train - Card {str(self.current_flashcard + 1)}/{str(self.total_flashcards)}")
        self.arrhythmia_name.setText(current_card.arrhythmia_annotation.rhythm_name)

        self.bpm_label.setText(f"Heart Rate (bpm): {current_card.arrhythmia_annotation.bpm}")
        self.rhythm_label.setText(f"Rhythm: {current_card.arrhythmia_annotation.rhythm}")
        self.p_wave_label.setText(f"P Wave: {current_card.arrhythmia_annotation.p_wave}")
        self.pr_label.setText(f"PR Interval (seconds): {current_card.arrhythmia_annotation.pr_interval}")
        self.qrs_label.setText(f"QRS Complex (seconds): {current_card.arrhythmia_annotation.qrs_complex}")
        self.note_label.setText(f"Note: {current_card.arrhythmia_annotation.note}")

        if self.current_flashcard == 0:
            self.previous_button.setEnabled(False)
        else:
            self.previous_button.setEnabled(True)

        self.ecg_plot.plot_ecg(self.flashcards[self.current_flashcard].ecg)
