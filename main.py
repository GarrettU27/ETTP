# https://www.riverbankcomputing.com/software/pyqt/
# https://pypi.org/project/neurokit2/

from PyQt6.QtWidgets import QApplication
import sys
from mainwindow import MainWindow


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())