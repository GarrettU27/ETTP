from PyQt6.QtWidgets import QScrollArea, QFrame, QVBoxLayout


class ScrollablePage(QScrollArea):
    def __init__(self, widget):
        super().__init__()

        self.setWidgetResizable(True)
        self.setStyleSheet("* { border: none; }")

        self.frame = QFrame()
        self.frame.setLayout(QVBoxLayout())

        self.frame.layout().addWidget(widget)

        self.setWidget(self.frame)
