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

from time import sleep
import android
from jnius import autoclass
import logging


class MK_Android_Hardware_Instance:
    def __init__(self):
        # get hardware instance of device
        self.Android_Hardware = autoclass('org.renpy.android.Hardware')


    # return the dpi for the device
    def MK_Android_Get_DPI(self):
        logging.debug('DPI is', self.Android_Hardware.getDPI())
        return self.Android_Hardware.getDPI()


    # vibrate the device
    def MK_Android_Vibrate(self, vibrate_time):
        self.Android_Hardware.vibrate(vibrate_time)


    # return data from the motion controller
    def MK_Android_Motion(self, time_range):
        self.Android_Hardware.accelerometerEnable(True)
        accel_data = []
        for x in xrange(time_range):
            logging.debug( self.Android_Hardware.accelerometerReading())
            accel_data.append(self.Android_Hardware.accelerometerReading())
            sleep(.1)
        return accel_data
