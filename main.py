# https://www.riverbankcomputing.com/software/pyqt/
# https://pypi.org/project/neurokit2/
# Potentially useful: https://coderslegacy.com/python/pyqt6-css-stylesheets/

from PyQt6.QtWidgets import QApplication
import sys
from main_window import MainWindow


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())