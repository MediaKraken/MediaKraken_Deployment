'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

from lcdproc.server import Server


# https://github.com/jinglemansweep/lcdproc/blob/master/examples.py

# lcdproc class
class CommonLCDProc(object):
    """
    Class for interfacing with lcpproc
    """

    def __init__(self, option_config_json):
        self.lcd = Server("media", debug=False)
        self.lcd.start_session()
        self.screens = {}

    def com_lcdproc_add_screen(self, name, heartbeat='off', duration=10):
        self.screens[name] = self.lcd.add_screen(name)
        self.screens[name].set_heartbeat(heartbeat)
        self.screens[name].set_duration(duration)

    def com_lcdproc_add_string(self, screen_name, name, text, x, y):
        string_widget = self.screens[screen_name].add_string_widget(
            name, text=text, x=x, y=y)

    def com_lcdproc_add_scroller(self, screen_name, name, text, speed=2):
        scroller_widget = self.screens[screen_name].add_scroller_widget(name, text=text,
                                                                        speed=speed)

    def com_lcdproc_add_hbar(self, screen_name, name, x, y, length=60):
        hbar_widget = self.screens[screen_name].add_hbar_widget(
            name, x=x, y=y, length=length)

    def com_lcdproc_add_frame(self, screen_name, name):
        frame_widget = self.screens[screen_name].add_frame_widget(name)

    def com_lcdproc_add_number(self, screen_name, name, x, value):
        num1_widget = self.screens[screen_name].add_number_widget(
            name, x=x, value=value)

#
# progress = 0
#
# while True:
#
#     num1_widget.set_value(progress)
#     num2_widget.set_value(progress)
#     num3_widget.set_value(progress)
#     num4_widget.set_value(progress)
#
#     time.sleep(0.5)
#
#     progress = progress + 1
#     if progress > 9: progress = 0
