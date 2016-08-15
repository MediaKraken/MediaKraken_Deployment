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


from __future__ import absolute_import, division, print_function, unicode_literals

vibration_pattern = '0.5,0.5,1,2,0.1,0.1,0.1,0.1,0.1,0.1'

import pytest
import sys
sys.path.append("../common")
from common_hardware import *


# turn on accelerometer
def test_mk_hardware_accelerometer_on():
    mk_hardware_accelerometer_on()


# turn off accelerometer
def test_mk_hardware_accelerometer_off():
    mk_hardware_accelerometer_off()


# get accelerometer data
# def mk_get_acceleration(dt):


# setup off the vibration via pattern
def test_mk_hardware_vibration():
    mk_hardware_vibration(pattern_string)


# vibration via time
@pytest.mark.parametrize(("seconds_to_vibrate"), [
    ("0.5"),
    ("2")])
def test_mk_hardware_vibration_time(seconds_to_vibrate):
    mk_hardware_vibration_Time(seconds_to_vibrate)


# stop vibration
def test_mk_hardware_vibration_stop():
    mk_hardware_vibration_Stop()


# gps setup
def test_mk_hardware_gps_on():
    mk_hardware_gps_on()


# gps location
# def on_location(self, **kwargs):


# gps status
# def on_status(self, stype, status):
