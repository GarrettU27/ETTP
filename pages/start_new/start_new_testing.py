from pages.start_new.start_new import StartNew


class StartNewTesting(StartNew):
    def __init__(self, set_state):
        super().__init__(set_state)

    def heading_text(self) -> str:
        return "Test"

    def paragraph_text(self) -> str:
        return "Select which arrhythmias you want to be tested on"

    def begin_button_text(self) -> str:
        return "Begin Test"
