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

import telnetlib

NEWLINE = "\n"


class CommonNetworkTelnet(object):
    """
    Class for interfacing with telnet protocol
    """

    def __init__(self, telnet_host, telnet_port, telnet_user=None,
                 telnet_password=None):
        """
        Open device via telnet
        """
        self.telnet_device = telnetlib.Telnet(telnet_host, telnet_port)
        if telnet_user is not None:
            self.telnet_device.read_until("login: ")
            self.telnet_device.write(telnet_user + NEWLINE)
            self.telnet_device.read_until("Password: ")
            self.telnet_device.write(telnet_password + NEWLINE)

    def com_net_telnet_read_device(self):
        """
        Read data from telnet device
        """
        return self.telnet_device.read_very_eager()

    def com_net_telnet_write_device(self, telnet_message):
        """
        Send data to telnet device
        """
        self.telnet_device.write(telnet_message + NEWLINE)

    def com_net_telnet_close(self):
        self.telnet_device.close()
