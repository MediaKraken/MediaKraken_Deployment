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
import logging
import common.common_network_Telnet


class CommonTivo(object):
    """
    Class for interfacing with tivo device
    """
    def __init__(self):
        pass


    def com_tivo_connect(self, telnet_host, telnet_port=31339):
        """
        Connect to specified tivo
        """
        self.tivo_device = MK_Telnet_Open_Device(telnet_host, telnet_port)
