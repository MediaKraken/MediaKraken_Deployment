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

from common import common_serial


class CommonHardwareControllerSerial(object):
    """
    Class for interfacing with hardware from json specifications
    """

    # db_hardware_json_read will populate the json
    def __init__(self, device_json, device_ip=None, device_port=None):
        self.device_inst = None
        self.device_json = device_json
        self.device_inst = common_serial.CommonSerial()
        self.device_inst.com_serial_open_device(
            self.device_json["Protocol"]["Hardware Port"],
            self.device_json["Protocol"]["Baud Rate"],
            self.device_json["Protocol"]["Parity Bit"],
            self.device_json["Protocol"]["Stop Bit"],
            self.device_json["Protocol"]["Data Length"])

    def com_hardware_command(self, command_value):
        """
        The command_value is the actual command text/ir code to send to hardware.
        The remote control program will have the value assigned to a key/mapping.
        """
        self.device_inst.com_serial_write_device(command_value)

    def com_hardware_close(self):
        self.device_inst.com_serial_close_device()
