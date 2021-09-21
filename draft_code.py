import os
import tkinter as tk
from tkinter import *


# used to run app through SSH
if os.environ.get('DISPLAY', '') == '':
    # print('no display found. Using :0.0') #commented out when don't want to log in terminal
    os.environ.__setitem__('DISPLAY', ':0.0')

root = tk.Tk()

labelframe = LabelFrame(root, text="This is a LabelFrame")
labelframe.pack(fill="both", expand="yes")
 
left = Label(labelframe, text="Inside the LabelFrame")
left.pack()
 
root.mainloop()