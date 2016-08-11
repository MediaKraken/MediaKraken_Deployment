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

import logging
from kivy.utils import platform
if platform != 'android':
    import pylirc as lirc


sockid = None


def MK_LIRC_Init(app_string="OctMote"):
    """
    Initialize LIRC
    """
    sockid = lirc.init(app_string)
    return sockid


def MK_LIRC_Load_Config(config_file):
    """
    Load config file for LIRC
    """
    lirc.load_config_file(config_file)


def MK_LIRC_Close():
    """
    Shutdown LIRC
    """
    lirc.deinit()
