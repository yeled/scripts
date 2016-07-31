"""
used sql creation code from https://weechat.org/scripts/source/triggerreply.py.html/
"""
try:
    import weechat as w
    import sqlite3
    IMPORT_ERR = 0
except ImportError:
    IMPORT_ERR = 1
import os

SCRIPT_NAME = "url_olde"
SCRIPT_AUTHOR = "Charlie Allom <charlie@evilforbeginners.com"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "Public domain"
SCRIPT_DESC = "tells you how long ago a URL was first posted."

def create_db():
    """ create the sqlite database """
    tmpcon = sqlite3.connect(DBFILE)
    cur = tmpcon.cursor()
    cur.execute("CREATE TABLE urls(id INTEGER PRIMARY KEY, uri VARCHAR, date INTEGER);")
    cur.execute("INSERT INTO urls(uri, date) VALUES ('spodder.com',1)")
    tmpcon.commit()
    cur.close()

def 

# weechat.register(name, author, version, license, description,
#                  shutdown_function, charset)
w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
           SCRIPT_LICENSE, SCRIPT_DESC, '', '')

    if IMPORT_ERR:
        w.prnt("", "You need sqlite3 to run this plugin.")
    DBFILE = "%s/olde.sqlite3" % w.info_get("weechat_dir", "")
    if not os.path.isfile(DBFILE):
        create_db()

w.prnt(w.current_buffer(), "feh")


def _print_url(data, buffer):
    return w.WEECHAT_RC_OK
