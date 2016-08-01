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


def create_db():
    """ create the sqlite database """
    tmpcon = sqlite3.connect(DBFILE)
    cur = tmpcon.cursor()
    cur.execute("CREATE TABLE urls(id INTEGER PRIMARY KEY, uri VARCHAR, date INTEGER, nick VARCHAR, channel VARCHAR);")
    cur.execute("INSERT INTO urls(uri, date, nick, channel) VALUES ('http://spodder.com',1470006765,'yeled','hello.#world')")
    cur.execute("INSERT INTO urls(uri, date, nick, channel) VALUES ('http://moo.com',110006765,'charlie','yelp.#badgers')")
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
    nick = prefix
    channel = w.buffer_get_string(buffer, 'name') # current channel. needs to come from sql.
    entry = []
    entry.append(message)
    entry.append(time.time())
    entry.append(nick)
    entry.append(channel)
    #, str(time.time()), nick, channel)]
    for olde in (message,):
        cursor.execute("SELECT date,uri,nick,channel from urls WHERE uri LIKE ?", (message,))
        result=cursor.fetchone()
        if result is None:
            w.command(buffer, "/say %s"  % (entry))
            cursor.execute("INSERT INTO urls(uri, date, nick, channel) VALUES (?,?,?,?)", entry)
            database.commit()
        else:
            date, uri, nick, channel = result
            pretty_time = time.ctime(float(str(date)))
            #w.command(buffer, "/say %s"  % str(result))
            w.prnt_date_tags(buffer, 0, 'no_log,notify_none', 'mentioned by %s in %s on %s' % (nick, channel, pretty_time))
    return w.WEECHAT_RC_OK


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
