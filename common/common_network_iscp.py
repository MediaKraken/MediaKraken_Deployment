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
# this is for network and rs232 control of Integra/Onkyo receivers
if platform != 'android':
    import eiscp


# the EISCP auto discover only works on 2011 models or higher
def MK_EISCP_Discovery():
    return eiscp.eISCP.discover(timeout=5)


def MK_EISCP_Connection(ip_addr):
    return eiscp.eISCP(ip_addr)


def MK_EISCP_Disconnect(eiscp_device):
    eiscp_device.disconnect()


def MK_EISCP_Command(eiscp_device, eiscp_command):
    eiscp_device.command(eiscp_command)


def MK_EISCP_Command_RAW(eiscp_device, eiscp_raw_command):
    eiscp_device.raw(eiscp_raw_command)
