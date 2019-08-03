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
from common import common_network_ircc


# ircc device discovery via ssdp
def test_com_net_ircc_discover():
    """
    Test function
    """
    common_network_ircc.com_net_ircc_discover()

# filler found device
# def MK_Network_IRCC_Found_Device(ircc_device):


# process the found devices
# def MK_Network_IRCC_Finished_Searching(devices):


# register device for control
# def MK_Network_IRCC_Register_Device(ircc_device, ircc_service):


# send commands to ircc device
# def MK_Network_IRCC_Send_Command(ircc_device, ircc_service, command_text):
