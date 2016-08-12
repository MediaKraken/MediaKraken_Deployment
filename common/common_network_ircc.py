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
import sys
sys.path.append("../../MediaKraken_Common/lib")


# ircc device discovery via ssdp
def com_net_ircc_discover():
    SSDP_MSearch.search(cbFoundDevice=com_net_ircc_Found_Device,\
        cbFinishedSearching=com_net_ircc_Finished_Searching,\
        target='urn:schemas-sony-com:service:IRCC:1')


# filler found device
def com_net_ircc_found_device(ircc_device):
    pass


def com_net_ircc_finished_searching(devices):
    """
    # process the found devices
    """
    ircc_device = devices[0] # first device only for now
    ircc_service = ircc_device.get_service('schemas.sony.com/IRCC/1')
    com_net_ircc_Register_Device(ircc_device, ircc_service)


def com_net_ircc_register_device(ircc_device, ircc_service):
    """
    # register device for control
    """
    if ircc_device.register("My IRCC Controller") != unr.UNR_REGISTER_RESULT_OK:
        logging.error("Registration Failed")


def com_net_ircc_send_command(ircc_device, ircc_service, command_text):
    """
    # send commands to ircc device
    """
    ircc_device.ircc.sendIRCC(command_text)
