import weechat as w

SCRIPT_NAME = "url_olde"
SCRIPT_AUTHOR = "Charlie Allom <charlie@evilforbeginners.com"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "Public domain"
SCRIPT_DESC = ""

# weechat.register(name, author, version, license, description,
#                  shutdown_function, charset)
w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
           SCRIPT_LICENSE, SCRIPT_DESC, '', '')

w.prnt(w.current_buffer(), "feh")


def _print_url(data, buffer):
    return w.WEECHAT_RC_OK
