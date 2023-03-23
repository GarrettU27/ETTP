import PyQt6
import json
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QGridLayout

from generate_ecg_plot import get_ecg_svg
import qtawesome as qta

##from testing.py
import random
#from backend.get_ecg_from_db import Question
import io
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout
from PyQt6.QtSvgWidgets import QSvgWidget

##from testing_questions.py
from components.heading_label import HeadingLabelTest
from components.choice_button import ChoiceButtonLeft,ChoiceButtonRight
from backend.generate_ecg_plot import get_ecg_svg
from Logic.testing import Testing_object

#do we need global variables for the JSON dictonary to work?
NormalSinusRhythm = np.array([]) #global variable
SinusBradycardia = np.array([]) #global variable
SinusTachycardia = np.array([]) #global variable
AtrialFibrillation = np.array([]) #global variable
AtrialFlutter = np.array([]) #global variable
FirstDegreeAVBlock = np.array([]) #global variable

##from testing.py
class Training_object():
    svg_files = [io.BytesIO]
    # class variable for each trainig object, stores arrythmia list
    #arrhythmia = [Question]
    index_Q = 0
    index_SVG = 0

    def __init__(self):
        
        #This function will get the next arrhythmia from the list
        def next_question(self):
            if self.index != self.questions:
                choice_list = self.choices.copy()
                return choice_list
            else:
                return ["X","X","X","X"]
    
        def get_next_svg(self):
            next_svg = self.svg_files[self.index_SVG]
            self.index_SVG += 1
            return next_svg
        #This function will add a list of answers to the 
        def add_answers(self,q_ans):
            self.answers.append(q_ans)
    
        #This function checks the answers agains the passed in arrhythmia to check it's correctness
        def check_answers(self):
            for i in range(self.questions):
                if self.arhythmia == self.answers:
                    self.correct.append(True)
                else:
                    self.correct.append(False)

        #Returns the number of questions
        def get_questions(self):
            return self.questions
    
        #Returns the list of arhythmia
        def get_arrhythmia(self):
            return self.arrhythmia
        
        def set_arrhythmia(self,arrhythmia):
            self.arrhythmia = arrhythmia.copy()
        
        def update_object(self):
            self.index_Q = 0
            self.index_SVG = 0
            self.svg_files = []
            for i in range(len(self.arrhythmia)):
                self.svg_files.append(self.arrhythmia[i].ecg)
 
        
