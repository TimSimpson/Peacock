"""
Source for image files.
"""
import datetime
import logging
import os
import os.path


def add_directory(database, directory):
    log = logging.getLogger("add_directory %s" % directory)
    source_id = database.add_directory(directory)
    directory_len = len(directory) + 1
    for root, dirs, files in os.walk(directory):
        for f in files:
            full = os.path.join(root, f)
            mtime = os.path.getmtime(full)
            date_time = datetime.datetime.fromtimestamp(mtime)
            path = full[directory_len:]
            log.info("Adding image: %s (%s)" % (path, date_time))
            database.add_image(source_id, full, date_time)
