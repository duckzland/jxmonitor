import sys, re
sys.path.append('../')
from modules.utility import printText
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
                text = printText(text)
            except Exception as e:
                print e
        except:
            pass

        return text
                
