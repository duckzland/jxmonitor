#!/usr/bin/env python

from modules.utility import printLog
from widgets.summary import Summary
from widgets.logger import Logger
from widgets.gpuinfo import GPUInfo
from collections import OrderedDict

import urwid, json

class LayoutView(urwid.WidgetWrap):

    palette = [
        ('body', 'black', 'light gray', 'standout'),
        ('header', 'dark blue', 'white', 'bold'),
        ('line', 'black', 'light gray', 'standout'),
        ('widget_value', 'dark green', 'white', 'standout'),
        ('widget_box', 'black', 'white', 'standout'),
        ('widget_line', 'light gray', 'white', 'standout'),
    ]



    def __init__(self, controller):
        self.maps = dict()
        self.controller = controller
        self.data = None
        self.sidebarWidgets = OrderedDict()
        self.contentWidgets = OrderedDict()
        self.sidebarBlock = []
        self.contentBlock = []



    def start(self):
        try:
            urwid.WidgetWrap.__init__(self, self.mainWindow())
            status = 'success'

        except:
            status = 'error'

        finally:
            printLog('Initializing main display', status)
            
            
            
    def update(self, data):
        temp = self.data
        try:
            if data:
                temp = json.loads(data.replace('\n', '\\n').replace('\r', '\\r'), strict=False)
            else:
                temp = data
        except:
            pass
        finally:
            if self.data != temp:
                self.data = temp
                if self.sidebarWidgets:
                    for key, widget in self.sidebarWidgets.iteritems():
                        widget.refresh(self.data)
                        widget.layout()

                if self.contentWidgets:
                    for key, widget in self.contentWidgets.iteritems():
                        widget.refresh(self.data)
                        widget.layout()

                self.layout()




    def reset(self):
        self.data = None
        self.sidebarWidgets = OrderedDict()
        self.contentWidgets = OrderedDict()
        self.sidebarBlock = []
        self.contentBlock = []
        self.layout()


    def layout(self):
        self.sidebarColumn()
        self.contentColumn()



    def sidebarColumn(self):
        if not 'summary' in self.sidebarWidgets:
            self.sidebarWidgets['summary'] = Summary(self, self.data, 'summary')

        if not 'gpuinfo' in self.sidebarWidgets:
            self.sidebarWidgets['gpuinfo'] = GPUInfo(self, self.data, 'gpuinfo')

        widgets = []
        if self.sidebarWidgets:
            for key, widget in self.sidebarWidgets.iteritems():
                if widget.frame:
                    for element in widget.frame:
                        widgets.append(element)

            if not self.sidebarBlock:
                self.sidebarBlock =  urwid.SimpleListWalker(widgets)
            else:
                self.sidebarBlock[:] = widgets



    def contentColumn(self):
        if not 'gpuinfo' in self.contentWidgets:
            self.contentWidgets['gpuinfo'] = Logger(self, self.data, 'miner:logs:gpu:0')

        for logKey in ['miner:logs:cpu', 'miner:logs:gpu:1']:
            if not logKey in self.contentWidgets:
                if self.data and logKey in self.data:
                    self.contentWidgets[logKey] = Logger(self, self.data, logKey)

        if self.contentWidgets:
            widgets = []
            for key, widget in self.contentWidgets.iteritems():
                if widget.frame:
                    for element in widget.frame:
                        widgets.append(element)

            if not self.contentBlock:
                self.contentBlock = urwid.SimpleListWalker(widgets)
            else:
                self.contentBlock[:] = widgets



    def mainWindow(self):
        separator = urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')
        self.layout()

        window = urwid.Columns([
            ('fixed', 44, urwid.ListBox(self.sidebarBlock)),
            ('fixed', 1, separator),
            ('weight', 2, urwid.ListBox(self.contentBlock)),
        ],
        dividechars=1,
        focus_column=1)

        window = urwid.Padding(window, ('fixed left', 1), ('fixed right', 1))
        window = urwid.AttrWrap(window, 'body')
        return window




class Layout:

    def __init__(self):
        self.viewReady = False
        self.loopReady = False



    def init(self):
        self.viewReady = True
        self.view = LayoutView(self)



    def main(self):
        self.view.start()
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        self.loopReady = True
        self.loop.run()



    def destroy(self):
        urwid.ExitMainLoop()
        self.loopReady = False