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
import telnetlib
import time
newline = "\n"


class MK_Common_Telnet_API:
    def __init__(self):
        pass


    def MK_Telnet_Open_Device(self, telnet_host, telnet_port, telnet_user=None, telnet_password=None):
        self.telnet_device = telnetlib.Telnet(telnet_host, telnet_port)
        if telnet_user is not None:
            self.telnet_device.read_until("login: ")
            self.telnet_device.write(telnet_user + newline)
            self.telnet_device.read_until("Password: ")
            self.telnet_device.write(telnet_password + newline)
    
    
    def MK_Telnet_Read_Device(self):
        time.sleep(1)
        read_data = ''
        while self.telnet_device.inWaiting() > 0:
            read_data += self.telnet_device.read_all()
        return read_data
    
    
    def MK_Telnet_Write_Device(self, telnet_message):
        self.telnet_device.write(telnet_message + newline)
