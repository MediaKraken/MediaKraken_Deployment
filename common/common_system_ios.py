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
import logging
from pyobjus import autoclass


class CommoniOSHardwareInstance(object):
    """
    Class for interfacing with iOS hardware
    """
    def __init__(self):
# get hardware instance of device
        self.iOS_Hardware = autoclass('bridge')


    def com_ios_motion(self, time_range):
        """
        # return data from the motion controller
        """
        br = self.iOS_Hardware.alloc().init()
        br.motionManager.setAccelerometerUpdateInterval_(0.1)
        br.startAccelerometer()
        accel_data = []
        for i in range(time_range):
            logging.debug('x: {0} y: {1} z: {2}'.format(br.ac_x, br.ac_y, br.ac_z))
            accel_data.append((br.ac_x, br.ac_y, br.ac_z))
        return accel_data


    def com_ios_gyro(self, time_range):
        """
        # return data from the gyro
        """
        br = self.iOS_Hardware.alloc().init()
        br.startGyroscope()
        gyro_data = []
        for i in range(time_range):
            logging.debug('x: {0} y: {1} z: {2}'.format(br.gy_x, br.gy_y, br.gy_z))
            gyro_data.append((br.ac_x, br.ac_y, br.ac_z))
        return gyro_data


    def com_ios_magnetometer(self, time_range):
        """
        # return data from the magnetometer
        """
        br = self.iOS_Hardware.alloc().init()
        br.startMagnetometer()
        mag_data = []
        for i in range(time_range):
            logging.debug('x: {0} y: {1} z: {2}'.format(br.mg_x, br.mg_y, br.mg_z))
            mag_data.append((br.mg_x, br.mg_y, br.mg_z))
        return mag_data
