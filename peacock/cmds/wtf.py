import logging
import sys
import datetime
from tkinter import *
from tkinter import ttk
from peacock import db
from peacock import image
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
    images = conn.grab_all_images()
    for image in images:
        print("ID=%s Path=%s\n\tDateTime=%s"
              % (image.id, image.path, image.datetime))
