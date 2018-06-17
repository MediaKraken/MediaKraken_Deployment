'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

import json

from common import common_network_telnet
from common import common_serial


def main_remote_control_event_process(self, action_type_list):
    """
    # process remote control button
    """
    try:
        json_data = json.loads(
            self.remote_mode_details_item[self.remote_mode_currrent_item])
        # check to see if rs232 device is already open
        if json_data["Protocol"]["Method"].lower() == "rs232":
            if not json_data["Protocol"]["Hardware Port"] in self.rs232_devices_dict:
                com_net_telnet_device = common_network_telnet.CommonNetworkTelnet()
                self.rs232_devices_dict[json_data["Protocol"]["Host IP"]] \
                    = com_net_telnet_device.com_net_telnet_open_device(
                    json_data["Protocol"]["Host IP"],
                    json_data["Protocol"]["Host Port"], json_data["Protocol"]["User"],
                    json_data["Protocol"]["Password"])
                com_net_telnet_device.com_net_telnet_write_device(
                    self.octmote_json_fetch_data_for_command(json_data,
                                                             action_type_list))
        # check to see if IR device is already open
        elif json_data["Protocol"]["Method"].lower() == "ir":
            if not json_data["fake"] in self.ir_devices_dict:
                pass
        # check to see if lan device already open
        elif json_data["Protocol"]["Method"].lower() == "lan":
            if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"]) \
                   in self.lan_devices_dict:
                pass
        elif json_data["Protocol"]["Method"].lower() == "telnet":
            # check to see if telnet device already opened
            if not json_data["Protocol"]["Host IP"] in self.telnet_devices_dict:
                com_net_telnet_device = common_network_telnet.CommonNetworkTelnet()
                self.telnet_devices_dict[json_data["Protocol"]["Host IP"]] \
                    = com_net_telnet_device.com_net_telnet_open_device(
                    json_data["Protocol"]["Host IP"],
                    json_data["Protocol"]["Host Port"], json_data["Protocol"]["User"],
                    json_data["Protocol"]["Password"])
                com_net_telnet_device.com_net_telnet_write_device(
                    self.octmote_json_fetch_data_for_command(json_data, action_type_list))
        elif json_data["Protocol"]["Method"].lower() == "serial":
            # check to see if serial device already opened
            if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"]) \
                   in self.serial_devices_dict:
                com_net_serial_device = common_serial.CommonSerial()
                self.serial_devices_dict[(json_data["Protocol"]["Host IP"],
                                          json_data["Protocol"]["Hardware Port"])] \
                    = com_net_serial_device.com_serial_open_device(
                    json_data["Protocol"]["Hardware Port"],
                    json_data["Protocol"]["Baud Rate"], json_data["Protocol"]["Parity Bit"],
                    json_data["Protocol"]["Stop Bit"], json_data["Protocol"]["Data Length"])
                com_net_serial_device.com_serial_write_device(
                    self.octmote_json_fetch_data_for_command(json_data, action_type_list))
        elif json_data["Protocol"]["Method"].lower() == "eiscp":
            # check to see if eiscp device already open
            if not json_data["Protocol"]["Host IP"] in self.eiscp_devices_dict:
                pass
        elif json_data["Protocol"]["Method"].lower() == "kivy":
            if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"]) \
                   in self.kivy_lan_devices_dict:
                self.kivy_lan_devices_dict[(json_data["Protocol"]["Host IP"],
                                            json_data["Protocol"]["Hardware Port"])] \
                    = (json_data["Protocol"]["Host IP"],
                       json_data["Protocol"]["Hardware Port"])
            common_network_kodi.com_net_kodi_command(json_data["Protocol"]["Host IP"],
                                                     json_data["Protocol"]["Hardware Port"],
                                                     self.octmote_json_fetch_data_for_command(
                                                         json_data,
                                                         action_type_list))
        else:
            print(("Unhandled Protocol Method %s",
                   json_data["Protocol"]["Method"]))
    except:
        pass
