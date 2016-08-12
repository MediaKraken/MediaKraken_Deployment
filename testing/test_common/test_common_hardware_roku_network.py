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
from com_Hardware_Roku_Network import *


def test_mk_roku_network_discovery():
    mk_roku_network_discovery()


# def mk_roku_network_command(roku_addr, roku_port, roku_command, roku_command_seconds):


# def mk_roku_network_app_query(roku_addr, roku_port):


# def mk_roku_network_app_launch(roku_addr, roku_port, roku_app_id):


# def mk_roku_network_app_icon(roku_addr, roku_port, roku_app_id):


# def mk_roku_network_touch(roku_addr, roku_port, x, y):
