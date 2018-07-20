import time as tm

from kivy.properties import OptionProperty, AliasProperty
from kivy.uix.label import Label

from .clockbehavior import ClockBehavior


class DigitalClock(ClockBehavior, Label):

    def get_format(self):
        if self.style == 'simple':
            return '%H:%M:%S'
        elif self.style == 'short':
            return '%H:%M'
        elif self.style == 'cool':
            return '[b]%%H %%M [/b][size=%d]%%S[/size]' % round(self.font_size * 0.7)

    style = OptionProperty('simple', options=['simple', 'short', 'cool'])
    fmt = AliasProperty(get_format, None, bind=['style'])
    markup = True

    def on_time(self, *args):
        self.text = tm.strftime(self.fmt, self.time)

    def on_size(self, *args):
        self.text_size = self.size
