import io
from typing import List, Callable

import PyQt6
from PyQt6.QtCore import Qt, pyqtSlot, QThreadPool, QRunnable, QMetaObject, Q_ARG
from PyQt6.QtGui import QColor
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout

from backend.generate_ecg_plot import create_test_ecg
from backend.get_ecg_from_db import Flashcard
from components.heading_label import HeadingLabel
from components.main_button import MainButton
from components.paragraph_label import ParagraphLabel
from components.waiting_spinner_widget import QtWaitingSpinner


class TrainingFlashcards(QWidget):
    current_flashcard = 0
    total_flashcards: int
    flashcards: List[Flashcard]

    def __init__(self, set_state: Callable):
        super().__init__()
        self.set_state = set_state

        self.qsw = QSvgWidget()
        self.qsw.setSizePolicy(PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
                               PyQt6.QtWidgets.QSizePolicy.Policy.Expanding)

        self.title = HeadingLabel("Train")
        self.arrhythmia_name = ParagraphLabel("Normal Sinus Rhythm", 40)

        self.spinner = QtWaitingSpinner(self, True, True)

        self.spinner.setRoundness(70.0)
        self.spinner.setMinimumTrailOpacity(15.0)
        self.spinner.setTrailFadePercentage(70.0)
        self.spinner.setNumberOfLines(12)
        self.spinner.setLineLength(10)
        self.spinner.setLineWidth(5)
        self.spinner.setInnerRadius(10)
        self.spinner.setRevolutionsPerSecond(2.5)
        self.spinner.setColor(QColor(0, 0, 0))

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(30)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.qsw)
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

        self.next_button = MainButton("Next")
        self.layout.addWidget(self.next_button)
        self.next_button.clicked.connect(self.show_next_flashcard)

        self.spinner.raise_()

    def start_new_training(self, flashcards: List[Flashcard]):
        self.flashcards = flashcards
        self.reset_training()

    def reset_training(self):
        self.total_flashcards = len(self.flashcards)
        self.current_flashcard = 0
        self.load_flashcard()

    def show_next_flashcard(self):
        self.current_flashcard += 1
        if self.current_flashcard >= self.total_flashcards:
            self.set_state()
        else:
            self.load_flashcard()

    def load_flashcard(self):
        self.spinner.start()
        load_test_ecg = LoadTrainingECG(self)
        QThreadPool.globalInstance().start(load_test_ecg)

    @pyqtSlot(io.BytesIO)
    def show_flashcard(self, data):
        self.spinner.stop()
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

        self.qsw.load(data)
        self.qsw.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)


# https://gist.github.com/eyllanesc/1a09157d17ba13d223c312b28a81c320
class LoadTrainingECG(QRunnable):
    def __init__(self, training_flashcards: TrainingFlashcards):
        QRunnable.__init__(self)
        self.training_flashcards = training_flashcards

    def run(self):
        ecg = create_test_ecg(self.training_flashcards.flashcards[self.training_flashcards.current_flashcard].ecg)
        QMetaObject.invokeMethod(self.training_flashcards, "show_flashcard", Qt.ConnectionType.QueuedConnection,
                                 Q_ARG(bytes, ecg))
