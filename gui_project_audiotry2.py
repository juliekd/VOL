from tkinter import *
import time
import os
import ctypes
from sound import Sound
from pocketsphinx import LiveSpeech, get_model_path
from threading import Thread

global start
global f

#function for decreasing volume where input is speed
def decrease(inputspeed):
	#while current volume is not desired volume
	#decrease volume at rate according to speed
	speed = int(inputspeed)
	count = 0
	if speed == 1:
		while count <= 15:
			#1 second reduction for 15 bars
			Sound.volume_down()
			time.sleep(1 / 15)
			count += 1
	elif speed == 3:
		while count <= 15:
			#3 second reduction for 15 bars
			Sound.volume_down()
			time.sleep(3 / 15)
			count += 1
	elif speed == 5:
		while count <= 15:
			#5 second reduction for 15 bars
			Sound.volume_down()
			time.sleep(5 / 15)
			count += 1

def instant_decrease():
	Sound.volume_set(10)

#reset volume 
def normalize():
	Sound.volume_set(40)

def audioCheck(option):
    if (option == "0" or option == "1" or option == "3" or option == "5"):
        model_path = get_model_path()
        speech = LiveSpeech(
                verbose=False,
                sampling_rate=16000,
                buffer_size=2048,
                no_search=False,
                full_utt=False,
                hmm=os.path.join(model_path, 'en-us'),
                lm=os.path.join(model_path, 'en-us.lm.bin'),
                dic=os.path.join(model_path, 'cmudict-en-us.dict'))
        #speech = LiveSpeech(lm=False, keyphrase='hey', kws_threshold=1e+20)
        for phrase in speech:
            print(phrase)
            break
        if option == "0":
            instant_decrease()
        else:
            decrease(option)

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

        #Start button initiates the experiment
        self.speed = Entry(self)
        self.speed.pack()
        self.speed.insert(0,"0") #decrease speed default
        
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

    #Setup for experiment start
    def start(self):
        normalize()
        #set Start time
        global start
        global f
        start = time.time()

        self.line1.after(60000, self.increment)

        #audio
        option = self.speed.get()
        f.write('AUDIO REDUCTION LEVEL: ' + option + '\n')
        #audioThread = Thread(target=audioCheck, args=(option,))
        #audioThread.start()
        audioCheck(option)
        f.write('AUDIO CUE: ' + str(time.time() - start - float(option)) + '\n')
        normalize()
        
        #hacky solution for showing the 1min mark
    def increment(self):
        #global start
        #t = time.time() - start
        #self.line1["text"]=str(t)
        global f
        #f.write('CUE: ' + str(t) + '\n')
        f.close()
        ctypes.windll.user32.MessageBoxW(0, "DONE!", "Test over", 1)

    #Record time button is clicked
    def colour(self, colour):
        global start
        t = time.time() - start
        global f
        f.write('REACTION:' + str(t) + '\n')

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
