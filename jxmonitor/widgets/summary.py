import os, sys, urwid
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append('../')
from pprint import pprint

from widget import *

class Summary(Widget):

    def init(self):
        self.keywords = [
            { 'key'    : 'general:boxname', 'default': 'JXMiner', 'color': 'header' },
            { 'key'    : 'general:active:gpu:coin' },
            { 'key'    : 'general:active:gpu:pool' },
            { 'key'    : 'miner:hashrate:gpu:0', 'default': '0' },
            { 'key'    : 'miner:shares:gpu:0', 'default': '0' },
            { 'key'    : 'general:active:gpu:second_coin' },
            { 'key'    : 'general:active:gpu:second_pool' },
            { 'key'    : 'miner:hashrate:gpu:1', 'default': '0' },
            { 'key'    : 'miner:shares:gpu:1', 'default': '0' },
            { 'key'    : 'general:active:cpu:coin' },
            { 'key'    : 'general:active:cpu:pool' },
            { 'key'    : 'miner:hashrate:cpu', 'default': '0' },
            { 'key'    : 'miner:shares:cpu', 'default': '0' },
            { 'key'    : 'memory:virtual:free', 'default': '0', 'process': [ self.Bytes2human ] },
            { 'key'    : 'memory:virtual:total', 'default': '0', 'process': [ self.Bytes2human ] },
            { 'key'    : 'memory:swap:free', 'default': '0', 'process': [ self.Bytes2human ] },
            { 'key'    : 'memory:swap:total', 'default': '0', 'process': [ self.Bytes2human ] },
            { 'key'    : 'disk:usage:used', 'default': '0', 'process': [ self.Bytes2human ] },
            { 'key'    : 'disk:usage:total', 'default': '0', 'process': [ self.Bytes2human ] },
            { 'key'    : 'network:status:bytes_recv', 'default': '0', 'process': [ self.Bytes2human ] },
            { 'key'    : 'network:status:bytes_sent', 'default': '0', 'process': [ self.Bytes2human ] },
        ]

        self.isDynamicRegistered = False
        self.registerDynamicElement()
        
        
    def layout(self):

        self.registerDynamicElement()

        self.layouts = OrderedDict()
        self.layouts['box:title'] = [
            self.maps['general:boxname'],
            self.divider,
        ]

        self.layouts['gpu:1:info'] = self.doubleColumn('GPU 1 : ', 'general:active:gpu:coin', 'general:active:gpu:pool')
        self.layouts['gpu:1:stat'] = self.doubleColumn('Stats : ', 'miner:hashrate:gpu:0', 'miner:shares:gpu:0')

        if self.data:
            if 'general:active:gpu:second_coin' in self.data and 'general:active:gpu:second_pool' in self.data:
                self.layouts['gpu:2:info'] = self.doubleColumn('GPU 2 : ', 'general:active:gpu:second_coin' , 'general:active:gpu:second_pool')

            if 'miner:hashrate:gpu:1' in self.data and 'miner:shares:gpu:1' in self.data:
                self.layouts['gpu:2:stat'] = self.doubleColumn('Stats : ', 'miner:hashrate:gpu:1', 'miner:shares:gpu:1')

            if 'general:active:cpu:coin' in self.data and 'general:active:cpu:pool' in self.data:
                 self.layouts['cpu:info'] = self.doubleColumn('CPU   : ', 'general:active:cpu:coin', 'general:active:cpu:pool')

            if 'miner:hashrate:cpu' in self.data and 'miner:shares:cpu' in self.data:
                self.layouts['cpu:stat'] = self.doubleColumn('Stats : ', 'miner:hashrate:cpu', 'miner:shares:cpu')

        self.layouts['memory:virtual'] = self.doubleColumn('Memory: ', 'memory:virtual:free' , 'memory:virtual:total', True)
        self.layouts['memory:swap'] = self.doubleColumn('Swap  : ', 'memory:swap:free' , 'memory:swap:total')
        self.layouts['disk'] = self.doubleColumn('Disk  : ', 'disk:usage:used' , 'disk:usage:total', True)
        self.layouts['network'] = self.doubleColumn('Net   : ', 'network:status:bytes_recv' ,'network:status:bytes_sent', True)

        if self.isDynamicRegistered:
            self.layouts['cpu:load'] = self.multiColumn('CPU    ', 'Usage :', 'cpu:usage:', 'CPU%s', 2, True)
            self.layouts['fan:speed'] = self.multiColumn('Fan    ', 'Speed :', 'fan:speed', '%s', 2, True)

        self.frameWidget()
                

    def registerDynamicElement(self):
        if self.data and not self.isDynamicRegistered:
            for keyword, value in self.data.iteritems():
                if 'cpu:usage' in keyword:
                    self.keywords.append({ 'key' : keyword, 'default': '0.00', 'format': '%s%%', 'process': [ float, int ] })

                if 'fan:speed' in keyword:
                    self.keywords.append({ 'key' : keyword, 'default': '0.00', 'format': '%s%%', 'process': [ float, int ] })
            self.isDynamicRegistered = True
            self.mapping()
            
            
            
    def Bytes2human(self, n):
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