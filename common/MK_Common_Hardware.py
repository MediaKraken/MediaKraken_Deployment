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

vibration_pattern = '0.5,0.5,1,2,0.1,0.1,0.1,0.1,0.1,0.1'

import logging
from kivy.lang import Builder
from kivy.clock import Clock
from plyer import accelerometer
from plyer import gps


# turn on accelerometer
def MK_Hardware_Accelerometer_On():
    accelerometer.enable()
    Clock.schedule_interval(MK_Get_Acceleration, 1 / 20.)


# turn off accelerometer
def MK_Hardware_Accelerometer_Off():
    accelerometer.disable()
    Clock.unschedule(MK_Get_Acceleration)


# get accelerometer data
def MK_Get_Acceleration(dt):
    val = accelerometer.acceleration[:3]
    if(not val == (None, None, None)):
        #ids.x_label.text = "X: " + str(val[0])
        #ids.y_label.text = "Y: " + str(val[1])
        #ids.z_label.text = "Z: " + str(val[2])
        return val


# setup off the vibration via pattern
def MK_Hardware_Vibration(pattern_string):
    vibrator.pattern([float(n) for n in ti.text.split(',')])


# vibration via time
def MK_Hardware_Vibration_Time(seconds_to_vibrate):
    vibrator.vibrate(seconds_to_vibrate)


# stop vibration
def MK_Hardware_Vibration_Stop():
    vibrator.cancel()


# gps setup
def MK_Hardware_GPS_On():
    self.gps = gps
    try:
        self.gps.configure(on_location=self.on_location, on_status=self.on_status)
    except NotImplementedError:
        import traceback; traceback.print_exc()
        self.gps_status = 'GPS is not implemented for your platform'
    return self.gps


# gps location
def on_location(self, **kwargs):
    return '\n'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])


# gps status
def on_status(self, stype, status):
    return 'type={}\n{}'.format(stype, status)
