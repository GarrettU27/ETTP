from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QIcon, QPixmap, QScreen
from PyQt6.QtCore import Qt
import sys
from generate_ecg_plot import get_ecg_png, get_ecg_svg


class Window(QWidget):
    def __init__(self):
        super().__init__()
        screenSize = self.screen().availableGeometry().size() * (3/4)

        self.resize(screenSize.width(), screenSize.height())
        self.setWindowTitle("ETTP")
        self.setWindowIcon(QIcon("icon.jpg"))

        layout = QVBoxLayout()
        self.setLayout(layout)

        qsw = QSvgWidget()
        qsw.load(get_ecg_svg())
        qsw.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(qsw)



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())