import os, sys, re
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from collections import OrderedDict
from pprint import pprint

from widget import *

class Logger(Widget):

    def init(self):
        self.headers = {
            'miner:logs:gpu:0': 'Primary GPU Miner',
            'miner:logs:gpu:1': 'Secondary GPU Miner',
            'miner:logs:cpu': 'Primary CPU Miner'
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
            try:
                text = self.printText(text)
            except Exception as e:
                print e
        except:
            pass

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
                