import PyQt6
import PyQt6.QtCore
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QSpacerItem, QHBoxLayout, QComboBox
from arrhythmia import supported_arrhythmias
from components.heading_label import HeadingLabel
from components.main_button import MainButton
from components.main_checkbox import MainCheckbox
from pages.start_new.start_new import StartNew


class StartNewTesting(StartNew):
    def __init__(self):
        super().__init__()

    def heading_text(self) -> str:
        return "What Do You Want to be Tested On?"

    def begin_button_text(self) -> str:
        return "Begin Test"
