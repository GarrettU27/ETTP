# https://www.pythonguis.com/tutorials/pyqt6-animated-widgets/
# https://stackoverflow.com/questions/72054664/pyqt6-animation-doesnt-work-for-decreasing-width

from PyQt6.QtWidgets import QListWidget, QTreeWidget
from PyQt6 import QtCore


class BurgerMenu(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setStyleSheet("""* { 
            font-size: 20px; 
            border: none; 
            font-family: 'Encode Sans'; 
            border-width: 0 2px 0 0;
            border-color: #ddd;
            border-style: solid; 
        }
        """)
        self.openWidth = self.sizeHint().width()

        self.animation = QtCore.QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(125)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self.ensure_proper_size)

        self.setMinimumWidth(self.openWidth)
        self.setMaximumWidth(self.openWidth)

        self.isOpen = True

    def toggle(self):
        if self.isOpen:
            self.burger_close()
        else:
            self.burger_open()

        self.isOpen = not self.isOpen

    def burger_open(self):
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.openWidth)
        self.animation.start()

    def burger_close(self):
        self.setMinimumWidth(0)
        self.animation.setStartValue(self.openWidth)
        self.animation.setEndValue(0)
        self.animation.start()

    def ensure_proper_size(self):
        if self.isOpen:
            self.setMinimumWidth(self.openWidth)
