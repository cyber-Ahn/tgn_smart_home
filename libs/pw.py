import time
from tkinter import *
from tgnLIB import ifI2C, read_eeprom

ROM_ADDRESS = 0x53

pw_key = "0000"
inLine = ""
if ifI2C(ROM_ADDRESS) == "found device":
    start_add_Z = 0x40
    index = 0
    pw_key = ""
    while index < 15:
        cach = read_eeprom(1,ROM_ADDRESS,0x01,start_add_Z)
        if cach != "X":
            pw_key = pw_key + cach
        index = index + 1
        start_add_Z = start_add_Z + 1
def callback7():
    global inLine
    inLine = inLine + "7"
def callback8():
    global inLine
    inLine = inLine + "8"
def callback9():
    global inLine
    inLine = inLine + "9"
def callback4():
    global inLine
    inLine = inLine + "4"
def callback5():
    global inLine
    inLine = inLine + "5"
def callback6():
    global inLine
    inLine = inLine + "6"
def callback1():
    global inLine
    inLine = inLine + "1"
def callback2():
    global inLine
    inLine = inLine + "2"
def callback3():
    global inLine
    inLine = inLine + "3"
def callbackstar():
    global inLine
    inLine = ""
def callback0():
    global inLine
    inLine = inLine + "0"
def callbackroute():
    global inLine
    if(inLine == pw_key):
        inLine = "PW OK"
        time.sleep(1)
        root.quit()
    else:
        inLine = ""
the_time=''
TIME = newtime = time.time()
class Window(Frame):
	def __init__(self,master):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()
	def create_widgets(self):
		self.display_time=Label(self, text=the_time)
		self.display_time.grid(row=0, column=1)
		def change_value_the_time():
			global the_time
			the_time="Input:"+inLine
			self.display_time.config(text=the_time, font=('times', 15, 'bold'), bg="black", fg="red")
			self.display_time.after(1000, change_value_the_time)
		change_value_the_time()
root = Tk()
WMWIDTH, WMHEIGHT, WMLEFT, WMTOP = root.winfo_screenwidth(), root.winfo_screenheight(), 0, 0
root.overrideredirect(1)
root.geometry("%dx%d+%d+%d" % (WMWIDTH, WMHEIGHT, WMLEFT, WMTOP))
menu = Menu(root)
root.config(background = "black", menu=menu)
root.wm_title("TGN Smart Home Login")
rightFrame = Frame(root, width=400, height = 400)
rightFrame.configure(background="black")
rightFrame.grid(row=0, column=1, padx=10, pady=3)
buttonFrame = Frame(rightFrame)
buttonFrame.configure(background="black")
buttonFrame.grid(row=1, column=0, padx=10, pady=3)
buttonLabel1 = Label(buttonFrame, text="Password:")
buttonLabel1.configure(background="black", font=('times', 15, 'bold'), foreground="red")
buttonLabel1.grid(row=0, column=1, padx=10, pady=3)
B1 = Button(buttonFrame, text="7", bg="gray", fg="black", width=5, command=callback7)
B1.grid(row=1, column=0, padx=10, pady=3)
B2 = Button(buttonFrame, text="8", bg="gray", fg="black", width=5, command=callback8)
B2.grid(row=1, column=1, padx=10, pady=3)
B3 = Button(buttonFrame, text="9", bg="gray", fg="black", width=5, command=callback9)
B3.grid(row=1, column=2, padx=10, pady=3)
B4 = Button(buttonFrame, text="4", bg="gray", fg="black", width=5, command=callback4)
B4.grid(row=2, column=0, padx=10, pady=3)
B5 = Button(buttonFrame, text="5", bg="gray", fg="black", width=5, command=callback5)
B5.grid(row=2, column=1, padx=10, pady=3)
B6 = Button(buttonFrame, text="6", bg="gray", fg="black", width=5, command=callback6)
B6.grid(row=2, column=2, padx=10, pady=3)
B7 = Button(buttonFrame, text="1", bg="gray", fg="black", width=5, command=callback1)
B7.grid(row=3, column=0, padx=10, pady=3)
B8 = Button(buttonFrame, text="2", bg="gray", fg="black", width=5, command=callback2)
B8.grid(row=3, column=1, padx=10, pady=3)
B9 = Button(buttonFrame, text="3", bg="gray", fg="black", width=5, command=callback3)
B9.grid(row=3, column=2, padx=10, pady=3)
B10 = Button(buttonFrame, text="C", bg="gray", fg="black", width=5, command=callbackstar)
B10.grid(row=4, column=0, padx=10, pady=3)
B11 = Button(buttonFrame, text="0", bg="gray", fg="black", width=5, command=callback0)
B11.grid(row=4, column=1, padx=10, pady=3)
B12 = Button(buttonFrame, text="E", bg="gray", fg="black", width=5, command=callbackroute)
B12.grid(row=4, column=2, padx=10, pady=3)
app=Window(rightFrame)
root.mainloop()