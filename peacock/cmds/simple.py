import logging
import sys
import datetime
from tkinter import *
from tkinter import ttk
from peacock import db
from peacock import init
from peacock import source
from peacock.gui.picture import ImageView


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Expected at least two arguments.")
        sys.stderr.write("\t%s [config_path]"
                         % sys.argv[0])

        sys.exit(1)

    cfg = init.initialize(sys.argv[1])
    log = logging.getLogger(__file__)
    log.info("Checking db configs...")
    db_admin = db.Database.from_config(cfg)
    log.info("Opening up database...")
    conn = db_admin.open_connection()
    now = datetime.datetime.now()
    image_finder = conn.find(now, tags=None)
    image_cursor = image.ImageCursor(image_finder)

    root = Tk()
    # Without this menu items get some gross tear off thing.
    root.option_add('*tearoff', FALSE)
    root.title("Image View Demo")
    p = ImageView(root, image_cursor)
    root.mainloop()
