'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

from . import common_hardware_marantz
from . import common_hardware_pioneer
from . import common_hardware_samsung


class CommonHardwareController(object):
    """
    Class for interfacing with hardware from json specifications
    """

    def __init__(self, device_manufacturer, device_json, device_communication, device_ip,
                 device_port):
        self.device_inst = None
        self.device_manufacturer = device_manufacturer
        self.device_json = device_json
        if device_communication == 'network':
            if device_manufacturer == 'marantz':
                self.device_inst = common_hardware_marantz.CommonHardwareMarantz(
                    device_ip=device_ip)
            elif device_manufacturer == 'pioneer':
                self.device_inst = common_hardware_pioneer.CommonHardwarePioneer(
                    device_ip=device_ip, device_port=device_port)
            elif device_manufacturer == 'samsung':
                self.device_inst = common_hardware_samsung.CommonHardwareSamsung(
                    device_ip=device_ip)
        elif device_communication == 'ir remote':
            pass

    def com_hardware_command(self, command_type, command_value):
        if command_type == 'Volume Up':
            self.com_hardware_command_send(self.device_json['Commands']['Sound']['Volume Up'])
        elif command_type == 'Volume Down':
            self.com_hardware_command_send(self.device_json['Commands']['Sound']['Volume Down'])
        elif command_type == 'Mute':
            self.com_hardware_command_send(self.device_json['Commands']['Sound']['Mute'])
        elif command_type == 'UnMute':
            self.com_hardware_command_send(self.device_json['Commands']['Sound']['UnMute'])
        else:
            self.com_hardware_command_send(command_type, command_value)

    def com_hardware_command_send(self, command_json, command_value=None):
        pass
