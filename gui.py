from tkinter import *
import requests
import random
import socket
import json
import re
    
#create instance of tKinter window
window = Tk()
#Changes text on top bar of window, next to icon
window.title("Quiz App made with Tkinter")
window.geometry("1000x700")

class Quiz():
    # method for game logic - driver code
    def __init__(self, param, data):
        self.gameWindow = Tk()
        self.score = 0
        self.totalPossible = param["amount"]
        self.gameData = data
        self.correctAnswer = None
        self.questions=[]
        self.correctAnswers=[]
        self.wrongAnswers=[]
        self.options=[]
        self.i = 0
        self.clickedNumber = 0
        self.userAnswer = StringVar(self.gameWindow)
        self.game(self.gameData)
        
    def game(self, data):
        self.gameWindow.title("Welcome to the Quiz")
        for item in data:
            correctAnswer = item["correct_answer"]
            wrongAnswers= item["incorrect_answers"]
            options = wrongAnswers + [correctAnswer]
            strippedQuestion = self.cleanerHTML(item["question"])
            strippedr = self.cleanerHTML(correctAnswer)
            self.questions.append(strippedQuestion)
            self.correctAnswers.append(strippedr)
            self.wrongAnswers.append(wrongAnswers)
            self.options.append(options)  
        self.next()
        self.gameWindow.mainloop()
      
    def next(self):
        frame=Frame(self.gameWindow, width=500, height=500)
        frame.pack(side="top", expand=True, fill="both")
        if self.i < len(self.questions):
            self.correctAnswer = self.correctAnswers[self.i]
            questionLabel = Label(frame, text= self.questions[self.i]).pack()
            self.radioButtons(self.options[self.i], frame)
            self.i+=1
        else:
            frame.destroy()
            frame=Frame(self.gameWindow, width=500, height=500)
            frame.pack(side="top", expand=True, fill="both")
            self.microservice(frame)


    def microservice(self, frame):
        s = socket.socket()
        host = 'localhost'
        port = 8005
        s.connect((host, port))
        data = str(self.score)+"/"+str(self.totalPossible)
        data = data.encode("utf8")
        s.send(data)
        ret = s.recv(1024).decode()
        questionLabel = Label(frame, text=f"Your Score is {ret}%").pack()
        questionLabel = Label(frame, text="Thanks for Playing!").pack()
        exitButton = Button(frame, text="Exit", command=self.gameWindow.destroy)
        exitButton.pack()
        s.close()
            
    def cleanerHTML(self, str):
        '''Method cleans up the HTML marks in JSON file'''
        CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        return re.sub(CLEANR,"",str)
            
    def quizSubmit(self, value, frame):
        if value == self.correctAnswer:
            self.score+=1
        frame.destroy()
        self.next()
                         
    def radioButtons(self,options,frame):
        random.shuffle(options)
        for item in options:
            strippedOption = self.cleanerHTML(item)
            Radiobutton(frame, 
                        indicatoron=0,
                        width=40,
                        padx=10, 
                        text=strippedOption, 
                        variable=self.userAnswer, 
                        value=strippedOption,
                        command=lambda: self.quizSubmit(self.userAnswer.get(), frame)).pack()
    
            
    
# method to submit the quiz form    
def formSubmit():
    type = clickType.get()
    if type == "True/False":
        type = "boolean"
    elif type == "Multiple Choice":
        type = "multiple"
    categoryCode = 0    
    i = 9
    j = 0
    while i <= 32:
        #print(categories_list[j])
        if categories_list[j] == clickCategory.get():
            categoryCode = i
        i+=1
        j+=1
                    
    parameters = {
        "amount" : numQuestions.get(),
        "category" : categoryCode,
        "difficulty" : clickDifficulty.get().lower(),
        "type" : type,
        #"encode" : "default"
    }
    response = requests.get(url="https://opentdb.com/api.php", params=parameters)
    question_data = response.json()["results"]
    quiz = Quiz(parameters, question_data)
    
# function controls pop up window for exit button
def exitClick():
    exitWindow = Tk()
    exitWindow.overrideredirect(1)
    frame1 = Frame(exitWindow, highlightbackground="red", highlightcolor="red", highlightthickness=2, background="#F0FFFF")
    frame1.pack()
    exitWindow.geometry("200x200+700+300")
    label1 = Label(frame1, text="Are you sure you want to exit?")
    label1.pack()
    yes = Button(frame1, text="Yes", background="#5F9EA0", command=quit)
    yes.pack()
    no = Button(frame1, text="No", background="#5F9EA0", command=exitWindow.destroy)
    no.pack()
    exitWindow.mainloop()


# Label widget (Introduction)
intro1 = Label(window, text="Welcome to the Quiz App", bg="#5F9EA0", width="700", height="2")
intro1.pack()
space1 = Label(window, width="700", height="2")
space1.pack()

# Quiz Form
prompt1 = Label(window, text="Please enter number of quiz questions you would like to be asked:", height="2")
prompt1.pack()

#request for # of questions
numQuestions = IntVar(window)      
numQuestions.set("Click for Options")
drop1 = OptionMenu(window,numQuestions,"1","5","10","15","20")
drop1.pack()

prompt2 = Label(window, text="Please select a quiz category:", height="2")
prompt2.pack()

#request for category data & drop down categories menu
categories = requests.get(url='https://opentdb.com/api_category.php')
json_categories = (categories.json())
categories_list=[]
for name in json_categories["trivia_categories"]:
    categories_list.append(name["name"])
clickCategory = StringVar(window)      
clickCategory.set("Click for Options")
drop1 = OptionMenu(window,clickCategory,*categories_list)
drop1.pack()


    #drop down for difficulty level
prompt3 = Label(window, text="Please choose a level of difficulty:", height="2")
prompt3.pack()
clickDifficulty = StringVar(window)
clickDifficulty.set ("Click for Options")
drop2 = OptionMenu(window,clickDifficulty,"Easy", "Medium", "Hard")
drop2.pack()

#drop down for question type
prompt4 = Label(window, text="Please choose a type of question:", height="2")
prompt4.pack()
clickType = StringVar()
clickType.set ("Click for Options")
drop3 = OptionMenu(window, clickType,"Multiple Choice", "True/False")
drop3.pack()
    
# submission button
submitButton = Button(window, text="Submit", padx=20, pady=10, command = formSubmit)
submitButton.pack()

# exit button
exitButton = Button(window, text="Exit", padx=20, pady=10, command = exitClick)
exitButton.pack()
    
# event loop for ui, loops gui
window.mainloop()