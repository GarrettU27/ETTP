from components.main_button import MainButton


class MainCheckbox(MainButton):
    def __init__(self, text, font_size=30):
        super().__init__(text, font_size)

        self.setChecked(False)
        self.setCheckable(True)
