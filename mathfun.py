#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import random
import pango
import Timer

class Question:
    
    def __init__(self):
        
        operation = random.choice([' + ', ' - ', ' * ', '/'])
        operand1 = random.randint(1,50)
        operand2 = random.randint(1,50) 
        if(operation == '/'):
            temp = str(float(operand1)) + operation + str(float(operand2))
            self.ans = round(eval(temp),2)
        else:
            temp = str((operand1)) + operation + str((operand2))
            self.ans = eval(temp)
        self.Q = temp + " = ?"
        choices = [self.ans]
        choices.append(self.ans + random.randint(1,50))
        choices.append(self.ans - random.randint(1,50))
        choices.append(self.ans + random.randint(1,50) - random.randint(1,50))
        choices = set(choices)
        while(len(choices) < 4):
            choices.add((self.ans + random.randint(1,50) - random.randint(1,50)) % int(self.ans))            
        choices = list(choices)
        random.shuffle(choices)
        self.ans = str(self.ans)
        self.A = str(choices[0])
        self.B = str(choices[1])
        self.C = str(choices[2])
        self.D = str(choices[3])
        self.answered = False

    def set_answered(self,value):
        assert(value == True or value == False) 
        self.answered = value
        
    def get_answered(self):
        return self.answered

class Base:

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def text_change(self,widget):
        self.quest_label.set_text(self.question.Q)

    def update_score(self, value):
        if(self.question.get_answered() is False):
            self.question.set_answered(True)
            self.attempts += 1
            if(value):
                self.correct += 1
            self.score = float(self.correct) / float(self.attempts)
            self.num_attempts.set_text(str(self.attempts))
            self.num_correct.set_text(str(self.correct))
            self.num_score.set_text(str(round(self.score*100,2)))
            
            
    def update_question(self, widget):
        q = Question()
        self.quest_label.set_text(q.Q)
        self.A_button.set_label(q.A)
        self.B_button.set_label(q.B)
        self.C_button.set_label(q.C)
        self.D_button.set_label(q.D)
        self.question = q
        self.choices = [self.A_button.child, self.B_button.child, self.C_button.child, self.D_button.child]
        map(lambda b: b.modify_font(pango.FontDescription("Arial 10")), self.choices)
        

    def check_answer(self, widget):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        box = gtk.Fixed()
        window.add(box)
        window.set_title("")
        window.set_size_request(100,100)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_resizable(False)
        button = gtk.Button("Okay")
        button2 = gtk.Button("Quit")
        box.put(button, 17, 50)
        box.put(button2, 52,50)
        button.connect("clicked", lambda x: window.destroy())
        button2 .connect("clicked", self.destroy)
        if(widget.get_label() == self.question.ans):
            self.update_score(True)
            box.put(gtk.Label("Correct! :)"), 25, 25)          
            window.connect("destroy", self.update_question)
            window.show_all()           
        else:
            self.update_score(False)
            box.put(gtk.Label("Try again! :("), 25, 25)
            window.show_all()       

    def __init__(self):

        """Create the results viewer"""
        self.attempts =  self.correct =  self.score = 0
        self.results_box = gtk.HBox()
        self.correct_label = gtk.Label("Correct")
        self.attempts_label = gtk.Label("Attempts")
        self.score_label = gtk.Label("Score (%)")
        self.num_correct = gtk.Label(self.correct)
        self.num_attempts = gtk.Label(self.attempts)
        self.num_score = gtk.Label(self.score)


        self.correct_frame = gtk.Frame("Correct")
        self.correct_frame.add(self.num_correct)
        self.attempt_frame = gtk.Frame("Attempts")
        self.attempt_frame.add(self.num_attempts)
        self.score_frame = gtk.Frame("Score")
        self.score_frame.add(self.num_score)

        self.results_box.pack_start(self.correct_frame)
        self.results_box.pack_start(self.attempt_frame)
        self.results_box.pack_start(self.score_frame)      
        
        self.question = Question()
        self.window =  gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(250,250)
        self.window.set_resizable(False)
        self.window.set_title("Math Fun!")
        
        """Table composed of two HBox's"""
        self.TopBox = gtk.HBox()
        self.TopBox.set_homogeneous(True)
        self.BotBox = gtk.HBox()
        self.BotBox.set_homogeneous(True)
        
        """Make a Label for the Question"""
        self.QueBox =gtk.HBox()
        self.quest_label = gtk.Label(self.question.Q)
        self.quest_label.modify_font(pango.FontDescription("Arial 13"))
        self.quest_frame = gtk.Frame("Question")
        self.quest_frame.add(self.quest_label)
        self.QueBox.pack_start((self.quest_frame))
        
        """Create the choice buttons"""
        self.A_button = gtk.Button(self.question.A)
        self.A_button.connect("clicked", self.check_answer)
        self.B_button = gtk.Button(self.question.B)
        self.B_button.connect("clicked", self.check_answer)
        self.C_button = gtk.Button(self.question.C)
        self.C_button.connect("clicked", self.check_answer)
        self.D_button = gtk.Button(self.question.D)
        self.D_button.connect("clicked", self.check_answer)
        self.choices = [self.A_button.child, self.B_button.child, self.C_button.child, self.D_button.child]
        map(lambda b: b.modify_font(pango.FontDescription("Arial 10")), self.choices)
        
        """Pack the choice buttons"""
        self.TopBox.pack_start(self.A_button)
        self.TopBox.pack_start(self.B_button)
        self.BotBox.pack_start(self.C_button)
        self.BotBox.pack_start(self.D_button)
        self.choice_box = gtk.VBox()
        self.choice_box.pack_start(self.TopBox)
        self.choice_box.pack_start(self.BotBox)
        self.choices_frame = gtk.Frame("Choices")
        self.choices_frame.add(self.choice_box)

        """Make WIndow Box"""
        self.WinBox = gtk.VBox()
        self.WinBox.pack_start(self.results_box)
        self.WinBox.set_homogeneous(False)
        self.WinBox.pack_start(self.QueBox)
        self.WinBox.pack_start(self.choices_frame)

        """Place boxes in the window"""
        self.window.add(self.WinBox)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def main(self):
        gtk.main()

if(__name__=="__main__"):
    base = Base()
    base.main()


  
    
  
