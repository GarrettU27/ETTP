from components.main_button import MainButton


class ChoiceButton(MainButton):
    def __init__(self, text):
        super().__init__(text)

        self.setObjectName("test_choice")
