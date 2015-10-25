import logging
import sys
from peacock import db
from peacock import init
from peacock import source

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Expected at least three arguments.")
        sys.stderr.write("\t%s [config_path] [root_pic_dir1] [root_pic_dir2]"
                         % sys.argv[0])
        sys.exit(1)

    cfg = init.initialize(sys.argv[1])
    log = logging.getLogger(__file__)
    log.info("Checking db configs...")
    db_admin = db.Database.from_config(cfg)
    log.info("Creating tables...")
    db_admin.create_tables()
    conn = db_admin.open_connection()


    for directory in sys.argv[2:]:
        log.info("Adding directory %s" % directory)
        source.add_directory(conn, directory)



    log.info("HI!")

