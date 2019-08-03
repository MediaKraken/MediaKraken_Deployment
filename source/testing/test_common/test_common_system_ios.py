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

import sys

sys.path.append('.')
# from common import common_system_ios
#
#
# class TestiOSHardwareInstance:
#
#     @classmethod
#     def setup_class(self):
#         self.ios_connection = common_system_ios.CommoniOSHardwareInstance()
#
#     @classmethod
#     def teardown_class(self):
#         pass
#
#     @pytest.mark.parametrize(("time_range"), [
#         (0.5),
#         (5)])
#     def test_com_ios_motion(self, time_range):
#         """
#         # return data from the motion controller
#         """
#         self.ios_connection.com_ios_motion(time_range)
#
#     @pytest.mark.parametrize(("time_range"), [
#         (0.5),
#         (5)])
#     def test_com_ios_gyro(self, time_range):
#         """
#         # return data from the gyro
#         """
#         self.ios_connection.com_ios_gyro(time_range)
#
#     @pytest.mark.parametrize(("time_range"), [
#         (0.5),
#         (5)])
#     def test_com_ios_magnetometer(self, time_range):
#         """
#         # return data from the magnetometer
#         """
#         self.ios_connection.com_ios_magnetometer(time_range)
