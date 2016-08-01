"""
used sql creation code from https://weechat.org/scripts/source/triggerreply.py.html/
"""

SCRIPT_NAME = "url_olde"
SCRIPT_AUTHOR = "Charlie Allom <charlie@evilforbeginners.com"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "Public domain"
SCRIPT_DESC = "tells you how long ago a URL was first posted."

try:
    import weechat as w
    import sqlite3, time
    IMPORT_ERR = 0
except ImportError:
    IMPORT_ERR = 1
import os

# regex are from urlbar.py, written by xt
#url_octet = r'(?:2(?:[0-4]\d|5[0-5])|1\d\d|\d{1,2})'
#url_ipaddr = r'%s(?:\.%s){3}' % (url_octet, url_octet)
#url_label = r'[0-9a-z][-0-9a-z]*[0-9a-z]?'
#url_domain = r'%s(?:\.%s)*\.[a-z][-0-9a-z]*[a-z]?' % (url_label, url_label)

def create_db():
    """ create the sqlite database """
    tmpcon = sqlite3.connect(DBFILE)
    cur = tmpcon.cursor()
    cur.execute("CREATE TABLE urls(id INTEGER PRIMARY KEY, uri VARCHAR, date INTEGER);")
    cur.execute("INSERT INTO urls(uri, date) VALUES ('http://spodder.com',1470006765)")
    cur.execute("INSERT INTO urls(uri, date) VALUES ('http://moo.com',110006765)")
    tmpcon.commit()
    cur.close()


def search_urls_cb(data, buffer, date, tags, displayed, highlight, prefix, message):
    """ function for searching for the url
    message = uri
    buffer needs buffer_get_string for the short name
    prefix is nick
    """
    database = sqlite3.connect(DBFILE)
    database.text_factory = str
    cursor = database.cursor()
    channel = w.buffer_get_string(buffer, 'name')
    for row in cursor.execute("SELECT date,uri from urls WHERE uri LIKE ?", (message,)) :
        date, uri = row
        pretty_time = time.ctime(float(str(date)))
        #w.command(buffer, "/say %s" % pretty_time)
        w.prnt_date_tags(buffer, 0, 'no_log,notify_none', '%s' % (pretty_time))
    return w.WEECHAT_RC_OK



def modify_irc_cb(uri, date):
    """ add the url age to the IRC message """
    return date

# weechat.register(name, author, version, license, description,
#                  shutdown_function, charset)
if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
           SCRIPT_LICENSE, SCRIPT_DESC, '', ''):
    if IMPORT_ERR:
        w.prnt("", "You need sqlite3 to run this plugin.")
    DBFILE = "%s/olde.sqlite3" % w.info_get("weechat_dir", "")
    if not os.path.isfile(DBFILE):
        create_db()

    # catch urls in buffer and print
    w.hook_print('', '', '://', 1, 'search_urls_cb', '')

    # test
    w.prnt(w.current_buffer(), "feh")

#def _print_url(data, buffer):
#    return w.WEECHAT_RC_OK
