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

import sys

sys.path.append("./vault/lib")

from . import common_global


def com_net_ircc_discover():
    """
    # ircc device discovery via ssdp
    """
    SSDP_MSearch.search(cbFoundDevice=com_net_ircc_found_device,
                        cbFinishedSearching=com_net_ircc_finished_searching,
                        target='urn:schemas-sony-com:service:IRCC:1')


def com_net_ircc_found_device(ircc_device):
    """
    Found ircc device
    """
    pass


def com_net_ircc_finished_searching(devices):
    """
    # process the found devices
    """
    ircc_device = devices[0]  # first device only for now
    ircc_service = ircc_device.get_service('schemas.sony.com/IRCC/1')
    com_net_ircc_register_device(ircc_device, ircc_service)


def com_net_ircc_register_device(ircc_device, ircc_service):
    """
    # register device for control
    """
    if ircc_device.register("My IRCC Controller") != unr.UNR_REGISTER_RESULT_OK:
        common_global.es_inst.com_elastic_index('error', {'stuff': "Registration Failed"})


def com_net_ircc_send_command(ircc_device, ircc_service, command_text):
    """
    # send commands to ircc device
    """
    ircc_device.ircc.sendIRCC(command_text)
