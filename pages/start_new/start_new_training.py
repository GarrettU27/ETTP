from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout

from pages.start_new.start_new import StartNew


class StartNewTraining(StartNew):
    def __init__(self):
        super().__init__()

    def heading_text(self) -> str:
        return "What Do You Want to be Trained On?"

    def begin_button_text(self) -> str:
        return "Begin Training"
