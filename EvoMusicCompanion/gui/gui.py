import tkinter as tk
import tkinter.font as tkFont

from tkinter import *

HEIGHT = 1024
WIDTH = 1440
PRIMARY_COLOR = '#ff2345'
SECONDARY_COLOR = '#2A2A2A'
WHITE = '#f3f3f3'
PIANO_ROLL_BG_WHITE = '#f1f1f1'
root = Tk()
font = tkFont.Font(root=root, family="Lato Regular", size=12)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

mainframe = tk.Frame(root, bg = WHITE )

piece_index = 0
def render():
    mainframe.place(relwidth=1.0, relheight=1.0)

    leftframe = tk.Frame(mainframe, bg = SECONDARY_COLOR)
    leftframe.place(relwidth=0.20, relheight=1.0)

    label = Label(leftframe, text="EvoMusic", bg = SECONDARY_COLOR, fg=WHITE, font=font)
    label.place(relwidth=0.8, relx=0.1, rely=0.005)

    button = Button(leftframe, text="Test", bg=PRIMARY_COLOR, fg=WHITE)
    button.place(relx=0.1, rely=0.1)
    
    topframe = tk.Frame(mainframe, bg = SECONDARY_COLOR)
    topframe.place(relwidth=0.8, relheight=0.2, relx=0.2)
    
    curr_song_label = Label(topframe, text="Song 1/5", bg = SECONDARY_COLOR, fg=WHITE, font=font)
    curr_song_label.config(anchor=CENTER)
    curr_song_label.pack()
    
    #musicWindow(mainframe, None)
    root.mainloop()


def musicWindow(mainframe, pieces):
    musicframe = tk.Frame(mainframe, bg = WHITE)
    musicframe.place(relx=0.2, relwidth=0.8, relheight=0.8)

    label = Label(musicframe, text="Current piece", bg=WHITE, fg=SECONDARY_COLOR, font=font)
    label.config(anchor=CENTER)
    label.pack(ipady=10)
    
    piano_frame = tk.Frame(musicframe, bg=PIANO_ROLL_BG_WHITE)
    piano_frame.place(relwidth=1.0, relheight=0.5)
    p_canvas = Canvas(piano_frame, width=800, height=800)
    p_canvas.pack()
    p_canvas.create_rectangle(0, 0, 100, 100, fill=PRIMARY_COLOR)
    piano_frame.place()



def piano_octave(frame):
    piano_frame = tk.Frame(frame)
    p_canvas = tk.Canvas(piano_frame)
    p_canvas.pack()
    p_canvas.create_rectangle(0, 0, 50, 50, fill=PRIMARY_COLOR)
    piano_frame.place()

  
