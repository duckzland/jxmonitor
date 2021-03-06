import os, sys, traceback, urwid

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pprint import pprint
from collections import OrderedDict

__metaclass__ = type
class Widget:

    global urwid

    def __init__(self, Window, data, type):
        self.type = type
        self.data = data
        self.keywords = []
        self.maps = dict()
        self.divider = urwid.AttrWrap( urwid.Divider(u'\u2500'), 'widget_line' )
        self.layouts = OrderedDict()
        self.frame = None
        self.window = Window
        self.init()
        self.mapping()
        self.layout()


    def init(self):
        pass


    def layout(self):
        pass


    def mapping(self):
        for element in self.keywords:
            keyword  = element.get('key', None)
            multiple = element.get('multiple', False)
            if keyword and not multiple:
                default  = element.get('default', 'N/A')
                self.process(keyword, default, element)


    def refresh(self, data):
        self.data = data
        self.update()



    def process(self, keyword, value, element):
        keyword     = element.get('key', None)
        color       = element.get('color', 'widget_value')
        format      = element.get('format', '%s')
        processors  = element.get('process', [])

        if not keyword in self.maps:
            self.maps[keyword] = urwid.Text('')
            self.maps[keyword].pack((8,))

        if len(processors) > 0:
            for process in processors:
                value = process(value)
                if not value:
                    break

        if value:
            text = value
            if format:
                text = str(format % (value))

            if color:
                text = (color, text)

            self.maps[keyword].set_text(text)


    def update(self):
        for element in self.keywords:
            value = element.get('default', 'N/A')
            if self.data:
                value = self.data.get(element.get('key'), value)

            if value:
               self.process(element.get('key'), value, element)



    def doubleColumn(self, title, firstKey, secondKey, divider = None):
        w = []
        if divider:
            w.append(self.divider)

        w.append(urwid.Columns([
            ('fixed', 8, urwid.Text(('widget_label', title))),
            ('fixed', 10, self.maps[firstKey]),
            ('fixed', 3, urwid.Text(('widget_line', ' | '))),
            ('weight', 2, self.maps[secondKey]),
        ]))
        return w



    def multiColumn(self, title, subTitle, testKey, headerText, headerKey = 2, divider = None):
        rows = []
        headers = []
        w = []
        for keyword, urwidElement in self.maps.iteritems():
            if testKey in keyword:
                index = keyword.split(':')[int(headerKey)]
                headingText = headerText % (index)
                headers.append(('fixed', 6, urwid.Text(('widget_label', str(headingText).upper()) ) ))
                rows.append(('fixed', 6, urwidElement))

        if len(headers):
            headers = [('fixed', 8, urwid.Text(('widget_label', title)) )] + headers
            rows = [('fixed', 8, urwid.Text(('widget_label', subTitle) ))] + rows
            if divider:
                w.append(self.divider)

            w.append(urwid.Columns(headers))
            w.append(self.divider)
            w.append(urwid.Columns(rows))

        return w




    def frameWidget(self):
        self.frame = []
        c = []
        c.append(urwid.Divider())
        for key, row in self.layouts.iteritems():
            if row:
                for r in row:
                    c.append(r)

        c.append(urwid.Divider())

        p = urwid.Pile(c)
        p = urwid.Padding(p, ('fixed left', 1), ('fixed right', 1))
        p = urwid.LineBox(p)
        p = urwid.AttrWrap(p, 'widget_box')

        self.frame.append(urwid.Divider())
        self.frame.append(p)
        self.frame.append(urwid.Divider())


    def upperCase(self, text):
        return text.upper()