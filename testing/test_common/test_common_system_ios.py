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
import pytest
import sys
sys.path.append("../common")
from common_system_iOS import *


class TestiOSHardwareInstance(object):


    @classmethod
    def setup_class(self):
        self.db = common_system_iOS.MK_iOS_Hardware_Instance()


    @classmethod
    def teardown_class(self):
        pass


    # return data from the motion controller
    @pytest.mark.parametrize(("time_range"), [
        (0.5),
        (5)])
    def test_MK_iOS_Motion(self, time_range):
        MK_iOS_Motion(time_range)


    # return data from the gyro
    @pytest.mark.parametrize(("time_range"), [
        (0.5),
        (5)])
    def test_MK_iOS_Gyro(self, time_range):
        MK_iOS_Gyro(time_range)


    # return data from the magnetometer
    @pytest.mark.parametrize(("time_range"), [
        (0.5),
        (5)])
    def test_MK_iOS_Magnetometer(self, time_range):
        MK_iOS_Magnetometer(time_range)
