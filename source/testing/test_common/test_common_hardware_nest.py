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

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_hardware_nest


# connect to NEST device
# def MK_NEST_Device_Connect(user_name, password):


# grab structures and the devices
# def MK_NEST_Device_Structures(nest_device):


# temp conversion
@pytest.mark.parametrize(("temp_data"), [
    (-7),
    (36)])
def test_com_nest_c_to_f(temp_data):
    """
    Test function
    """
    common_hardware_nest.com_nest_c_to_f(temp_data)


@pytest.mark.parametrize(("temp_data"), [
    (-7),
    (60)])
def test_com_nest_f_to_c(temp_data):
    """
    Test function
    """
    common_hardware_nest.com_nest_f_to_c(temp_data)
