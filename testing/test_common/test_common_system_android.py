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


import pytest
import sys
sys.path.append("../common")
from MK_Common_System_Android import *


class Test_MK_Android_Hardware_Instance:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_System_Android.MK_Android_Hardware_Instance()


    @classmethod
    def teardown_class(self):
        pass


    # return the dpi for the device
    def test_MK_Android_Get_DPI(self):
        MK_Android_Get_DPI()


    # vibrate the device
    @pytest.mark.parametrize(("vibrate_time"), [
        (0.5),
        (5)])
    def test_MK_Android_Vibrate(self, vibrate_time):
        MK_Android_Vibrate(vibrate_time)


    # return data from the motion controller
    @pytest.mark.parametrize(("vibrate_time"), [
        (0.5),
        (5)])
    def test_MK_Android_Motion(self, time_range):
        MK_Android_Motion(time_range)
