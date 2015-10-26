import logging
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL.ImageTk import PhotoImage


class PilImage(object):

    def __init__(self, image_path):
        # Determine if the image is animated. TODO: After July 2015, use
        # n_frames to know if there are frames of animation.
        self._animated = image_path[-4:].lower() == ".gif"
        self._original_image = Image.open(image_path)
        self._image = self._original_image
        self._size = self._image.size

    @property
    def animated(self):
        # For some reasons playing a gif is chronically slow so disable it.
        return False # self._animated

    @property
    def image(self):
        return self._image

    def next_frame(self):
        try:
            logging.getLogger().debug("NEXT FRAME!")
            self._image.seek(self._image.tell() + 1)
        except EOFError:
            logging.getLogger().debug(" i/o errow?!! ")
            self._image.seek(0)

    def resize(self, width, height):
        scale_width = width / self._size[0]
        scale_height = height / self._size[1]
        scale = min(scale_width, scale_height)
        new_dimensions = (int(self._size[0] * scale),
                          int(self._size[1] * scale))
        self._image = self._original_image.resize(
            new_dimensions, Image.ANTIALIAS)


class ImageView(object):
    """
    Views an image. The arrow keys can be used to traverse back and
    forth.
    """

    def __init__(self, parent_control, image_cursor):
        self._parent = parent_control
        self._image_cursor = image_cursor
        self._log = logging.getLogger("ImageView")
        self.mainframe = ttk.Frame(self._parent, padding="0 0 0 0") #padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe['borderwidth'] = 2
        self.mainframe['relief'] = 'sunken'

        self._label_text = StringVar()
        self.label = ttk.Label(self.mainframe, textvariable=self._label_text)
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

    def _resize(self):
        """Resize the image."""
        self._image.resize(self._width, self._height)
        self.photo = PhotoImage(self._image.image)
        #self.photo.zoom(new_dimensions[0], new_dimensions[1])
        self.label['image'] = self.photo

    def _set_image(self):
        """Change to a new image or initialize it for the first time."""
        image = self._image_cursor.current()
        self._log.debug("Setting image %d" %self._image_cursor._index)
        self._label_text.set(image.path)
        self._image = PilImage(image.path)
        self._resize()
        if self._image.animated:
            self._log.debug("Going to animate.")
            self._parent.after(500, self._update_image)

    def _update_image(self):
        self._image.next_frame()
        self._resize()
        self._parent.after(500, self._update_image)


def demo():
    root = Tk()
    # Without this menu items get some gross tear off thing.
    root.option_add('*tearoff', FALSE)
    self.root.title("Image View Demo")
    p = ImageView(root)
    root.mainloop()
