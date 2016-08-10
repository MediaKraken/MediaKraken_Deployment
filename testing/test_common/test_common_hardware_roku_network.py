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
sys.path.append("../MediaKraken_Common")
from MK_Common_Hardware_Roku_Network import *


def test_MK_Roku_Network_Discovery():
    MK_Roku_Network_Discovery()


# def MK_Roku_Network_Command(roku_addr, roku_port, roku_command, roku_command_seconds):


# def MK_Roku_Network_App_Query(roku_addr, roku_port):


# def MK_Roku_Network_App_Launch(roku_addr, roku_port, roku_app_id):


# def MK_Roku_Network_App_Icon(roku_addr, roku_port, roku_app_id):


# def MK_Roku_Network_Touch(roku_addr, roku_port, x, y):
