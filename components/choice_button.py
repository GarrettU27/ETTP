from components.main_button import MainButton


class ChoiceButton(MainButton):
    def __init__(self, text, font_size=40):
        super().__init__(text, font_size)

        self.setObjectName("test_choice")
