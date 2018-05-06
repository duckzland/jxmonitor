import sys
sys.path.append('../')
from pprint import pprint
from modules.utility import flattenGPU
from widget import *
from collections import OrderedDict

class GPUInfo(Widget):

    def init(self):
        self.GPU = {}
        self.keywords = [
            { 'key' : 'temperature:highest', 'default': '0', 'format': '%sC'},
            { 'key' : 'temperature:average', 'default': '0', 'format': '%sC'},
            { 'key' : 'gpu:total_watt', 'default': '0', 'format': '%sW', 'process': [float, int]},
        ]
        self.registerGPU()



    def layout(self):
        self.registerGPU()
        self.layouts = OrderedDict()
        self.layouts['gpu:header'] = [urwid.Columns([
            ('fixed', 10, urwid.Text('GPU Unit')),
            ('fixed', 5, urwid.Text('Temp')),
            ('fixed', 5, urwid.Text('Fan')),
            ('fixed', 5, urwid.Text('Core')),
            ('fixed', 5, urwid.Text('Mem')),
            ('fixed', 5, urwid.Text('Pwr')),
            ('fixed', 5, urwid.Text('Watt')),
        ])]

        self.layouts['gpu:separator:top'] = [self.divider]

        if self.GPU and len(self.GPU) > 0:
            for index, unit in self.GPU.iteritems():
                keyword = 'GPU:%s' % (unit['index'])

                self.layouts['gpu:row:%s:content' % (unit['index'])] = [urwid.Columns([
                    ('fixed', 6, self.maps[keyword + ':type']),
                    ('fixed', 1, urwid.Text(':')),
                    ('fixed', 3, self.maps[keyword + ':index']),
                    ('fixed', 5, self.maps[keyword + ':temperature']),
                    ('fixed', 5, self.maps[keyword + ':fan']),
                    ('fixed', 5, self.maps[keyword + ':core']),
                    ('fixed', 5, self.maps[keyword + ':memory']),
                    ('fixed', 5, self.maps[keyword + ':power']),
                    ('fixed', 5, self.maps[keyword + ':watt'])
                ])]

                self.layouts['gpu:row:%s:separator' % (unit['index'])] = [self.divider]

        self.layouts['gpu:temperature'] = [urwid.Columns([
            ('fixed', 7, urwid.Text('High : ')), ('fixed', 4, self.maps['temperature:highest']), ('fixed', 3, urwid.Text(' | ')),
            ('fixed', 6, urwid.Text('Avg  : ')),  ('fixed', 4, self.maps['temperature:average']), ('fixed', 3, urwid.Text(' | ')),
            ('fixed', 8, urwid.Text('Watt : ')), ('fixed', 4, self.maps['gpu:total_watt']),
        ])]

        self.frameWidget()



    def registerGPU(self):
        GPU = flattenGPU(self.data)
        if GPU and len(GPU) > 0 and len(self.GPU) != len(GPU):
            self.GPU = GPU
            for index, unit in self.GPU.iteritems():
                keyword = 'GPU:%s' % (unit['index'])
                if not self.layouts.get(keyword + ':index'):
                    self.keywords.append({ 'key' : keyword + ':index', 'default': '0' })
                    self.keywords.append({ 'key' : keyword + ':type', 'default': '0' })
                    self.keywords.append({ 'key' : keyword + ':temperature', 'default': '0', 'format': '%sC' })
                    self.keywords.append({ 'key' : keyword + ':fan', 'default': '0', 'format': '%s%%' })
                    self.keywords.append({ 'key' : keyword + ':core', 'default': '0', 'format': '%s%%' })
                    self.keywords.append({ 'key' : keyword + ':memory', 'default': '0', 'format': '%s%%' })
                    self.keywords.append({ 'key' : keyword + ':power', 'default': '0', 'format': '%s%%' })
                    self.keywords.append({ 'key' : keyword + ':watt', 'default': '0', 'format': '%sW', 'process': [ float, int ] })

            self.mapping()



    def update(self):
        super(GPUInfo, self).update()

        # GPU Related Info
        GPU = flattenGPU(self.data)
        for index, unit in GPU.iteritems():
            keyword = 'GPU:%s' % (unit['index'])
            self.processGPU(unit)
                        
                        
                        
                        
    def processGPU(self, unit):
        keyword = 'GPU:%s' % (unit['index'])
        for element in self.keywords:
            if element.get('key') == keyword + ':index':
                self.process(keyword + ':index', unit['index'], element)
                
            if element.get('key') == keyword + ':type':
                self.process(keyword + ':type', unit['type'], element)
                
            if element.get('key') == keyword + ':temperature':
                self.process(keyword + ':temperature', unit['temperature'], element)
                
            if element.get('key') == keyword + ':fan':
                self.process(keyword + ':fan', unit['fan'], element)
                
            if element.get('key') == keyword + ':core':
                self.process(keyword + ':core', unit['core'], element)
                
            if element.get('key') == keyword + ':memory':
                self.process(keyword + ':memory', unit['memory'], element)
                
            if element.get('key') == keyword + ':power':
                self.process(keyword + ':power', unit['power'], element)
                
            if element.get('key') == keyword + ':watt':
                self.process(keyword + ':watt', unit['watt'], element)