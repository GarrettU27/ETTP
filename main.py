# https://www.riverbankcomputing.com/software/pyqt/
# https://pypi.org/project/neurokit2/

from PyQt6.QtWidgets import QApplication
import sys
from window import Window


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())