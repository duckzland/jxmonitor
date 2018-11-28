import os, sys, re
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from colorclass.parse import parse_input
from collections import OrderedDict
from pprint import pprint
from kitchen.text.converters import getwriter

from widget import *

class Logger(Widget):

    def init(self):
        self.headers = {
            'miner:logs:gpu:0': 'Primary GPU Miner',
            'miner:logs:gpu:1': 'Secondary GPU Miner',
            'miner:logs:cpu': 'Primary CPU Miner',
            'serverlog': 'Server Logs'
        }

        self.keywords = [
            { 'key'    : self.type, 'default': 'Not initialized', 'color': False, 'format': False, 'process': [ self.processText ] },
        ]
        
        
    def layout(self):
        self.layouts = OrderedDict()
        self.layouts['logger:box:' + self.type] = [
            urwid.Text(self.headers[self.type]),
            self.divider,
            self.maps[self.type]
        ]

        self.frameWidget()



    def processText(self, text):
        if isinstance(text, str):
            return text

        try:
            text = ''.join(text)
            text = re.sub(r'\[\d+\-\d+\-\d+ \d+:\d+:\d+\]', '-', text)

            # Ethminer special text
            text = re.sub(r'(?:  m | cu )', '+', text)
            text = re.sub(r'\d+:\d+:\d+\|\w+\|  ', '', text)

            text = parse_input(text, False, True)[0]
            text = self.printText(text)

        except Exception as e:
            print e

        return text
        
        
    def printText(self, raw_text):
    
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
        UTF8Writer = getwriter('utf8')
        raw_text = UTF8Writer(raw_text)
    
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

            if color_list[fg]:
                fgcolor = color_list[fg]

            if color_list[bg]:
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

            if fgcolor not in color_list:
                fgcolor = 'black'

            if bgcolor not in color_list:
                fgcolor = 'white'

            if not text:
                fgcolor = 'black'
                bgcolor = 'white'
                text = at

            formated_text.append((urwid.AttrSpec(fgcolor, bgcolor), text))
    
        return formated_text
                
