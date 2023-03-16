from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout


class StartNewTraining(QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QPushButton("Go to home")
        self.text = QLabel("Hello World")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)