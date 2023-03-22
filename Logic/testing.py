import random
class Testing_object():
    svg_files = []
    arrhythmia = []
    questions = 0
    answers = []
    correct = []
    choices = []
    index_Q = 0
    index_SVG = 0

    def __init__(self):
        answers = []

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
        self.correct = []
        self.svg_files = []
        self.choices = []
        for i in range(len(self.arrhythmia)):
            self.svg_files.append(self.arrhythmia[i][0])
            self.choices.append(self.arrhythmia[i][1])
            self.correct(self.arrhythmia[i][2])
    
            
        
        
            
