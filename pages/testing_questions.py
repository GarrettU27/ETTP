from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout
from PyQt6.QtSvgWidgets import QSvgWidget

from components.heading_label import HeadingLabelTest
from components.choice_button import ChoiceButtonLeft,ChoiceButtonRight
from backend.generate_ecg_plot import get_ecg_svg
from Logic.testing import Testing_object

class TestingQuestions(QWidget):
    test_object = Testing_object
    choices=["something","Is","Really","Wrong"]
    ECG_data = []
    def __init__(self):
        super().__init__()
        self.qsw = QSvgWidget()
        #self.choices = self.test_object.next_question()

        #get all of the necessary files required for creating the testing object here
    
        #load in the SVG data stream
        self.qsw.load(get_ecg_svg())
        self.qsw.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.title = HeadingLabelTest("Question")
        self.answer1 = ChoiceButtonLeft(self.choices[0])
        self.answer2 = ChoiceButtonRight(self.choices[1])
        self.answer3 = ChoiceButtonLeft(self.choices[2])
        self.answer4 = ChoiceButtonRight(self.choices[3])
        self.answer1.clicked.connect(lambda: self.update_nextQ(self.answer1))
        self.answer2.clicked.connect(lambda: self.update_nextQ(self.answer2))
        self.answer3.clicked.connect(lambda: self.update_nextQ(self.answer3))
        self.answer4.clicked.connect(lambda: self.update_nextQ(self.answer4))
        self.next = QPushButton(self)
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.title,0,0,1,2)
        self.layout.addWidget(self.answer1,6,0,1,2)
        self.layout.addWidget(self.answer2,6,2,1,2)
        self.layout.addWidget(self.answer3,7,0,1,2)
        self.layout.addWidget(self.answer4,7,2,1,2)
        self.layout.addWidget(self.qsw, 1, 0, 5, 2) 
        
        self.start_test()
    
    def update_nextQ(self,item):
        self.test_object.add_answers(item.text())
        self.choices = self.test_object.next_question()
        if self.choices[0] == "X":
            return -1
        else:
            self.qsw.load(self.test_object.get_next_svg())
            self.title.setText("Question " + self.test_object.index+1)
            self.answer1.setText(self.choices[0])
            self.answer2.setText(self.choices[1])
            self.answer3.setText(self.choices[2])
            self.answer4.setText(self.choices[3])

    
    def set_ecg_data(self,ecg_stuff):
        self.ECG_data = ecg_stuff.copy()
        self.test_object.set_arrhythmia(self.ECG_data)
        self.test_object.update_object()
    
    def start_test(self):
        self.choices = self.test_object.next_question()
        self.title.setText("Question " + self.test_object.index+1)
        self.qsw.load(self.test_object.get_next_svg())
        self.answer1.setText(self.choices[0])
        self.answer2.setText(self.choices[1])
        self.answer3.setText(self.choices[2])
        self.answer4.setText(self.choices[3])
    
    