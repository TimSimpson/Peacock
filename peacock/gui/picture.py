import logging
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
        self._log = logging.getLogger("ImageView")
        self.mainframe = ttk.Frame(self._parent, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe['borderwidth'] = 2
        self.mainframe['relief'] = 'sunken'

        self.label = ttk.Label(self.mainframe, text="HELLO")
        self.label.grid(column=1, row=1, sticky=(N, W, E, S))

        self.photo = None
        self.label['compound'] = 'bottom'

        # Tell the _parent its ok to resize.
        self._parent.columnconfigure(0, weight=1)
        self._parent.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.rowconfigure(1, weight=1)

        self._width = float(self.mainframe.winfo_width())
        self._height = float(self.mainframe.winfo_height())

        # Bind events to the mainframe letting arrow keys move back and forth
        def left(event):
            self._image_cursor.left()
            self._set_image()

        def right(event):
            self._image_cursor.right()
            self._set_image()

        def resize(event):
            #self._width = float(self.label.winfo_width())#float(event.width)
            #self._height = float(self.label.winfo_width())#float(event.height)
            self._width = float(event.width)
            self._height = float(event.height)
            self._log.debug("RESIZE! %s x %s" % (self._width, self._height))
            self._set_image()

        self.mainframe.bind('<Left>', left)
        self.mainframe.bind('<Right>', right)
        self.mainframe.bind('<Configure>', resize)
        self.mainframe.focus_set()
        self._set_image()


    def _set_image(self):
        image = self._image_cursor.current()
        self._log.debug("Setting image %d" %self._image_cursor._index)
        pil_image = Image.open(image.path)

        width, height = pil_image.size
        scale_width = self._width / width
        scale_height = self._height / height
        scale = min(scale_width, scale_height)

        #pil_image.thumbnail((self._width, self._height), Image.ANTIALIAS)
        new_dimensions = (int(width * scale), int(height * scale))
        self._log.debug("old size = %s x %s" % (width, height))
        self._log.debug("new size = %s x %s" % new_dimensions)
        pil_image = pil_image.resize(new_dimensions, Image.ANTIALIAS)
        self.photo = PhotoImage(pil_image)
        #self.photo.zoom(new_dimensions[0], new_dimensions[1])

        self.label['image'] = self.photo

def demo():
    root = Tk()
    # Without this menu items get some gross tear off thing.
    root.option_add('*tearoff', FALSE)
    self.root.title("Image View Demo")
    p = ImageView(root)
    root.mainloop()
