import random
from backend.get_ecg_from_db import Question
import io
class Testing_object():

    #Class variables, don't worry about these
    #They're just variables that the class needs to keep track of.
    svg_files = [io.BytesIO]
    arrhythmia = [Question]
    questions = 0
    answers = []
    correct = [str]
    correctAns = [bool]
    choices = [[str]]
    index_Q = 0
    index_SVG = 0

    #This function is run whenever a new test_object is created
    def __init__(self):
        answers = []

    #This function will get the next arrhythmia from the list and return the list of choices
    #If the list of arrhythmia is at the end, it will return a list of 4 "X" characters.
    #Applicable to the testing mode only really.
    def next_question(self):
        if self.index_Q != self.questions:
            choice_list = self.choices[self.index_Q].copy()
            self.index_Q += 1
            return choice_list
        else:
            return ["X","X","X","X"]
    
    #This function will get and return the next list of SVG bits.
    #These bits can be used with the self.qsw.load() function 
    def get_next_svg(self):
        next_svg = self.svg_files[self.index_SVG]
        self.index_SVG += 1
        return next_svg
    #This function will add a list of answers to the 
    def add_answers(self,q_ans):
        self.answers.append(q_ans)
    
    #This function checks the answers agains the passed in arrhythmia to check it's correctness
    def check_answers(self):
        self.correctAns = []
        for i in range(self.questions):
            if self.correct[i] == self.answers[i]:
                self.correctAns.append(True)
            else:
                self.correctAns.append(False)

    #Returns the number of questions
    def get_questions(self):
        return self.questions
    
    #Returns the list of arhythmia
    def get_arrhythmia(self):
        return self.arrhythmia
    
    #Returns the list of answers
    def get_answers(self):
        return self.answers
    
    #Returns the list of correct answers
    def get_correct(self):
        return self.correct
    
    def set_arrhythmia(self,arrhythmia):
        self.arrhythmia = arrhythmia.copy()
        
    def update_object(self):
        self.index_Q = 0
        self.index_SVG = 0
        self.questions = len(self.arrhythmia)
        self.correct = []
        self.svg_files = []
        self.choices = []
        for i in range(len(self.arrhythmia)):
            self.svg_files.append(self.arrhythmia[i].ecg)
            self.choices.append(self.arrhythmia[i].choices)
            self.correct.append(self.arrhythmia[i].correct_answer)
    
            
        
        
            
