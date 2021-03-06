import urwid, json

from widgets import *
from modules import *
from collections import OrderedDict

class LayoutView(urwid.WidgetWrap):

    palette = [
        ('body', 'light gray', 'black', 'standout'),
        ('header', 'dark red', '', 'bold', '#f60', ''),
        ('line', 'dark gray', '', 'standout'),
        ('widget_value', 'white', '', 'standout'),
        ('widget_label', 'light gray', '', 'standout'),
        ('widget_box', 'dark red', 'black', 'standout', '#f60', ''),
        ('widget_line', 'dark gray', 'black', 'standout'),
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

        except Exception as e:
            print e
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
                self.sidebarBlock =  urwid.SimpleFocusListWalker(widgets)
            else:
                self.sidebarBlock[:] = widgets




    def contentColumn(self):

        # This is weird if we dont add this here the rest of the box wont show
        # to circumvent this we add this first then remove it later if no gpuinfo available
        if not 'gpuinfo' in self.contentWidgets:
            self.contentWidgets['gpuinfo'] = Logger(self, self.data, 'miner:logs:gpu:0')

        for logKey in [ 'miner:logs:gpu:1', 'miner:logs:cpu', 'serverlog']:
            if not logKey in self.contentWidgets:
                if self.data and logKey in self.data:
                    self.contentWidgets[logKey] = Logger(self, self.data, logKey)

        # force remove the gpu box if no gpuinfo available
        if self.data and not 'miner:logs:gpu:0' in self.data:
            del self.contentWidgets['gpuinfo']


        if self.contentWidgets:
            widgets = []
            for key, widget in self.contentWidgets.iteritems():
                if widget.frame:
                    for element in widget.frame:
                        widgets.append(element)

            if not self.contentBlock:
                self.contentBlock = urwid.SimpleFocusListWalker(widgets)
            else:
                self.contentBlock[:] = widgets



    def mainWindow(self):
        separator = urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')
        self.layout()

        if self.controller.singleColumn:
            window = urwid.Pile(
                [urwid.ListBox(self.sidebarBlock), urwid.ListBox(self.contentBlock)]
            )
        else:
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

    def __init__(self, singleColumn = False):
        self.viewReady = False
        self.loopReady = False
        self.singleColumn = singleColumn



    def init(self):
        self.viewReady = True
        self.view = LayoutView(self)



    def main(self):
        self.view.start()
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        self.loop.screen.set_terminal_properties(colors=256)
        self.loopReady = True
        self.loop.run()



    def destroy(self):
        urwid.ExitMainLoop()
        self.loopReady = False