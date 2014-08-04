from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL.ImageTk import PhotoImage


class Peacock(object):

    def __init__(self, root):
        self.root = root
        # Will return x11, win32, or aqua.
        self.platform = root.tk.call('tk', 'windowingsystem')
        self.root.title("Peacock")
        self.mainframe  = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe['borderwidth'] = 2
        self.mainframe['relief'] = 'sunken'

        self.label = ttk.Label(self.mainframe, text="HELLO")
        self.label.grid(column=1, row=1, sticky=(N, W, E, S))
        self.image = Image.open("16-MinohKim_SuperPowerMasterOptimusPrime.jpg")
        self.photo = PhotoImage(self.image)
        self.label['compound'] = 'bottom'
        self.label['image'] = self.photo

        # This logic makes the Window resize. It currently doesn't look great.
        # I don't know if it's possible to resize an image on the fly in
        # standard Tkinter (drat)!

        # Tell the root its ok to resize.
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.rowconfigure(1, weight=1)


def run():
    root = Tk()
    # Without this menu items get some gross tear off thing.
    root.option_add('*tearoff', FALSE)
    p = Peacock(root)
    root.mainloop()
