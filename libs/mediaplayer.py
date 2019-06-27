import subprocess
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
from tgnLIB import *

vol = 80
data = "TGN Media Player v.0.2"
player = MPyg321Player()
def play():
    player.play_song(data)
    player.gain(vol)
def pause():
    player.pause()
def resume():
    player.resume()
def stop():
    player.stop()
def quit():
    player.quit()
    root.quit()
def openfi():
    global data
    name = askopenfilename()
    data = name
def openfolder():
    print("nothing")
def openfile():
    print("nothing")
def openurl():
    global data
    data = simpledialog.askstring("URL:", "", parent=root)
def volup():
    global vol
    vol = vol + 10
    if vol >= 110:
        vol = 100
    player.gain(vol)
def voldown():
    global vol
    vol = vol - 10
    if vol <= 1:
        vol = 0
    player.gain(vol)
class WindowC(Frame):
    def __init__(self,master):
        afbground = '#000000'
        fground = '#eaa424'
        Frame.__init__(self, master)
        self.grid()
        self.canvas = Canvas(self, bg=afbground, highlightthickness=0, width=453, height=40)
        self.canvas.pack(expand=True)
        xpos = 450
        ypos = 20
        self.canvas.create_text(xpos, ypos, anchor='w', text=data,font=('Helvetica 20 bold'), fill=fground, tags='text')
        text_begin = self.canvas.bbox('text')[0]
        text_end = self.canvas.bbox('text')[2]
        self.text_length = text_end - text_begin
        self.scroll_text()
    def scroll_text(self):
        self.canvas.move('text', -3, 0)
        text_end = self.canvas.bbox('text')[2]
        if text_end < 0:
            self.canvas.itemconfig('text',text=data)
            text_begin = self.canvas.bbox('text')[0]
            text_end = self.canvas.bbox('text')[2]
            self.text_length = text_end - text_begin
            self.canvas.move('text', 450 + self.text_length, 0)
        self.canvas.after(30, self.scroll_text)

#gui
root = Tk()
root.overrideredirect(0) 
root.geometry("%dx%d+%d+%d" % (550, 200, 0, 0))
root.wm_title("TGN MediaPlayer")

menu = Menu(root)
root.config(background = "#000000", menu=menu)
filemenu = Menu(menu)
menubar = Menu(root, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
filemenu = Menu(menubar, tearoff=0, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Play File", command=openfi)
filemenu.add_command(label="Play URL", command=openurl)
filemenu.add_command(label="Play Folder", command=openfolder)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)

playmenu = Menu(menubar, tearoff=0, background='#668ff8', foreground='#000000',activebackground='#2a66fc', activeforeground='#000000')
menu.add_cascade(label="Play", menu=playmenu)
playmenu.add_command(label="Play", command=play)
playmenu.add_command(label="Pause", command=pause)
playmenu.add_command(label="Resume", command=resume)
playmenu.add_command(label="Stop", command=stop)
playmenu.add_command(label="Repeat", command=openfile)
playmenu.add_command(label="VOL up", command=volup)
playmenu.add_command(label="VOL down", command=voldown)

leftFrame = Frame(root, width=400, height = 400)
leftFrame.configure(background="#000000")
leftFrame.grid(row=0, column=0, padx=10, pady=3)

seperatorFrame4 = Frame(leftFrame)
seperatorFrame4.configure(background="#000000")
seperatorFrame4.grid(row=0, column=0, padx=5, pady=3)
seperatorLabel1 = Label(seperatorFrame4, text="")
seperatorLabel1.configure(background="#000000")
seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

app=WindowC(leftFrame)

seperatorFrame4 = Frame(leftFrame)
seperatorFrame4.configure(background="#000000")
seperatorFrame4.grid(row=2, column=0, padx=5, pady=3)
seperatorLabel1 = Label(seperatorFrame4, text="")
seperatorLabel1.configure(background="#000000")
seperatorLabel1.grid(row=0, column=0, padx=10, pady=3)

buttonFrame1 = Frame(leftFrame)
buttonFrame1.configure(background='#000000')
buttonFrame1.grid(row=3, column=0, padx=10, pady=3)

B1 = Button(buttonFrame1, text="Play", bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=10, command=play)
B1.grid(row=1, column=0, padx=10, pady=3) 
B2 = Button(buttonFrame1, text="Pause", bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=10, command=pause)
B2.grid(row=1, column=1, padx=10, pady=3)
B3 = Button(buttonFrame1, text="Resume", bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=10, command=resume)
B3.grid(row=1, column=2, padx=10, pady=3)
B4 = Button(buttonFrame1, text="Stop", bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=10, command=stop)
B4.grid(row=1, column=3, padx=10, pady=3)

buttonFrame2 = Frame(leftFrame)
buttonFrame2.configure(background='#000000')
buttonFrame2.grid(row=4, column=0, padx=10, pady=3)

B1 = Button(buttonFrame2, text="Vol up", bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=10, command=volup)
B1.grid(row=1, column=0, padx=10, pady=3) 
B2 = Button(buttonFrame2, text="Vol down", bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=10, command=voldown)
B2.grid(row=1, column=1, padx=10, pady=3)
B2 = Button(buttonFrame2, text="Open", bg='#668ff8', fg='#000000',activebackground='#2a66fc', activeforeground='#000000', width=10, command=openfi)
B2.grid(row=1, column=2, padx=10, pady=3)

root.mainloop()
