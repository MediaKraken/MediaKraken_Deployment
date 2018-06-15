'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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

# from kivy.lang import Builder
from kivy.clock import Clock
from plyer import accelerometer
from plyer import gps
from plyer import vibrator

VIBRATION_PATTERN = '0.5,0.5,1,2,0.1,0.1,0.1,0.1,0.1,0.1'


def mk_hardware_accelerometer_on():
    """
    Turn on accelerometer
    """
    accelerometer.enable()
    Clock.schedule_interval(mk_get_acceleration, 1 / 20.)


def mk_hardware_accelerometer_off():
    """
    Turn off accelerometer
    """
    accelerometer.disable()
    Clock.unschedule(mk_get_acceleration)


def mk_get_acceleration(dt):
    """
    Get accelerometer data
    """
    val = accelerometer.acceleration[:3]
    if not val == (None, None, None):
        # ids.x_label.text = "X: " + str(val[0])
        # ids.y_label.text = "Y: " + str(val[1])
        # ids.z_label.text = "Z: " + str(val[2])
        return val


def mk_hardware_vibration(pattern_string):
    """
    Setup of the vibration via pattern
    """
    try:
        vibrator.pattern([float(n) for n in pattern_string.split(',')])
    except NotImplementedError:
        pass


def mk_hardware_vibration_time(seconds_to_vibrate):
    """
    Vibration via time
    """
    try:
        vibrator.vibrate(seconds_to_vibrate)
    except NotImplementedError:
        pass


def mk_hardware_vibration_stop():
    """
    Stop vibration
    """
    try:
        vibrator.cancel()
    except NotImplementedError:
        pass


def mk_hardware_gps_on():
    """
    gps setup
    """
    try:
        gps.configure(on_location=on_location, on_status=on_status)
    except NotImplementedError:
        import traceback
        traceback.print_exc()
        gps_status = 'GPS is not implemented for your platform'
    return gps


def on_location(self, **kwargs):
    """
    gps location
    """
    return '\n'.join(['{}={}'.format(k, v) for k, v in list(kwargs.items())])


def on_status(self, stype, status):
    """
    gps status
    """
    return 'type={}\n{}'.format(stype, status)