##Marie's training code
class Training(QWidget):
    train_object = Training_object
    ECG_data = []
    def __init__(self):
        super().__init__()
        
        # read file
        with open('HRData.json', 'r') as myfile:
            self.data=myfile.read()
        # parse file
        self.obj = json.loads(self.data) #an array of dictionaries
        #print(type(self.obj))

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.button = QPushButton("I AM TRAINING PAGE")
        self.text = QLabel("Hello World")

        self.qsw = QSvgWidget()
        self.qsw.load(get_ecg_svg())
        self.qsw.renderer().setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        #self.layout.addWidget(qsw)
    
        self.setupTxtBox()
                
        #self.choices = self.test_object.next_question()
       
    def update_nextQ(self,item):
        #self.train_object.add_answers(item.text())
        #self.choices = self.train_object.next_question()
        #if self.choices[0] == "X":
        #    return -1
        #else:
            self.qsw.load(self.train_object.get_next_svg())
            self.title.setText("Question " + self.train_object.index+1)
            self.next.setText(self)
            #self.answer2.setText(self.choices[1])
            #self.answer3.setText(self.choices[2])
            #self.answer4.setText(self.choices[3])
    
    def set_ecg_data(self,ecg_stuff):
        self.ECG_data = ecg_stuff.copy()
        self.train_object.set_arrhythmia(self.ECG_data)
        self.train_object.update_object()
    
    def start_train(self):
        self.choices = self.train_object.next_question()
        self.title.setText("Question " + self.train_object.index+1)
        self.qsw.load(self.train_object.get_next_svg())
        self.next.setText(self)
        #self.answer2.setText(self.choices[1])
        #self.answer3.setText(self.choices[2])
        #self.answer4.setText(self.choices[3])

    def setupTxtBox(self):
        
        #this is where the physionet code for the displayed ECG is called,  
        #and the related data is pulled from the JSON dictorary
        inputArr = 427084000	 #Sinus Tachycardia

        ##maybe Qlabel instead of Qlineedit?
        #self.textboxTitle = QLineEdit('You are Currently Training')
        #self.textboxSubtitle = QLineEdit('Hit the space bar to proceed to the next ECG strip')
        
        ##get all of the necessary files required for creating the training object here
        #load in the SVG data stream
        self.textboxTitle = HeadingLabelTest("You are Currently Training")
        self.textboxSubtitle = QLineEdit('Hit the space bar to proceed to the next ECG strip')
        self.next = NextButton(self)
        #self.answer2 = ChoiceButtonRight(self.choices[1])
        #self.answer3 = ChoiceButtonLeft(self.choices[2])
        #self.answer4 = ChoiceButtonRight(self.choices[3])
        self.next.clicked.connect(lambda: self.update_nextQ(self))
        #self.answer2.clicked.connect(lambda: self.update_nextQ(self.answer2))
        #self.answer3.clicked.connect(lambda: self.update_nextQ(self.answer3))
        #self.answer4.clicked.connect(lambda: self.update_nextQ(self.answer4))
        #self.next = QPushButton(self)
        
        #print("Data: " + str(self.data))
        #print("OBJ: " + str(self.obj))
        #calling data from json dictionary
        for x in self.obj:
            if x['PhysionetCode']==inputArr:
                print("Inside if")
                thisdict = {
                    x['RhythmName'],
                    x['HeartRate_bpm'],
                    x['Rhythm'],
                    x['P-wave'],
                    x['PRInterval_seconds'],
                    x['QRSComplex_seconds'],
                    x['Notes'],
                 }
                print(thisdict)
                self.textboxRhythmName = QLineEdit(x['RhythmName'])
                self.textboxHR = QLineEdit('Heart Rate (bpm): ' + x['HeartRate_bpm'])
                self.textboxRhy = QLineEdit('Rhythm: ' +x['Rhythm'])
                self.textboxPwav = QLineEdit('P-wave: '+ x['P-wave'])
                self.textboxPRint = QLineEdit('PR Interval (seconds): ' + x['PRInterval_seconds'])
                self.textboxQRScom = QLineEdit('QRS Complex (seconds): ' + x['QRSComplex_seconds'])
                self.textboxNotes = QLineEdit('Notes: ' + x['Notes'])
                print(inputArr)
        print(x)

        box = QGridLayout()
        #add ECG graph widget here first
        #box.addWidget(self.get_ecg_png(), 0, 0)
        #box.addWidget(self.textboxTitle, 1, 0)
        #box.addWidget(self.textboxSubtitle, 2, 0)
        #box.addWidget(self.qsw, 3, 0)
        #box.addWidget(self.textboxRhythmName, 4, 0)
        #box.addWidget(self.textboxHR, 5, 0)
        #box.addWidget(self.textboxRhy, 6, 0)
        #box.addWidget(self.textboxPwav, 7, 0)
        #box.addWidget(self.textboxPRint, 5, 4)
        #box.addWidget(self.textboxQRScom, 6, 4)
        #box.addWidget(self.textboxNotes, 7, 4)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.title,0,0,1,2)
        self.layout.addWidget(self.subtitle,0,1,1,2)
  
        self.layout.addWidget(self.qsw, 2, 0, 5, 2)
        self.addWidget(self.textboxRhythmName, 6,0,1,2)
        self.addWidget(self.textboxHR, 6,2,1,2)
        self.addWidget(self.textboxRhy, 6, 3,1,2)
        self.addWidget(self.textboxPwav, 7, 4,1,2)
        self.addWidget(self.textboxPRint, 7,5,1,2)
        self.addWidget(self.textboxQRScom, 7,1,1,2)
        self.addWidget(self.textboxNotes, 7,2,1,2)
        self.layout.addWidget(self.next,7,3,1,2)

        self.start_train()
        self.setLayout(box)
