import os, urwid, re, string
from datetime import datetime

def printLog(text, status = 'info'):
    if 'error' in status:
        status = '-#' + status + '  #-'
    elif 'info' in status:
        status = '---#' + status + '   #-'
    else:
        status = '--#' + status + '#-'

    status = (
        status
            .upper()
            # Cyan color
            .replace('---#', '\033[36m')

            # Green color
            .replace('--#', '\033[32m')

            # Red color
            .replace('-#', '\033[91m')
            .replace('#-', '\033[0m')
    )

    text = (
        text
            .replace('--#', '\033[32m')
            .replace('-#', '\033[91m')
            .replace('#-', '\033[0m')
    )

    print("[ {0} ][ {1} ] {2}".format(datetime.now().strftime('%m-%d %H:%M'), status, text).strip())



def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')


def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)