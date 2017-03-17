from tkinter import *
import time
import ctypes

global start
global f

class Application(Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        #seperator
        self.line1 = Label(self, text="--------------EXAMINOR---------------")
        self.line1.pack()

        #User File Name
        self.lbl = Label(self, text="Enter File Name:")
        self.lbl.pack()
        self.file = Entry(self)
        self.file.pack()
        self.file.insert(0, "test1a.txt") #default file
        self.openFile = Button(self, text="OK", command=self.fileStart)
        self.openFile.pack()

        #seperator
        self.line = Label(self, text="----------------USER----------------")
        self.line.pack()

        #Start button initiates the timer 
        self.start = Button(self, text="START", command=self.start)
        self.start.pack(padx=5, pady= 20)

        #Entry field for word counts
        self.ent = Entry(self)
        self.ent.pack()
        self.submit = Button(self, text="SUBMIT", bg="yellow", command=self.enter)
        self.submit.pack()

        #Colour buttons
        self.blue = Button(self, text="BLUE", fg="blue", bg="blue", height=5, width=10)
        self.blue["command"]=lambda colour="blue": self.colour(colour)
        self.blue.pack(padx=10, pady= 20, side="left")
        self.red = Button(self, text="RED", fg="red", bg="red",  height=5, width=10)
        self.red["command"]=lambda colour="red": self.colour(colour)
        self.red.pack(padx=10, pady= 20, side="left")
        self.green = Button(self, text="GREEN", fg="green", bg="green", height=5, width=10)
        self.green["command"]=lambda colour="green": self.colour(colour)
        self.green.pack(padx=10, pady= 20, side="left")

        #quit
        self.quit = Button(self, text="QUIT", fg="red", bg="black",command=root.destroy)
        self.quit.pack(padx=20, pady= 20)

    #set start time
    def start(self):
        global start
        start = time.time()

    #Record time button is clicked
    def colour(self, colour):
        global start
        t = time.time() - start
        global f
        f.write(str(t) + '\n')

    #Record user counts
    def enter(self):
        global start
        global f
        t = time.time() - start

        #Stop the experiment at 1.5min mark
        if (t > 90):
            f.close()
            ctypes.windll.user32.MessageBoxW(0, "DONE!", "Test over", 1)
        else:
            f.write(self.ent.get() + '\n')
        #clear the field for next entry
        self.ent.delete(0,END)

    #Open the user data file for writing
    def fileStart(self):
        global f
        f = open(self.file.get(),'w')
        
#setup the GUI
root = Tk()
app = Application(master=root)
root.geometry("400x400")
app.mainloop()
