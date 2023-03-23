import PyQt6

from components.main_button import MainButton


class MainCheckbox(MainButton):
    def __init__(self, text):
        super().__init__(text)

        self.setChecked(False)
        self.setCheckable(True)