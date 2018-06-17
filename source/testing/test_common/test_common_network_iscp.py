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
from common import common_network_iscp


# the EISCP auto discover only works on 2011 models or higher
def test_com_net_eiscp_discovery():
    """
    Test function
    """
    common_network_iscp.com_net_eiscp_discovery('10.0.0.1')

# def MK_EISCP_Connection(ip_addr):


# def MK_EISCP_Disconnect(eiscp_device):


# def MK_EISCP_Command(eiscp_device, eiscp_command):


# def MK_EISCP_Command_RAW(eiscp_device, eiscp_raw_command):
