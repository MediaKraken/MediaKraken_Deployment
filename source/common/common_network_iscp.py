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

from kivy.utils import platform

# this is for network and rs232 control of Integra/Onkyo receivers
if platform != 'android':
    import eiscp


def com_net_eiscp_discovery(self):
    """
    # the EISCP auto discover only works on 2011 models or higher
    """
    return eiscp.eISCP.discover(timeout=5)


class CommonNetworkEISCP:
    """
    Class for interfacing via Onkyo equipment
    """

    def __init__(self, ip_addr):
        self.eiscp_inst = eiscp.eISCP(ip_addr)

    def com_net_eiscp_disconnect(self):
        """
        Disconnect from device
        """
        self.eiscp_inst.disconnect()

    def com_net_eiscp_command(self, eiscp_command):
        """
        Send command via eiscp
        """
        self.eiscp_inst.command(self, eiscp_command)

    def com_net_eiscp_command_raw(self, eiscp_raw_command):
        """
        Send raw tcp
        """
        self.eiscp_inst.raw(eiscp_raw_command)
