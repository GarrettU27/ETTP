from pages.start_new.start_new import StartNew


class StartNewTraining(StartNew):
    def __init__(self):
        super().__init__()

    def heading_text(self) -> str:
        return "Train"

    def paragraph_text(self) -> str:
        return "Select which arrhythmias you want to learn how to identify"

    def begin_button_text(self) -> str:
        return "Begin Training"
