"""
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
"""

# from . import common_hardware_controller_eiscp
# from . import common_hardware_controller_ir
from . import common_hardware_controller_kodi
# from . import common_hardware_controller_lan
from . import common_hardware_controller_rs232
from . import common_hardware_controller_serial
from . import common_hardware_controller_telnet
from . import common_hardware_marantz
from . import common_hardware_pioneer
from . import common_hardware_samsung


class CommonHardwareController:
    """
    Class for interfacing with hardware from json specifications
    """

    # db_hardware_json_read will populate the json
    def __init__(self, device_json, device_ip=None, device_port=None, source_remote_ip=None):
        self.device_inst = None
        self.device_json = device_json
        if self.device_json['Manufacturer'] == 'Marantz':
            self.device_inst = common_hardware_marantz.CommonHardwareMarantz(
                device_ip=device_ip)
        elif self.device_json['Manufacturer'] == 'Pioneer':
            self.device_inst = common_hardware_pioneer.CommonHardwarePioneer(
                device_ip=device_ip, device_port=device_port)
        elif self.device_json['Manufacturer'] == 'Samsung':
            self.device_inst = common_hardware_samsung.CommonHardwareSamsung(
                source_remote_ip=source_remote_ip, device_ip=device_ip)
        else:
            # setup the initial connection that aren't setup above
            if self.device_json['Protocol']['Method'] == "EISCP":
                pass
            elif self.device_json['Protocol']['Method'] == "IR":
                pass
            elif self.device_json['Protocol']['Method'] == "Kodi":
                self.device_inst = common_hardware_controller_kodi.CommandHardwareControllerKodi(
                    self.device_json)
            elif self.device_json['Protocol']['Method'] == "LAN":
                pass
            elif self.device_json['Protocol']['Method'] == "RS232":
                self.device_inst = common_hardware_controller_rs232.CommandHardwareControllerRS232(
                    self.device_json)
            elif self.device_json['Protocol']['Method'] == "Serial":
                self.device_inst = common_hardware_controller_serial.CommonHardwareControllerSerial(
                    self.device_json)
            elif self.device_json['Protocol']['Method'] == "Telnet":
                self.device_inst = common_hardware_controller_telnet.CommonHardwareControllerTelnet(
                    self.device_json)

    def com_hardware_command(self, command_value):
        """
        The command_value is the actual command text/ir code to send to hardware.
        The remote control program will have the value assigned to a key/mapping.
        """
        self.device_inst.com_hardware_command(command_value)

    def com_hardware_close(self):
        self.device_inst.com_hardware_close()
