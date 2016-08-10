'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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

import pytest
import sys
sys.path.append("../common")
from MK_Common_Hardware import *


# turn on accelerometer
def test_MK_Hardware_Accelerometer_On():
    MK_Hardware_Accelerometer_On()


# turn off accelerometer
def test_MK_Hardware_Accelerometer_Off():
    MK_Hardware_Accelerometer_Off()


# get accelerometer data
# def MK_Get_Acceleration(dt):


# setup off the vibration via pattern
def test_MK_Hardware_Vibration():
    MK_Hardware_Vibration(pattern_string)


# vibration via time
@pytest.mark.parametrize(("seconds_to_vibrate"), [
    ("0.5"),
    ("2")])
def test_MK_Hardware_Vibration_Time(seconds_to_vibrate):
    MK_Hardware_Vibration_Time(seconds_to_vibrate)


# stop vibration
def test_MK_Hardware_Vibration_Stop():
    MK_Hardware_Vibration_Stop()


# gps setup
def test_MK_Hardware_GPS_On():
    MK_Hardware_GPS_On()


# gps location
# def on_location(self, **kwargs):


# gps status
# def on_status(self, stype, status):
