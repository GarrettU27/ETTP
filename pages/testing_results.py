from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QLabel

class TestingResults(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        


    def update_page(self,questions,answers,correct,correctAns):
        for i in range(questions):
            if correctAns[i]:
                myWidget = QLabel("Correct! Arrhythmia shown: " + str(answers[i]))
                self.layout.addWidget(myWidget)
            else:
                myWidget = QLabel("Incorrect! Arrhythmia answered: " + str(answers[i]) + " Correct arrhythmia: " + str(correct[i]))
                self.layout.addWidget(myWidget)
        
    
    def clear_page(self):

        #https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt

        #Too lazy am I? Too Bad!
        for i in reversed(range(self.layout.count())): 
            widgetToRemove = self.layout.itemAt(i).widget()
            # remove it from the layout list
            self.layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)