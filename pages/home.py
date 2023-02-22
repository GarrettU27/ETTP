import PyQt6
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

from generate_ecg_plot import get_ecg_svg


class Home(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        qsw = QSvgWidget()
        qsw.load(get_ecg_svg())
        qsw.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(qsw)

        self.button = QPushButton("Go to welcome")
        self.text = QLabel("Hello World")

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.show()