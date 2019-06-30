from math import sin, cos, pi

from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, AliasProperty
from kivy.uix.widget import Widget

from .clockbehavior import ClockBehavior


class AnalogClock(ClockBehavior, Widget):
    padding = NumericProperty(0)
    color = ListProperty([1, 1, 1, 1])

    def get_radius(self):
        return min(self.width, self.height) / 2 - self.padding

    radius = AliasProperty(get_radius, None, bind=['size', 'padding'])

    def calc_angles(self):
        angles = {'h': self.hour_to_angle((self.time.tm_hour * 60 + self.time.tm_min) / 12),
                  'm': self.hour_to_angle(self.time.tm_min),
                  's': self.hour_to_angle(self.time.tm_sec)}
        return angles

    angles = AliasProperty(calc_angles, None, bind=['time'])

    @staticmethod
    def hour_to_angle(value):
        angle = (90 - (value * 360 / 60)) % 360
        return angle * pi / 180

    @staticmethod
    def calc_line_points(center=(0, 0), angle=0, radius=1):
        x1 = center[0]
        y1 = center[1]
        x2 = x1 + cos(angle) * radius
        y2 = y1 + sin(angle) * radius
        return (x1, y1, x2, y2)


Builder.load_string("""

<AnalogClock>:
    canvas:
        Color:
            id: color
            rgba: self.color
        Line:
            id: border
            circle: (self.center_x, self.center_y, self.radius * 0.95)
            width: 2
        Line:
            id: hand_s
            points: root.calc_line_points(self.center, self.angles['s'], self.radius * 0.85)
            width: 1
        Line:
            id: hand_m
            points: root.calc_line_points(self.center, self.angles['m'], self.radius * 0.8)
            width: 2
        Line:
            id: hand_h
            points: root.calc_line_points(self.center, self.angles['h'], self.radius * 0.55)
            width: 2
""")
