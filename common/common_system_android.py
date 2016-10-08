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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
from time import sleep
#import android
from jnius import autoclass


class CommonAndroidHardwareInstance(object):
    """
    Class for interfacing with android hardware
    """
    def __init__(self):
        # get hardware instance of device
        self.android_hardware = autoclass('org.renpy.android.Hardware')


    def com_android_get_dpi(self):
        """
        Return the dpi for the device
        """
        logging.info('DPI is %s', self.android_hardware.getDPI())
        return self.android_hardware.getDPI()


    def com_android_vibrate(self, vibrate_time):
        """
        Vibrate the device
        """
        self.android_hardware.vibrate(vibrate_time)


    def com_android_motion(self, time_range):
        """
        Return data from the motion controller
        """
        self.android_hardware.accelerometerEnable(True)
        accel_data = []
        for ndx in xrange(time_range): # pylint: disable=W0612
            logging.info('Motion: %s', self.android_hardware.accelerometerReading())
            accel_data.append(self.android_hardware.accelerometerReading())
            sleep(.1)
        return accel_data
