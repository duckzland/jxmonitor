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


def printText(raw_text):

    color_list = [
        'black',
        'dark red',
        'dark green',
        'brown',
        'dark blue',
        'dark magenta',
        'dark cyan',
        'light gray',
        'dark gray',
        'light red',
        'light green',
        'yellow',
        'light blue',
        'light magenta',
        'light cyan',
        'white'
    ]

    formated_text = []
    raw_text = str(raw_text)
    raw_text = raw_text.decode("utf-8")

    for at in raw_text.split("\x1b["):
        try:
            attr, text = at.split("m",1)
        except:
            attr = '0'
            text = at.split("m",1)
        list_attr = []
        for i in attr.split(';'):
            i = re.sub("[^0-9]", "", i)
            i = i.lstrip('0')
            if i == '':
                i = '0'
            list_attr.append(int(i))
        list_attr.sort()
        fg = -1
        bg = -1

        for elem in list_attr:
            if elem <= 29:
                pass
            elif elem <= 37:
                fg = elem - 30
            elif elem <= 47:
                bg = elem - 40
            elif elem <= 94:
                fg = fg + 8
            elif elem >= 100 and elem <= 104:
                bg = bg + 8

        fgcolor = color_list[fg]
        bgcolor = color_list[bg]

        if fg < 0:
            fgcolor = 'black'
        if bg < 0:
            bgcolor = 'white'

        if list_attr == [0]:
            fgcolor = 'black'
            bgcolor = 'white'

        if fgcolor == 'white':
            fgcolor = 'black'

        if fgcolor == 'light gray':
            fgcolor = 'dark gray'

        if bgcolor == 'black':
            bgcolor = 'white'

        if 'light' in fgcolor:
            fgcolor = fgcolor.replace('light', 'dark')

        formated_text.append((urwid.AttrSpec(fgcolor, bgcolor), text))

    return formated_text




def flattenGPU(data):
    GPU = {}
    if data and len(data) > 0:
        for keyword, value in data.iteritems():
            if 'gpu:fan' in keyword:
                gpu, fan, type, index = keyword.split(':')
                if index not in GPU:
                    GPU[index] = {}

                GPU[index]['fan'] = value
                GPU[index]['type'] = type
                GPU[index]['index'] = index

            if 'gpu:temperature' in keyword:
                gpu, temperature, type, index = keyword.split(':')
                if index not in GPU:
                    GPU[index] = {}

                GPU[index]['temperature'] = value
                GPU[index]['type'] = type
                GPU[index]['index'] = index


            if 'gpu:memory' in keyword:
                gpu, memory, type, index = keyword.split(':')

                if index not in GPU:
                    GPU[index] = {}

                GPU[index]['memory'] = value
                GPU[index]['type'] = type
                GPU[index]['index'] = index


            if 'gpu:core' in keyword:
                gpu, core, type, index = keyword.split(':')

                if index not in GPU:
                    GPU[index] = {}

                GPU[index]['core'] = value
                GPU[index]['type'] = type
                GPU[index]['index'] = index


            if 'gpu:power' in keyword:
                gpu, power, type, index = keyword.split(':')

                if index not in GPU:
                    GPU[index] = {}

                GPU[index]['power'] = value
                GPU[index]['type'] = type
                GPU[index]['index'] = index


            if 'gpu:watt' in keyword:
                gpu, power, type, index = keyword.split(':')

                if index not in GPU:
                    GPU[index] = {}

                GPU[index]['watt'] = value
                GPU[index]['type'] = type
                GPU[index]['index'] = index

    return GPU



def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            try:
                value = float(n) / prefix[s]
                return '%.1f%s' % (value, s)
            except: pass
    return "%sB" % n