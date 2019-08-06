import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pprint import pprint
from modules import *
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

        if len(self.GPU) > 0:
            self.layouts = OrderedDict()
            self.layouts['gpu:header'] = [urwid.Columns([
                ('fixed', 10, urwid.Text(('widget_label', 'GPU Unit'))),
                ('fixed', 5, urwid.Text(('widget_label', 'Temp'))),
                ('fixed', 5, urwid.Text(('widget_label', 'Fan'))),
                ('fixed', 5, urwid.Text(('widget_label', 'Core'))),
                ('fixed', 5, urwid.Text(('widget_label', 'Mem'))),
                ('fixed', 5, urwid.Text(('widget_label', 'Pwr'))),
                ('fixed', 5, urwid.Text(('widget_label', 'Watt'))),
            ])]

            self.layouts['gpu:separator:top'] = [self.divider]

            if self.GPU and len(self.GPU) > 0:
                for index, unit in self.GPU.iteritems():
                    keyword = 'GPU:%s' % (unit['index'])

                    self.layouts['gpu:row:%s:content' % (unit['index'])] = [urwid.Columns([
                        ('fixed', 6, self.maps[keyword + ':type']),
                        ('fixed', 1, urwid.Text(('widget_label', ':'))),
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
                ('fixed', 7, urwid.Text(('widget_label', 'High : '))), ('fixed', 3, self.maps['temperature:highest']), ('fixed', 3, urwid.Text(('widget_line', ' | '))),
                ('fixed', 7, urwid.Text(('widget_label', 'Avg  : '))),  ('fixed', 3, self.maps['temperature:average']), ('fixed', 3, urwid.Text(('widget_line', ' | '))),
                ('fixed', 7, urwid.Text(('widget_label', 'Watt : '))), ('fixed', 7, self.maps['gpu:total_watt']),
            ])]

            self.frameWidget()



    def registerGPU(self):
        GPU = self.flattenGPU(self.data)
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
        GPU = self.flattenGPU(self.data)
        for index, unit in GPU.iteritems():
            self.processGPU(unit)
                        
                        
                        
                        
    def processGPU(self, unit):
        keyword = 'GPU:%s' % (unit['index'])
        for element in self.keywords:
            for x in ['index', 'type', 'temperature', 'fan', 'core', 'memory', 'power', 'watt']:
                if element.get('key') == '%s:%s' % (keyword, x):
                    self.process('%s:%s' % (keyword, x), unit[x], element)
                



    def flattenGPU(self, data):
        GPU = {}
        if data and len(data) > 0:
            for keyword, value in data.iteritems():

                if not value:
                    value = '0'

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

        return OrderedDict(sorted(GPU.items(), key=lambda k: int(k[0])))