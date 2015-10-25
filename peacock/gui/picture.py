from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL.ImageTk import PhotoImage


class ImageView(object):
    """
    Views an image. The arrow keys can be used to traverse back and
    forth.
    """

    def __init__(self, parent_control, image_cursor):
        self._parent = parent_control
        self._image_cursor = image_cursor
        self.mainframe = ttk.Frame(self._parent, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe['borderwidth'] = 2
        self.mainframe['relief'] = 'sunken'

        self.label = ttk.Label(self.mainframe, text="HELLO")
        self.label.grid(column=1, row=1, sticky=(N, W, E, S))

        self._set_image()


        # This logic makes the Window resize. It currently doesn't look great.
        # I don't know if it's possible to resize an image on the fly in
        # standard Tkinter (drat)!

        # Tell the _parent its ok to resize.
        self._parent.columnconfigure(0, weight=1)
        self._parent.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

    def _set_image(self):
        image = self._image_cursor.current()
        image_control = Image.open(image.path)
        self.photo = PhotoImage(image)
        self.label['compound'] = 'bottom'
        self.label['image'] = self.photo

def demo():
    root = Tk()
    # Without this menu items get some gross tear off thing.
    root.option_add('*tearoff', FALSE)
    self.root.title("Image View Demo")
    p = ImageView(root)
    root.mainloop()
