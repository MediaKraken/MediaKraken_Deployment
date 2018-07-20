import time as tm
from kivy.properties import ObjectProperty, AliasProperty, NumericProperty
from kivy.clock import Clock


class ClockBehavior(object):

    # Current time. struct_tm object as returned by time.localtime()
    time = ObjectProperty(tm.localtime(), rebind=True)
    # Offset to localtime in seconds. Defaults to 0
    offset = NumericProperty(0)
    # Updating interval in seconds. Defaults to 1s. If 0 clock will not update
    interval = NumericProperty(1)

    def get_strtime(self):
        return tm.strftime('%H:%M:%S', self.time)

    def set_strtime(self, strtime):
        self.time = tm.strptime('%H:%M:%S', strtime)

    strtime = AliasProperty(get_strtime, set_strtime, bind=['time'])

    def __init__(self, **kwargs):
        super(ClockBehavior, self).__init__(**kwargs)
        self.update_clock(self, 0)
        self.on_interval(self, self, self.interval)
        self.on_time(self, self, self.time)

    def update_clock(self, dt, *args):
        self.time = tm.localtime(tm.time() + self.offset)

    def on_interval(self, *args):
        if self.interval:
            Clock.schedule_interval(self.update_clock, self.interval)
        else:
            Clock.unschedule(self.update_clock)

    def on_time(self, *args):
        pass
