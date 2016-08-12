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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
from kivy.utils import platform
# this is for network and rs232 control of Integra/Onkyo receivers
if platform != 'android':
    import eiscp


def com_net_eiscp_discovery():
    """
    # the EISCP auto discover only works on 2011 models or higher
    """
    return eiscp.eISCP.discover(timeout=5)


def com_net_eiscp_connection(ip_addr):
    """
    Connect by ip address
    """
    return eiscp.eISCP(ip_addr)


def com_net_eiscp_disconnect(eiscp_device):
    """
    Disconnect from device
    """
    eiscp_device.disconnect()


def com_net_eiscp_command(eiscp_device, eiscp_command):
    eiscp_device.command(eiscp_command)


def com_net_eiscp_command_raw(eiscp_device, eiscp_raw_command):
    eiscp_device.raw(eiscp_raw_command)
