# https://www.pythonguis.com/tutorials/pyqt6-animated-widgets/
# https://stackoverflow.com/questions/72054664/pyqt6-animation-doesnt-work-for-decreasing-width

from PyQt6.QtWidgets import QListWidget
from PyQt6 import QtCore


class BurgerMenu(QListWidget):
    def __init__(self, width):
        super().__init__()

        self.animation = QtCore.QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(125)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)

        self.openWidth = width
        self.setMaximumWidth(self.openWidth)
        self.isOpen = True

    def toggle(self):
        if self.isOpen:
            self.burger_open()
        else:
            self.burger_close()

        self.isOpen = not self.isOpen

    def burger_close(self):
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.openWidth)
        self.animation.start()

    def burger_open(self):
        self.animation.setStartValue(self.openWidth)
        self.animation.setEndValue(0)
        self.animation.start()
